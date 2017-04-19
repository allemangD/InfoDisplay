#!/usr/bin/python3
from datetime import datetime

import pywapi
import timestring

LOCATION = '28223'
UNITS = 'imperial'

UPDATE_INTERVAL = 60 * 20

__weather = {}


def update_weather(force=False):
    global __weather
    now = datetime.now()
    last_check = timestring.Date(__weather.get('current_conditions', {}).get('last_checked', now)).date

    interval = (now - last_check).total_seconds()

    if force or interval <= 0 or interval > UPDATE_INTERVAL:
        __weather = pywapi.get_weather_from_weather_com(LOCATION, UNITS)
        __weather.setdefault('current_conditions', {}).setdefault('last_checked', str(now))
        print('updated weather at', now)


def get_weather(force_update=False):
    update_weather(force_update)

    return __weather


if __name__ == '__main__':
    while True:
        print('{0[current_conditions][temperature]}\u00b0{0[units][temperature]}'.format(get_weather()))
