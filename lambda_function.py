import boto3
import requests
from bs4 import BeautifulSoup
import emoji

# init website
WEBSITE_URL = "https://onemotoring.lta.gov.sg/content/onemotoring/home/driving/traffic_information/traffic_updates_and_road_closures.html"

# init dynamodb
dynamodb = boto3.client('dynamodb')
LAST_UPDATE_TABLE_NAME = "sgroadalert-lastupdate"

# init ssm for telegram
ssm = boto3.client('ssm')
response_BOT_TOKEN = ssm.get_parameter(
    Name='telagram-bot-token-coderautobot',
    WithDecryption=True
)
response_CHAT_ID_sgroadalert = ssm.get_parameter(
    Name='telagram-chatid-sgroadalert'
)
BOT_TOKEN = response_BOT_TOKEN['Parameter']['Value']
TELEGRAM_CHAT_ID = response_CHAT_ID_sgroadalert['Parameter']['Value']


def lambda_handler(event, context):
    # Fetch last checked update
    last_update = fetch_last_update()
    print(last_update)

    # Fetch current traffic update
    current_update = fetch_traffic_update()
    print(current_update)

    # Compare current and last updates
    if current_update != last_update:
        # Update last checked update
        update_last_update(current_update)

        # Send Telegram message
        send_telegram_message(current_update)

    return {
        'statusCode': 200,
        'body': 'Traffic update check completed.'
    }


def fetch_traffic_update():
    response = requests.get(WEBSITE_URL)
    html_content = response.text

    # Parse HTML and extract traffic update
    soup = BeautifulSoup(html_content, 'html.parser')
    table = soup.find('table', class_='traffic-updates__table')
    if table:
        rows = table.find_all('tr')
        if len(rows) > 0:
            first_row = rows[0]
            img = first_row.find('img')
            if img:
                img_src = img['src']
                if 'traffic_3' in img_src:
                    emoji = '🔩'  # Add the emoji you want to display for traffic_3 breakdown
                elif 'traffic_1' in img_src:
                    emoji = '🚧'  # Add the emoji for traffic_1 roadworks
                elif 'traffic_0' in img_src:
                    emoji = '💥'  # Add the emoji for traffic_0 accident
                elif 'traffic_8' in img_src:
                    emoji = '🚦'  # Add the emoji for traffic_8 jam
                else:
                    emoji = '⚠️'  # Default emoji if no match is found

                description = first_row.find(
                    'div', class_='traffic-updates__desc').text.strip()
                timestamp = first_row.find(
                    'div', class_='traffic-updates__time').text.strip()
                return {'emoji': emoji, 'description': description, 'timestamp': timestamp}

    return None


def fetch_last_update():
    response = dynamodb.get_item(
        TableName=LAST_UPDATE_TABLE_NAME,
        Key={'id': {'S': 'last_update'}}
    )
    item = response.get('Item')

    if item:
        description = item.get('description', {}).get('S', '')
        # Extract the first character as the emoji code
        emoji = description[0] if len(description) > 0 else ''
        # Remove the emoji code and any leading/trailing spaces from the description
        description = description[1:].strip()
        timestamp = item.get('timestamp', {}).get('S', '')
        return {'emoji': emoji, 'description': description, 'timestamp': timestamp}

    return None


def update_last_update(update):
    # Update last update in DynamoDB
    # Get the emoji value from the update dictionary, or use an empty string if not present
    emoji = update.get('emoji', '')
    dynamodb.put_item(
        TableName=LAST_UPDATE_TABLE_NAME,
        Item={
            'id': {'S': 'last_update'},
            # Include the emoji in the description
            'description': {'S': emoji + update['description']},
            'timestamp': {'S': update['timestamp']}
        }
    )


def send_telegram_message(update):
    # Compose message with emojis
    # Get the emoji code from the update dictionary, or use an empty string if not present
    emoji_code = update.get('emoji', '')
    description = update['description']
    timestamp = update['timestamp']

    # Replace emoji aliases with Unicode representations
    emoji_mapping = {
        ':hammer_and_wrench:': '🔩',  # Replace ':hammer_and_wrench:' with '🔩'
        ':construction:': '🚧',  # Replace ':construction:' with '🚧'
        ':collision:': '💥',  # Replace ':collision:' with '💥'
        ':traffic_light:': '🚦',  # Replace ':traffic_light:' with '🚦'
        ':warning:': '⚠️'  # Replace ':warning:' with '⚠️'
    }

    for alias, emoji in emoji_mapping.items():
        description = description.replace(alias, emoji)
        timestamp = timestamp.replace(alias, emoji)

    message = f"{emoji_code} {description}\n\n{timestamp}"

    requests.get(
        f"https://api.telegram.org/{BOT_TOKEN}/sendMessage?chat_id={TELEGRAM_CHAT_ID}&text="
        + f"{message}"
        + "&parse_mode=markdown&disable_web_page_preview=True"
    )
