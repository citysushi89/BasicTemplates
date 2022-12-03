"""
WORKS AS OF 12/03/2022 - BUT NEED TO CREATE A DIFFERENT APP PASSWORD
main.py searches to see if If the ISS is close to my current position and if it is currently dark, then
then sends me an email to tell me to look up.
The code was launched to python anywhere and set to run in the cloud
"""
 
import requests
from datetime import datetime
import smtplib
import time
from dotenv import load_dotenv
import os
 
# Set up env variables
load_dotenv()
MY_FROM_EMAIL = os.getenv("MY_FROM_EMAIL")
MY_TO_EMAIL = os.getenv("MY_TO_EMAIL")
MY_PASSWORD = os.getenv("MY_PASSWORD")
MY_LAT = os.getenv("MY_LAT")
MY_LONG = os.getenv("MY_LONG")
 
 
def is_iss_overhead():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()
    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])
 
    if MY_LAT-5 <= iss_latitude <= MY_LAT+5 and MY_LONG-5 <= iss_longitude <= MY_LONG+5:
        return True
 
 
def is_night():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }
    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])
    time_now = datetime.now().hour
    if time_now <= sunrise or time_now >= sunset:
        return True
 
 
while True:
    time.sleep(60)
    if is_iss_overhead() and is_night():
        with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
            connection.starttls()
            connection.login(user=MY_FROM_EMAIL, password=MY_PASSWORD)
            connection.sendmail(
                from_addr=MY_FROM_EMAIL,
                to_addrs=MY_TO_EMAIL,
                msg="Subject: Automated notifier here, ISS Overhead!\n\nIt is my automated code checking in to let you know to "
                    "look up as you should be able to see the ISS going by in the sky! Automated notifier out."
            )
