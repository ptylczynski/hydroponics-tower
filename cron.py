import datetime
import socket

import requests
import objects
import os


def _should_apply_state(day: objects.CronDay):
    today_hour = datetime.datetime.now().hour
    today_minute = datetime.datetime.now().minute
    return (today_hour >= day.start_hour and today_hour < day.end_hour) \
        or (today_hour == day.start_hour and today_minute >= day.start_minute) \
        or (today_hour == day.end_hour and today_minute < day.end_minute)


def _apply_state(light: objects.Light, day: objects.CronDay):
    if day.state_to_be_set:
        light.turn_on()
        print(f"Turned on {light.name}")
    else:
        light.turn_off()
        print(f"Turned off {light.name}")

def _revert_state(light: objects.Light, day: objects.CronDay):
    if day.state_to_be_set:
        light.turn_off()
        print(f"Turned off {light.name}")
    else:
        light.turn_on()
        print(f"Turned on {light.name}")

def _update_lights():
    print("Updating lights...")
    lights = objects.create_or_load_lights()
    today_day_no = datetime.datetime.now().weekday()
    for light in lights:
        for day in light.cron_days:
            if day.day_no == today_day_no and day.enabled:
                if _should_apply_state(day):
                    _apply_state(light, day)
                else:
                    _revert_state(light, day)

    objects.save(lights)

def _update_address():
    print("Updating ip in DDNS...")
    token = os.environ.get("DDNS_TOKEN")
    secret_token = os.environ.get("DDNS_SECRET")
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
        response = requests.put(
            f"https://ddns.ptl.cloud/register/{token}/",
            json={"ip": f"{ip}:{port}", "secret_token": secret_token}
        ).json()
        print(f"DDNS response: {response}")
    else:
        print("DDNS_TOKEN or IP or PORT not found")

def run():
    _update_lights()
    _update_address()

run()

