im lazy to write documentation for this repo

aspect: monitoring, change detection and alert

[telegram channel](https://t.me/TrafficAlertSG)

[website](https://onemotoring.lta.gov.sg/content/onemotoring/home/driving/traffic_information/traffic_updates_and_road_closures.html#traffic-updates)

**create directory**

pip install beautifulsoup4 --target . --no-user

pip install emoji --target . --no-user

create lambda_function.py and paste the code in

zip the files to lambda_function.zip and standby to upload to lambda

**create lambda**

name: sgroadalert

upload lambda_function.zip

add Execution role AmazonSSMReadOnlyAccess

timeout set 30s

note: 128mb, average 3000ms, runs every minute and we are still within free tier!
```
Unit conversions
Number of requests: 1 per minute * (60 minutes in an hour x 730 hours in a month) = 43800 per month
Amount of memory allocated: 128 MB x 0.0009765625 GB in a MB = 0.125 GB
Amount of ephemeral storage allocated: 512 MB x 0.0009765625 GB in a MB = 0.5 GB
Pricing calculations
43,800 requests x 3,000 ms x 0.001 ms to sec conversion factor = 131,400.00 total compute (seconds)
0.125 GB x 131,400.00 seconds = 16,425.00 total compute (GB-s)
16,425.00 GB-s - 400000 free tier GB-s = -383,575.00 GB-s
Max (-383575.00 GB-s, 0 ) = 0.00 total billable GB-s
Tiered price for: 0.00 GB-s
Total tier cost = 0.0000 USD (monthly compute charges)
43,800 requests - 1000000 free tier requests = -956,200 monthly billable requests
Max (-956200 monthly billable requests, 0 ) = 0.00 total monthly billable requests
0.50 GB - 0.5 GB (no additional charge) = 0.00 GB billable ephemeral storage per function
Lambda costs - With Free Tier (monthly): 0.00 USD
```
https://calculator.aws/#/addService/Lambda

**create environment in lambda**

key:

description: any 

timestamp: any 

emoji: any

**create eventBridge**

name: schedule-sg-road-alert

cron(*/1 * * * ? *)

**ssm**

BOT_TOKEN with WithDecryption

TELEGRAM_CHAT_ID
