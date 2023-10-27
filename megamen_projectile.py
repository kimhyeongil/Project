from pico2d import *

import game_world

projectile = None


class MegaBuster:
    l = [546, 559]
    t = [488, 488]
    w = [9, 10]
    h = [7, 7]
    for i in range(len(t)):
        t[i] += h[i]

    def __init__(self, x, y):
        self.img = projectile
        self.x, self.y = x, y
        self.speed = 10
        self.frame = 0

    def draw(self):
        self.img.clip_draw(MegaBuster.l[self.frame], self.img.h - MegaBuster.t[self.frame],
                           MegaBuster.w[self.frame], MegaBuster.h[self.frame],
                           self.x, self.y, MegaBuster.w[self.frame] * 2, MegaBuster.h[self.frame] * 2)

    def update(self):
        self.frame = (self.frame + 1) % len(MegaBuster.l)
        self.x += self.speed
        if self.x > 800 - 50 or self.x < 0 + 50:
            game_world.erase_obj(self)


class MegaTornado:
    l = [534, 613, 697]
    t = [1735, 1732, 1732]
    w = [71, 72, 66]
    h = [58, 66, 59]

    for i in range(len(t)):
        t[i] += h[i]

    def __init__(self, x, y, speed):
        self.img = projectile
        self.x, self.y = x, y
        self.speed = speed
        self.frame = 0

    def draw(self):
        self.img.clip_draw(MegaTornado.l[self.frame], self.img.h - MegaTornado.t[self.frame],
                           MegaTornado.w[self.frame], MegaTornado.h[self.frame],
                           self.x, self.y, MegaTornado.w[self.frame] * 2, MegaTornado.h[self.frame] * 2)
        print("tornado")

    def update(self):
        self.frame = (self.frame + 1) % len(MegaTornado.l)
        self.x += self.speed * game_world.time_slice
        print("tornado update")
        if self.x > 800 - 50 or self.x < 0 + 50:
            game_world.erase_obj(self)
