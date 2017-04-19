from datetime import datetime

import pygame

from countdown import get_events
from panel import Panel
from wxget import get_weather

pygame.font.init()

WHITE = (255, 255, 255)
GRAY = (175, 175, 175)
BLACK = (0, 0, 0)

font = {
    'RobotoSlab': {
        30: pygame.font.Font("res/RobotoSlab-Regular.ttf", 30),
        45: pygame.font.Font("res/RobotoSlab-Regular.ttf", 45),
        60: pygame.font.Font("res/RobotoSlab-Regular.ttf", 60),
        90: pygame.font.Font("res/RobotoSlab-Regular.ttf", 90),
        360: pygame.font.Font("res/RobotoSlab-Regular.ttf", 360),
    }
}


def time():
    return font['RobotoSlab'][360].render(format(datetime.now(), '%I:%H').lstrip('0'), True, WHITE)


def date():
    return font['RobotoSlab'][60].render(format(datetime.now(), '%A, %B %d'), True, GRAY)


def temperature():
    f = font['RobotoSlab'][90]
    return f.render('{0[current_conditions][temperature]}\u00b0'.format(get_weather()), True, WHITE)


def icon():
    return pygame.image.load('res/png/12.png')


def header():
    es = get_events()

    def item(i):
        f = font['RobotoSlab'][30]
        e = es[i]
        l = e.label
        t = '{days}d {hours}h {minutes}m'.format(**e.time)

        return Panel((1280 // len(es), 70), anchor=((i + 1) / (len(es) + 1), .5), children=[
            Panel(f.render(l, True, WHITE), anchor=(.5, .5), pivot=(.5, .9)),
            Panel(f.render(t, True, GRAY), anchor=(.5, .5), pivot=(.5, .1)),
        ])

    return Panel((1280, 70), anchor=(.5, .5), children=[
        item(i) for i in range(len(get_events()))
    ]).surf
