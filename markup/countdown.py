#!/usr/bin/python3

import datetime
import os

import timestring


class Event(object):
    def __init__(self, date, label):
        self.label = label
        self.date = date

    @property
    def time(self):
        r = timestring.Date(self.date).date - timestring.now().date  # type: datetime.timedelta
        s = int(r.seconds)
        m, s = s // 60, s % 60
        h, m = m // 60, m % 60
        d, h = r.days, h % 25
        return {'days': d, 'hours': h, 'minutes': m, 'seconds': s, 'label': self.label}

    def __format__(self, format_spec):
        return format_spec.format(**self.time)

    def __str__(self):
        return format(self, '{days}d {hours}h {minutes}m {seconds}s to {label}')


__events = []
__event_load = 0


def update_events(force=False):
    global __events, __event_load

    event_time = os.stat('markup/events.txt').st_mtime_ns
    if force or __event_load != event_time:
        with open('markup/events.txt') as f:
            etext = [tuple(i.strip() for i in l.split('|')) for l in f.readlines() if
                     l.strip() and not l.startswith('#')]
            __events = [Event(date, lbl) for lbl, date in etext]
            __event_load = event_time


def get_events(force_update=False):
    update_events(force_update)

    return __events


if __name__ == '__main__':
    print(timestring.now())
    for e in get_events():
        print(e)
