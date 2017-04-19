import importlib
import json
import os
import re

import pygame


class Panel(object):
    def __init__(self, surf, position=None, anchor=None, pivot=None, children=None, args=None):
        if isinstance(surf, tuple) or not surf:
            self.__surf = pygame.Surface(surf or (0, 0), flags=pygame.SRCALPHA)
        else:
            self.__surf = surf

        self.position = position or (0, 0)
        self.anchor = anchor or (0, 0)
        self.pivot = pivot or self.anchor
        self.children = children or []
        self.args = args or {}

    @property
    def size(self):
        surf = self.__surf

        if callable(surf):
            surf = surf(**self.args)
        if isinstance(surf, Panel):
            return surf.size

        return surf.get_width(), surf.get_height()

    @property
    def surf(self):
        surf = self.__surf

        if callable(surf):
            surf = surf(**self.args)
        elif isinstance(surf, Panel):
            surf = surf.surf
        else:
            surf = surf.copy()

        for child in self.children:
            c_surf = child
            position = (0, 0)

            if isinstance(child, Panel):
                c_surf = child.surf

                position = tuple(int(a * s - v * c + p) for a, v, s, c, p in
                                 zip(child.anchor, child.pivot, self.size, child.size, child.position))

            surf.blit(c_surf, position)

        return surf


old_modules = {}


def load(file):
    loaded_modules = {}

    fp = file
    directory, file = os.path.split(file)

    def ordered_pair(s, dtype=float):
        if not s:
            return None

        try:
            op = tuple(dtype(c) for c in (re.split(r'\s*[,x\s]\s*', s)))
        except ValueError:
            return None

        if len(op) != 2:
            return None

        return op

    def script(s):
        if not s:
            return None

        pair = re.split(r'::', s)

        if len(pair) != 2:
            return None

        mod, func = pair

        mname = directory.replace('/', '.') + '.' + mod

        if mod not in loaded_modules:
            if mod in old_modules:
                importlib.reload(old_modules[mod])

            try:
                loaded_modules[mod] = importlib.import_module(mname)
            except ModuleNotFoundError:
                return None

        mod = loaded_modules[mod]

        try:
            func = getattr(mod, func)
        except AttributeError:
            return None

        return func

    def from_dict(d: dict):
        surf = d.get('surf', None)
        position = d.get('position', None)
        anchor = d.get('anchor', None)
        pivot = d.get('pivot', None)
        children = d.get('children', [])
        args = d.get('args', {})

        surf = ordered_pair(surf, int) or script(surf)
        position = ordered_pair(position, int)
        anchor = ordered_pair(anchor)
        pivot = ordered_pair(pivot)
        children = [from_dict(d) for d in children]

        return Panel(surf, position, anchor, pivot, children, args)

    with open(fp) as f:
        j = json.load(f)
        if isinstance(j, list):
            ls = [from_dict(d) for d in j]
        else:
            ls = [from_dict(j)]

        old_modules.clear()
        for k, v in loaded_modules.items():
            old_modules[k] = v

        return ls


if __name__ == '__main__':
    print(load('clock.json'))
