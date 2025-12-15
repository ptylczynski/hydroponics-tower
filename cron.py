import datetime
import socket

import requests
import objects
import os

lights = objects.create_or_load_lights()

today_day_no = datetime.datetime.now().weekday()
today_hour = datetime.datetime.now().hour
today_minute = datetime.datetime.now().minute

print("Updating lights...")
for light in lights:
    for day in light.cron_days:
        if day.day_no == today_day_no:
            if day.enabled :
                if today_hour >= day.start_hour and today_hour < day.end_hour:
                    light.turn_on()
                    print(f"Turned on {light.name}")
                elif today_hour == day.start_hour and today_minute >= day.start_minute:
                    light.turn_on()
                    print(f"Turned on {light.name}")
                elif today_hour == day.end_hour and today_minute < day.end_minute:
                    light.turn_on()
                    print(f"Turned on {light.name}")
                else:
                    light.turn_off()
                    print(f"Turned off {light.name}")

objects.save(lights)

print("Updating ip in DDNS...")

token = os.environ.get("DDNS_TOKEN")
port = os.environ.get("DDNS_PORT", 8501)
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.settimeout(0)
try:
    # doesn't even have to be reachable
    s.connect(('10.254.254.254', 1))
    ip = s.getsockname()[0]
except Exception:
    ip = '127.0.0.1'
finally:
    s.close()

if token and ip and port:
    response = requests.get(f"https://ddns.ptl.cloud/register/{token}/{ip}:{port}").json()
    print(f"DDNS response: {response}")
else:
    print("DDNS_TOKEN or IP or PORT not found")

