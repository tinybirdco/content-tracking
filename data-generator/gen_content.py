import datetime
import csv
import random
import uuid

SAMPLE = 1_000_000

def generate_prods():
  headers = ['id','type','company']
  print(datetime.datetime.now())

  file_name = 'content.csv'
  type_names = ['presentation','social media','video','print products','marketing','office']
  company_names = ['Tinybird Co','Content Company','Example Inc','Speedwins Tech','Realtime Data']
  
  type_weights = [random.random() for _ in range(len(type_names))]
  types = random.choices(type_names,type_weights,k=SAMPLE)
  company_weights = [random.random() for _ in range(len(company_names))]
  companies = random.choices(company_names,company_weights,k=SAMPLE)

  with open (f'./data-project/datasources/fixtures/{file_name}','w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(headers)
    for _ in range(SAMPLE):
      id = uuid.uuid4().hex
      type = types[_]
      company = companies[_]
      writer.writerow([id,type,company])
  print(datetime.datetime.now())
  print(file_name)
  return(file_name) 
 
if __name__ == '__main__':
 generate_prods()
