from pico2d import *

import game_framework
import game_world

projectile = None


class MegaBuster:
    l = [546, 559]
    t = [488, 488]
    w = [9, 10]
    h = [7, 7]
    for i in range(len(t)):
        t[i] += h[i]

    def __init__(self, x, y, dir):
        self.img = projectile
        self.x, self.y = x, y
        self.speed = 10 * dir
        self.dir = dir
        self.frame = 0
        self.size = 2
    def draw(self):
        if self.dir == 1:
            self.img.clip_draw(MegaBuster.l[self.frame], self.img.h - MegaBuster.t[self.frame],
                               MegaBuster.w[self.frame], MegaBuster.h[self.frame],
                               self.x + MegaBuster.w[self.frame] * self.size // 2, self.y + 5,
                               MegaBuster.w[self.frame] * self.size, MegaBuster.h[self.frame] * self.size)
        else:
            self.img.clip_composite_draw(MegaBuster.l[self.frame], self.img.h - MegaBuster.t[self.frame],
                                         MegaBuster.w[self.frame], MegaBuster.h[self.frame],
                                         0, 'h',
                                         self.x - MegaBuster.w[self.frame] * self.size // 2, self.y + 5,
                                         MegaBuster.w[self.frame] * self.size, MegaBuster.h[self.frame] * self.size)

    def update(self):
        self.frame = (self.frame + 1) % len(MegaBuster.l)
        self.x += self.speed * game_world.PIXEL_PER_METER * game_framework.frame_time
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

    def update(self):
        self.frame = (self.frame + 1) % len(MegaTornado.l)
        self.x += self.speed * game_world.time_slice
        if self.x > 800 - 50 or self.x < 0 + 50:
            game_world.erase_obj(self)


class ChargeShot:
    l = [415, 444, 693]
    t = [283, 274, 273]
    w = [23, 35, 94]
    h = [23, 42, 40]

    for i in range(len(t)):
        t[i] += h[i]

    def __init__(self, x, y, dir):
        self.img = projectile
        self.x, self.y = x, y
        self.speed = 10 * dir
        self.dir = dir
        self.frame = 2
        self.size = 1

    def draw(self):
        if self.dir == 1:
            self.img.clip_draw(ChargeShot.l[self.frame], self.img.h - ChargeShot.t[self.frame],
                               ChargeShot.w[self.frame], ChargeShot.h[self.frame],
                               self.x + ChargeShot.w[self.frame] * self.size // 2, self.y + 5,
                               ChargeShot.w[self.frame] * self.size, ChargeShot.h[self.frame] * self.size)
        else:
            self.img.clip_composite_draw(ChargeShot.l[self.frame], self.img.h - ChargeShot.t[self.frame],
                                         ChargeShot.w[self.frame], ChargeShot.h[self.frame],
                                         0, 'h',
                                         self.x - ChargeShot.w[self.frame] * self.size // 2, self.y + 5,
                                         ChargeShot.w[self.frame] * self.size, ChargeShot.h[self.frame] * self.size)

    def update(self):
        self.x += self.speed * game_world.PIXEL_PER_METER * game_framework.frame_time
        if self.x > 800 - 50 or self.x < 0 + 50:
            game_world.erase_obj(self)
