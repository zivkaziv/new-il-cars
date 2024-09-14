import os
import json
import time
import requests
from mailjet_rest import Client

# Environment variables
MAILJET_API_KEY = os.environ['MAILJET_API_KEY']
MAILJET_API_SECRET = os.environ['MAILJET_API_SECRET']
SENDER_EMAIL = os.environ['SENDER_EMAIL']
RECIPIENT_EMAIL = os.environ['RECIPIENT_EMAIL']
DATA_FILE = os.environ['DATA_FILE']
SLEEP_TIME = int(os.environ.get('SLEEP_TIME', 14400))  # Default to 4 hours (14400 seconds) if not set

def make_request():
    url = 'https://data.gov.il/api/3/action/datastore_search'
    headers = {
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/x-www-form-urlencoded'
    }
    data = {
        "resource_id": "39f455bf-6db0-4926-859d-017f34eacbcb",
        "q": "",
        "filters": {"not_count_request": "0"},
        "limit": 1,
        "offset": 0,
        "sort": "_id desc"
    }
    
    response = requests.post(url, headers=headers, json=data)
    return response.json()

def get_latest_id():
    response_data = make_request()
    if response_data['success'] and response_data['result']['records']:
        return response_data['result']['records'][0]['_id']
    return None

def read_saved_id():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return int(f.read().strip())
    return 0

def save_id(new_id):
    with open(DATA_FILE, 'w') as f:
        f.write(str(new_id))

def send_email(subject, body):
    mailjet = Client(auth=(MAILJET_API_KEY, MAILJET_API_SECRET), version='v3.1')
    data = {
        'Messages': [
            {
                "From": {
                    "Email": SENDER_EMAIL,
                    "Name": "Car Data Monitor"
                },
                "To": [
                    {
                        "Email": RECIPIENT_EMAIL,
                        "Name": "Recipient"
                    }
                ],
                "Subject": subject,
                "TextPart": body
            }
        ]
    }
    result = mailjet.send.create(data=data)
    print(result.status_code)
    print(result.json())

def check_for_updates():
    latest_id = get_latest_id()
    if latest_id is None:
        print("Failed to fetch the latest ID")
        return
    
    saved_id = read_saved_id()
    
    if latest_id > saved_id:
        print(f"New data found: ID {latest_id}")
        save_id(latest_id)
        subject = "New Car Data Available"
        body = f"""A new car record with ID {latest_id} has been added to the database. 
        Checkout the following link for more details - https://data.gov.il/dataset/mehir_yevuan/resource/39f455bf-6db0-4926-859d-017f34eacbcb"""
        send_email(subject, body)
    else:
        print("No new data found")

def main():
    while True:
        print("Checking for updates...")
        check_for_updates()
        print(f"Sleeping for {SLEEP_TIME} seconds...")
        time.sleep(SLEEP_TIME)
        
if __name__ == "__main__":
    main()