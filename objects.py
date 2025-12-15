import os
import pickle
from typing import List, Optional
from gpiozero import LED

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
    def __init__(self, day_no: int, start_hour: int, start_minute: int, end_hour: int, end_minute: int, enabled: bool):
        self.day_no = day_no
        self.start_hour = start_hour
        self.start_minute = start_minute
        self.end_hour = end_hour
        self.end_minute = end_minute
        self.enabled = enabled


class Light:
    def __init__(self, state: bool, cron_days: List[CronDay], name: str, pin_no: int):
        self.state = state
        self.icon = ":material/lightbulb:" if self.state else ":material/light_off:"
        self.cron_days = cron_days
        self.name = name
        self.pin_no = pin_no
        self.gpio = self._create_gpio()
        self._update_gpio()

    def switch(self):
        self.state = not self.state
        self.icon = ":material/lightbulb:" if self.state else ":material/light_off:"
        self._update_gpio()

    def turn_on(self):
        if not self.state:
            self.state = True
            self.icon = ":material/lightbulb:"
            self._update_gpio()

    def turn_off(self):
        if self.state:
            self.state = False
            self.icon = ":material/light_off:"
            self._update_gpio()

    def _create_gpio(self):
        try:
            return LED(self.pin_no)
        except Exception as e:
            print(e)
            print("GPIO is disabled now!")
            return None

    def _update_gpio(self):
        if self.gpio:
            if self.state:
                self.gpio.on()
            else:
                self.gpio.off()
        else:
            print(f"No GPIO is set! Not changing state of light {self.name}")


def save(lights: List[Light]):
    with open("lights.pkl", "wb") as f:
        pickle.dump(lights, f)