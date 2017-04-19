#!/usr/bin/python3
import os
import sys

import pygame

import panel

CONFIG_PATH = sys.argv[1]
print(CONFIG_PATH)

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
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        panel_time = os.stat(CONFIG_PATH).st_mtime_ns
        if panel_time != panel_load:
            parent = panel.Panel(SIZE, children=panel.load(CONFIG_PATH))
            panel_load = panel_time

        mode.blit(parent.surf, (0, 0))

        pygame.display.update()
        clock.tick(8)


game_loop()
