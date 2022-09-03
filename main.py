import requests
import datetime
import smtplib
import time

MY_LAT = 45.815010
MY_LONG = 15.981919
MY_EMAIL = "martin.pytest@yahoo.com"
MY_PASSWORD = "peemwvunfxvcsmzs"
MY_EMAIL_SMTP = "smtp.mail.yahoo.com"
SMTP_PORT = 587
SLEEP_TIME = 60


def get_hour_now():
    return datetime.datetime.now().hour


def get_sunrise_sunset_hours():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0
    }
    response = requests.get(url="https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    return int(data["results"]["sunrise"].split("T")[1].split(":")[0]), int(data["results"]["sunset"].split("T")[1].split(":")[0])


def is_night():
    return hour_now in range(0, (hour_sunrise + 1)) or hour_now in range(hour_sunset, 24)


def get_iss_position():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()
    return float(data["iss_position"]["latitude"]), float(data["iss_position"]["longitude"])


def iss_is_above(lat, lng):
    return (MY_LAT - 5) < lat < (MY_LAT + 5) and (MY_LONG - 5) < lng < (MY_LONG + 5)


def send_email(destination_email):
    with smtplib.SMTP(MY_EMAIL_SMTP, SMTP_PORT) as connection:
        connection.starttls()
        connection.login(user=MY_EMAIL, password=MY_PASSWORD)
        connection.sendmail(from_addr=MY_EMAIL,
                            to_addrs=destination_email,
                            msg="Subject:Look up!\n\n"
                                "The ISS is above you!")


hour_sunrise, hour_sunset = get_sunrise_sunset_hours()

while True:
    time.sleep(SLEEP_TIME)
    hour_now = get_hour_now()
    if is_night():
        iss_lat, iss_lng = get_iss_position()
        if iss_is_above(iss_lat, iss_lng):
            send_email("martin.petracic@gmail.com")


# This code is supposed to run in the cloud every 60 secs, in that case it has to be slightly modified.
