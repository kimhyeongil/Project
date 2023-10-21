from pico2d import *

import game_world


class MegaBuster:
    img = None
    l = [546, 559]
    t = [488, 488]
    w = [9, 10]
    h = [7, 7]
    for i in range(len(t)):
        t[i] += h[i]

    def __init__(self, x, y):
        if MegaBuster.img == None:
            MegaBuster.img = load_image('megamen.png')
        self.x, self.y = x, y
        self.speed = 10
        self.frame = 0

    def draw(self):
        MegaBuster.img.clip_draw(MegaBuster.l[self.frame], MegaBuster.img.h - MegaBuster.t[self.frame],
                                 MegaBuster.w[self.frame], MegaBuster.h[self.frame],
                                 self.x, self.y, MegaBuster.w[self.frame] * 2, MegaBuster.h[self.frame] * 2)

    def update(self):
        self.frame = (self.frame + 1) % len(MegaBuster.l)
        self.x += self.speed
        if self.x > 800 - 50 or self.x < 0 + 50:
            game_world.erase_obj(self)
