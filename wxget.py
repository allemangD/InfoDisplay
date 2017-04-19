#!/usr/bin/python3
from datetime import datetime

import pywapi
import timestring

LOCATION = '28223'
UNITS = 'imperial'

UPDATE_INTERVAL = 60 * 20

__weather = {}


class AttrDict(dict):
    """ Dictionary subclass whose entries can be accessed by attributes
        (as well as normally).
    """

    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self

    @staticmethod
    def from_nested_dict(data):
        """ Construct nested AttrDicts from nested dictionaries. """
        if not isinstance(data, dict):
            return data
        else:
            return AttrDict({key: AttrDict.from_nested_dict(data[key])
                             for key in data})


def update_weather(force=False):
    global __weather
    now = datetime.now()
    last_check = timestring.Date(__weather.get('current_conditions', {}).get('last_checked', now)).date

    interval = (now - last_check).total_seconds()

    if force or interval <= 0 or interval > UPDATE_INTERVAL:
        __weather = pywapi.get_weather_from_weather_com(LOCATION, UNITS)
        __weather.setdefault('current_conditions', {}).setdefault('last_checked', str(now))
        __weather = AttrDict.from_nested_dict(__weather)
        print('updated weather at', now)


def get_weather(force_update=False):
    update_weather(force_update)

    return __weather


if __name__ == '__main__':
    while True:
        print('{current_conditions.temperature}\u00b0{units.temperature}'.format(**get_weather()))
