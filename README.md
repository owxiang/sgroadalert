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
