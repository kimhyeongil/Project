from pico2d import *

import game_framework
import game_world

projectile = None


class MegaBuster:
    frame = [(546, 1439, 9, 7,),
             (559, 1439, 10, 7,), ]
    FRAME_PER_SEC = 5
    nFrame = 2

    def __init__(self, x, y, dir):
        self.img = projectile
        self.x, self.y = x, y
        self.speed = 10 * dir
        self.dir = dir
        self.frame = 0
        self.size = 2

    def draw(self):
        frame = int(self.frame)
        if self.dir == 1:
            self.img.clip_draw(*MegaBuster.frame[frame],
                               self.x + MegaBuster.frame[frame][2] * self.size // 2, self.y + 5,
                               MegaBuster.frame[frame][2] * self.size, MegaBuster.frame[frame][3] * self.size)
        else:
            self.img.clip_composite_draw(*MegaBuster.frame[frame],
                                         0, 'h',
                                         self.x - MegaBuster.frame[frame][2] * self.size // 2, self.y + 5,
                                         MegaBuster.frame[frame][2] * self.size, MegaBuster.frame[frame][3] * self.size)

    def update(self):
        self.frame = (self.frame + game_framework.frame_time * MegaBuster.FRAME_PER_SEC) % MegaBuster.nFrame
        self.x += self.speed * game_world.PIXEL_PER_METER * game_framework.frame_time
        if self.x > 800 - 50 or self.x < 0 + 50:
            game_world.erase_obj(self)


class MegaTornado:
    frame = [(534, 141, 71, 58,),
             (613, 136, 72, 66,),
             (697, 143, 66, 59,), ]
    nFrame = 3
    FRAME_PER_SEC = 18

    def __init__(self, x, y, speed):
        self.img = projectile
        self.x, self.y = x, y
        self.speed = speed
        self.frame = 0

    def draw(self):
        frame = int(self.frame)
        self.img.clip_draw(*MegaTornado.frame[frame],
                           self.x, self.y, MegaTornado.frame[frame][2] * 2, MegaTornado.frame[frame][3] * 2)

    def update(self):
        self.frame = (self.frame + game_framework.frame_time * MegaTornado.FRAME_PER_SEC) % MegaTornado.nFrame
        self.x += self.speed * game_world.PIXEL_PER_METER * game_framework.frame_time
        if self.x > 800 - 50 or self.x < 0 + 50:
            game_world.erase_obj(self)


class ChargeShot:
    frame = [(415, 1628, 23, 23,),
             (444, 1618, 35, 42,),
             (484, 1615, 45, 48,),
             (693, 1621, 94, 40,), ]
    nFrame = 4

    def __init__(self, x, y, dir):
        self.img = projectile
        self.x, self.y = x, y
        self.speed = 10 * dir
        self.dir = dir
        self.frame = ChargeShot.nFrame - 1
        self.size = 1

    def draw(self):
        frame = self.frame
        if self.dir == 1:
            self.img.clip_draw(*ChargeShot.frame[frame],
                               self.x + ChargeShot.frame[frame][2] * self.size // 2, self.y + 5,
                               ChargeShot.frame[frame][2] * self.size, ChargeShot.frame[frame][3] * self.size)
        else:
            self.img.clip_composite_draw(*ChargeShot.frame[frame],
                                         0, 'h',
                                         self.x - ChargeShot.frame[frame][2] * self.size // 2, self.y + 5,
                                         ChargeShot.frame[frame][2] * self.size, ChargeShot.frame[frame][3] * self.size)

    def update(self):
        self.x += self.speed * game_world.PIXEL_PER_METER * game_framework.frame_time
        if self.x > 800 - 50 or self.x < 0 + 50:
            game_world.erase_obj(self)


class MegaHurricane:
    frame = [(292, 394, 38, 36,),
             (336, 393, 35, 37,),
             (379, 393, 35, 37,), ]
    FRAME_PER_SEC = 6
    nFrame = 3

    def __init__(self, x, y):
        self.img = projectile
        self.x, self.y = x, y
        self.size = 2
        self.frame = 0

    def draw(self):
        frame = int(self.frame)
        self.img.clip_draw(
            *MegaHurricane.frame[frame],
            self.x,
            self.y + MegaHurricane.frame[frame][3] * self.size // 2,
            MegaHurricane.frame[frame][2] * self.size,
            MegaHurricane.frame[frame][3] * self.size
        )

    def update(self):
        self.frame = (self.frame + game_framework.frame_time * MegaHurricane.FRAME_PER_SEC) % MegaBuster.nFrame
