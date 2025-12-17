import datetime
import sys
from typing import Optional

import streamlit as st
import pickle
import mock_pyarrow
import os
import schedule
from cron import update_lights

from altair import DateTime

import objects

lights = objects.create_or_load_lights()

default_cron_settings = {
    "start_hour": 10,
    "start_minute": 0,
    "end_hour": 18,
    "end_minute": 0,
}

days = [
    {"name": "Monday", "number": 0},
    {"name": "Tuesday", "number": 1},
    {"name": "Wednesday", "number": 2},
    {"name": "Thursday", "number": 3},
    {"name": "Friday", "number": 4},
    {"name": "Saturday", "number": 5},
    {"name": "Sunday", "number": 6},
]

invalid_day: Optional[objects.CronDay] = None

schedule.every(1).minutes.do(update_lights)

def switch_var(light_no):
    lights[light_no].switch()
    objects.save(lights)


def save_settings():
    with open("cron_settings.pkl", "wb") as f:
        pickle.dump(lights, f)

def is_cron_valid(cron_day: objects.CronDay):
    global invalid_day
    if cron_day.start_hour > cron_day.end_hour:
        invalid_day = cron_day
        return "Start hour must be before end hour"
    if cron_day.start_hour == cron_day.end_hour and cron_day.start_minute >= cron_day.end_minute:
        invalid_day = cron_day
        return "Start minute must be before end minute"
    return None

def create_cron_day_if_missing(day_number: int, light: objects.Light):
    if not any(day["number"] == cron_day.day_no for cron_day in light.cron_days):
        new_cron_day = objects.CronDay(
            day_number,
            default_cron_settings["start_hour"],
            default_cron_settings["start_minute"],
            default_cron_settings["end_hour"],
            default_cron_settings["end_minute"],
            False
        )
        light.cron_days.append(new_cron_day)

st.set_page_config(
    page_title="Light Controls",
    page_icon=":material/lightbulb:",
)
st.header(":material/power: Manual Switch", divider=True)

for idx in range(len(lights)):
    st.button(lights[idx].name, width="stretch", icon=lights[idx].icon, on_click=switch_var, args=[idx])

st.header(":material/calendar_today: Schedule", divider=True)

for day in days:
    day_name = day["name"]
    day_number = day["number"]
    with st.expander(day_name):
        for light in lights:
            create_cron_day_if_missing(day_number, light)
            st.subheader(light.name)
            cron_day = light.cron_days[day_number]
            cron_day.enabled = st.checkbox("Enabled", key=f"{day_name}-{light.name}-enabled", value=cron_day.enabled)
            if cron_day.enabled:
                with st.container(horizontal=True, key=f"start_time-{day_name}-{light.name}"):
                    cron_day.start_hour = st.number_input("Start hour", key=f"{day_name}-{light.name}-start_hour", min_value=0,
                                                 max_value=23, value=cron_day.start_hour)
                    cron_day.start_minute = st.number_input("Start minute", key=f"{day_name}-{light.name}-start_minute", min_value=0,
                                                   max_value=59, value=cron_day.start_minute)
                with st.container(horizontal=True, key=f"end_time-{day_name}-{light.name}"):
                    cron_day.end_hour = st.number_input("End hour", key=f"{day_name}-{light.name}-end_hour", min_value=0, max_value=23, value=cron_day.end_hour)
                    cron_day.end_minute = st.number_input("End minute", key=f"{day_name}-{light.name}-end_minute", min_value=0,
                                                 max_value=59, value=cron_day.end_minute)

                cron_validation_response = is_cron_valid(cron_day)
                if cron_validation_response:
                    st.error(cron_validation_response)

with st.container(horizontal=True, horizontal_alignment="right"):
    if invalid_day:
        st.error(f"Invalid cron day: {days[invalid_day.day_no]['name']}")
    if st.button("Save", disabled=invalid_day is not None):
        st.balloons()
        objects.save(lights)

with st.container(horizontal=True):
    st.badge(f":material/alarm: Server time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    st.badge(f":material/code: Interpreter version {sys.version}")
