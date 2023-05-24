im lazy to write documentation for this repo

aspect: monitoring, change detection and alert

[telegram channel](t.me/RoadAlertSG)

[website](https://onemotoring.lta.gov.sg/content/onemotoring/home/driving/traffic_information/traffic_updates_and_road_closures.html#traffic-updates)

**create directory**

pip install beautifulsoup4 --target . --no-user

pip install emoji --target . --no-user

create lambda_function.py and paste the code in

zip the files to lambda_function.zip and standby to upload to lambda

**create dynamodb**

name: sgroadalert-lastupdate

attributes below:

id: last_update in string, literally last_update

description: any string 

timestamp: any string 

**create lambda**

name: sgroadalert

upload lambda_function.zip

add Execution role AmazonDynamoDBFullAccess and AmazonSSMReadOnlyAccess

timeout set 1 min

**create eventBridge**

name: schedule-sg-road-alert

cron(*/5 * * * ? *)

**ssm**

BOT_TOKEN with WithDecryption

TELEGRAM_CHAT_ID
