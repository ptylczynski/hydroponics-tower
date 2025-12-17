import os
import pickle
from typing import List, Optional

import yaml

def create_or_load_lights():
    if os.path.exists("lights.pkl"):
        with open("lights.pkl", "rb") as f:
            lights = pickle.load(f)
    else:
        with open('config.yaml', 'r') as f:
            data = yaml.load(f, Loader=yaml.SafeLoader)
            lights_defaults = data["lights"]
        lights = [Light(False, [], light["name"], light["pin_no"]) for light in lights_defaults]
        with open("lights.pkl", "wb") as f:
            pickle.dump(lights, f)
    return lights

class CronDay:
    def __init__(self, day_no: int, start_hour: int, start_minute: int, end_hour: int, end_minute: int, enabled: bool, state_to_be_set: bool):
        self.day_no = day_no
        self.start_hour = start_hour
        self.start_minute = start_minute
        self.end_hour = end_hour
        self.end_minute = end_minute
        self.enabled = enabled
        self.state_to_be_set = state_to_be_set


class Light:
    def __init__(self, state: bool, cron_days: List[CronDay], name: str, pin_no: int):
        self.state = state
        self.icon = ":material/lightbulb:" if self.state else ":material/light_off:"
        self.cron_days = cron_days
        self.name = name
        self.pin_no = pin_no

    def switch(self):
        self.state = not self.state
        self.icon = ":material/lightbulb:" if self.state else ":material/light_off:"

    def turn_on(self):
        if not self.state:
            self.state = True
            self.icon = ":material/lightbulb:"

    def turn_off(self):
        if self.state:
            self.state = False
            self.icon = ":material/light_off:"


def save(lights: List[Light]):
    with open("lights.pkl", "wb") as f:
        pickle.dump(lights, f)
