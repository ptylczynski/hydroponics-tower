import time

import schedule
from gpiozero import LED

import objects

gpio_state = dict()

def _create_gpio(pin_no: int):
    try:
        if pin_no not in gpio_state:
            gpio_state[pin_no] = LED(pin_no, active_high=False)
    except Exception as e:
        print(e)
        print("GPIO is disabled now!")
        return None

def _update_gpio():
    print("Updating GPIO...")
    for l in objects.create_or_load_lights():
        pin_no = l.pin_no
        state = l.state
        name = l.name
        _create_gpio(pin_no)
        print(f"Setting pin {pin_no} to {state}")
        if pin_no in gpio_state and gpio_state[pin_no]:
            if state:
                gpio_state[pin_no].on()
            elif not state:
                gpio_state[pin_no].off()
        else:
            print(f"No GPIO is set! Not changing state of light {name}")

_update_gpio()

while True:
    # have to be done this way as crontab has granularity of 1 minute
    _update_gpio()
    time.sleep(10)