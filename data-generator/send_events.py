import uuid
import requests
import json
from datetime import datetime, timedelta
import click
import random

def send_event(ds: str, token: str, messages: list, host: str):
  params = {
    'name': ds,
    'token': token,
    'wait': 'false',
    'host': host,
  }
  data = '\n'.join(json.dumps(m) for m in messages)
  r = requests.post(f'{host}/v0/events', params=params, data=data)
  # uncomment the following two lines in case you don't see your data in the datasource
  # print(r.status_code)
  # print(r.text)

@click.command()
@click.option('--datasource', help ='the destination datasource. Default = events', default='events')
@click.option('--sample', help = 'number of messages simulated in each repetition. Default = 100', type=int, default=100)
@click.option('--events', help = 'number of events per request. Sent as NDJSON in the body. Default = 50', type=int, default=50)
@click.option('--repeat', type=int, default=1)
@click.option('--silent', is_flag=True, default=False)
@click.option('--d_from', help = 'used along d_to to simulate data from the past. d_from lets you select the number of days previous to today for starting the simulation. Default = 0', type=int, default=0)
@click.option('--d_to', help = 'used along d_from to simulate data from the past. d_to lets you select the number of days previous to today for ending the simulation. Default = 0', type=int, default=0)
@click.option('--create_users', is_flag=True, default=False)
def send_hfi(datasource,
             sample,
             events,
             repeat,
             silent,
             d_from,
             d_to,
             create_users
             ):

 
  with open ("./data-project/.tinyb") as tinyb:
    tb = json.load(tinyb)
    token = tb['token']
    host = tb['host']

  if(not(create_users)):
    get_user_ids = requests.get(f"{host}/v0/sql?q=select distinct userId as id from events format JSON&token={token}").json()['data'] 

  for _ in range(repeat):  

    get_content_ids = requests.get(f"{host}/v0/sql?q=SELECT id, rand() r FROM content order by r limit {events} format JSON&token={token}").json()['data']

    if(create_users):
        get_user_ids = [uuid.uuid4().hex for s in range(int(events/5))]
    
    nd = []
    
    for s in range(sample):
        user_ids = random.choices(get_user_ids, k=events)
        content_ids = random.choices(get_content_ids, k=events)
        event_types = random.choices(['view','edit','share','publish'], weights=[x + y for x, y in zip([100,40,15,1], [random.randint(-3,10) for _ in range(4)])], k=events)

        if (d_from != 0):
            delta_days=random.randint(d_to,d_from)
            delta_seconds=random.randint(1,3600*24)

        message = {
        'timestamp': (datetime.utcnow() - timedelta(days=delta_days, seconds=delta_seconds)).isoformat() if (d_from != 0) else datetime.utcnow().isoformat(),
        'userId':  str(user_ids[s%events]) if (create_users) else str(user_ids[s%events]['id']),
        'contentId': content_ids[s%events]['id'],
        'eventType': event_types[s%events]
        }
        # time.sleep(0.05)

        nd.append(message) 
        if len(nd) == events:
            send_event(datasource, token, nd, host)
            nd = []
        if not(silent):
            print(message) 
    send_event(datasource, token, nd, host)
    nd = []


if __name__ == '__main__':
    send_hfi()
