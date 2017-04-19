#!/usr/bin/python3
import os

import pygame

import countdown
import panel
import wxget

CONFIG_PATH = 'clock.json'

pygame.init()

pygame.mouse.set_visible(False)

SIZE = (1280, 1024)
mode = pygame.display.set_mode(SIZE, 1)
pygame.display.set_caption("weather clock")
clock = pygame.time.Clock()


def game_loop():
    panel_load = None
    parent = None

    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()
                if event.key == pygame.K_r:
                    wxget.update_weather(True)
                    countdown.update_events(True)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        panel_time = os.stat(CONFIG_PATH).st_mtime_ns
        if panel_time != panel_load:
            parent = panel.Panel(SIZE, children=panel.load(CONFIG_PATH))
            panel_load = panel_time

        wxget.update_weather()
        mode.fill((0, 0, 0))
        mode.blit(parent.surf, (0, 0))
        pygame.display.update()

        clock.tick(8)

        # weather = wxget.__weather
        #
        # if iconName != weather['current_conditions']['icon']:
        #     iconName = str(int(weather['current_conditions']['icon']))
        #     icon = pygame.image.load('res/png/' + iconName + '.png')
        #
        # temp = '{0[current_conditions][temperature]}\u00b0{0[units][temperature]}'.format(wxget.get_weather())
        # temp = font60.render(temp, True, WHITE)
        # feels_like = 'Feels like ' + weather['current_conditions']['feels_like']
        # feels_like = font45.render(feels_like, True, GRAY)
        # lastupdate = Date(weather['current_conditions']['last_updated']).format('Last updated %I:%M')
        # lastupdate = font30.render(lastupdate, True, GRAY)
        #
        # status = join_horizontal(icon, join_vertical(temp, feels_like, 10, TOP_LEFT, BOTTOM_LEFT), 0)
        # status = join_vertical(status, lastupdate, 10)
        #
        # draw_surf(status, (0, -30), BOTTOM_CENTER, BOTTOM_CENTER)
        #
        # now = datetime.now()
        # time = now.strftime('%I:%M')
        # time = font360.render(time, True, WHITE)
        # date = now.strftime('%A, %B %d')
        # date = font60.render(date, True, GRAY)
        #
        # time = join_vertical(time, date, -100)
        #
        # draw_surf(time, ZERO, CENTER, (0.5, 0.4))
        #
        # event_surfs = []
        # events = countdown.events
        #
        # for e in events:
        #     elbl = font45.render(e.label, True, WHITE)
        #     etime = font30.render(format(e, '{days}d {hours}h {minutes}m'), True, GRAY)
        #     event = join_vertical(elbl, etime, 5)
        #     event_surfs.append(event)
        #
        # timer = pygame.Surface((0, 0))
        # max_w = max((e.get_width() for e in event_surfs))
        # for es in event_surfs:
        #     timer = join_horizontal(timer, join_vertical(es, pygame.Surface((max_w, 1)), -1), 15)
        #
        # draw_surf(timer, ZERO, TOP_CENTER, TOP_CENTER)
        #
        # bells.play_chime(now.hour, now.minute)


game_loop()
