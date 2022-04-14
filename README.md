# content-tracking
quick demo for tracking content views, interactions...

## Working with the Tinybird CLI

To start working with data projects as if they were software projects, let's install the Tinybird CLI in a virtual environment.
Check the [CLI documentation](https://docs.tinybird.co/cli.html) for other installation options and troubleshooting.

```bash
cd data-project
virtualenv -p python3 .e
. .e/bin/activate
pip install tinybird-cli
tb auth --interactive
```

Choose your region: __1__ for _us-east_, __2__ for _eu_

Go to your workspace, copy a token with admin rights and paste it. A new `.tinyb` file will be created.

```bash
tb push --fixtures --push-deps
```

## Data Project

```bash
├── datasources
│   ├── content_daily_mv.datasource
│   ├── content.datasource
│   ├── events.datasource
│   ├── events_enriched_mv.datasource
│   └── fixtures
│       └── content.csv
├── endpoints
│   ├── events_demo.pipe
│   ├── fatser_events_demo.pipe
│   └── most_interacted_content.pipe
└── pipes
    ├── content_daily.pipe
    └── enriching_mat.pipe
```

## Sending dummy events

from the root folder, just run

```bash
python3 data-generator/send_events.py --create_users
```

or any combination of flags —see `python3 data-generator/send_events.py --help`— you want. For the video we used:

```bash
python3 data-generator/send_events.py --repeat 1200000  --events 213 --sample 1009
```
