from datetime import datetime

import pygame

from countdown import get_events
from panel import Panel
from wxget import get_weather

pygame.font.init()

WHITE = (255, 255, 255)
GRAY = (175, 175, 175)
BLACK = (0, 0, 0)


class Font(object):
    def __init__(self, name):
        self.file = name
        self.fonts = {}

    def __getitem__(self, size):
        if size not in self.fonts:
            self.fonts[size] = pygame.font.Font(self.file, size)
        return self.fonts[size]


roboto = Font('res/RobotoSlab-Regular.ttf')


def __do_eval(text):
    try:
        return eval(text)
    except:
        return text


def text(size=60, t="", do_eval=False):
    if do_eval:
        t = __do_eval(t)
    return roboto[size].render(t, True, WHITE)


def time(size=60, fmt='%I:%H', strip='0'):
    return roboto[size].render(format(datetime.now(), fmt).lstrip(strip), True, WHITE)


def weather(size=60, fmt='{current_conditions.temperature}\u00b0'):
    return roboto[size].render(fmt.format(**get_weather()), True, WHITE)


def image(path="", do_eval=False):
    if do_eval:
        path = __do_eval(path)
    try:
        return pygame.image.load(path)
    except:
        return text(size=15, t=path)


def header():
    es = get_events()

    def item(i):
        f = roboto[30]
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
