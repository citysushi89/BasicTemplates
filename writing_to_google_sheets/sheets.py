from dotenv import load_dotenv
import os
from datetime import datetime
import requests
load_dotenv()

URL = os.getenv('SHEETY_URL_WITH_APIKEY')
today_date = datetime.now().strftime("%x")
sheet_inputs = {
    "api_access": {
        "item": "Testing Item",
        "cost": "Testing Cost",
        "link": "Testing Link",
        "inStock": "Testing Stock",
        "date": today_date,
    }
}

sheet_response = requests.post(URL, json=sheet_inputs)
response = sheet_response.json()
print(type(sheet_response))


print(sheet_response.text)