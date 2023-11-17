import time

from pico2d import *

import game_framework
import game_world
import player1_control
import player2_control
from ground import Ground

projectile = None


class MegaBuster:
    frame = [(546, 1439, 9, 7,),
             (559, 1439, 10, 7,), ]
    FRAME_PER_SEC = 5
    nFrame = 2
    damage = 1
    rigid_coefficient = 0.5

    def __init__(self, x, y, dir):
        self.img = projectile
        self.x, self.y = x, y
        self.speed = 10 * dir
        self.dir = dir
        self.frame = 0
        self.size = 2
        game_world.add_obj(self, 1)

    def draw(self):
        frame = int(self.frame)
        if self.dir == 1:
            self.img.clip_draw(*MegaBuster.frame[frame],
                               self.x, self.y,
                               MegaBuster.frame[frame][2] * self.size, MegaBuster.frame[frame][3] * self.size)
        else:
            self.img.clip_composite_draw(*MegaBuster.frame[frame],
                                         0, 'h',
                                         self.x, self.y,
                                         MegaBuster.frame[frame][2] * self.size, MegaBuster.frame[frame][3] * self.size)
        draw_rectangle(*self.get_bb())

    def update(self):
        self.frame = (self.frame + game_framework.frame_time * MegaBuster.FRAME_PER_SEC) % MegaBuster.nFrame
        self.x += self.speed * game_world.PIXEL_PER_METER * game_framework.frame_time
        if self.x > 800 - 50 or self.x < 0 + 50:
            game_world.erase_obj(self)

    def get_bb(self):
        frame = int(self.frame)
        return self.x - MegaBuster.frame[frame][2] * self.size // 2, self.y - MegaBuster.frame[frame][
            3] * self.size // 2, self.x + MegaBuster.frame[frame][2] * self.size // 2, self.y + MegaBuster.frame[frame][
                   3] * self.size // 2

    def handle_collision(self, group, other):
        if other.control_method.isHit(group):
            other.hit(self.damage, self.rigid_coefficient)
            game_world.erase_obj(self)


class MegaTornado:
    frame = [(534, 141, 71, 58,),
             (613, 136, 72, 66,),
             (697, 143, 66, 59,), ]
    nFrame = 3
    FRAME_PER_SEC = 18
    damage = 1
    rigid_coefficient = 0.01

    def __init__(self, x, y, speed):
        self.img = projectile
        self.x, self.y = x, y
        self.speed = speed
        self.frame = 0
        self.size = 1.5
        self.cooltime = 0
        game_world.add_obj(self, 0)

    def draw(self):
        frame = int(self.frame)
        self.img.clip_draw(*MegaTornado.frame[frame],
                           self.x, self.y, MegaTornado.frame[frame][2] * self.size,
                           MegaTornado.frame[frame][3] * self.size)
        draw_rectangle(*self.get_bb())

    def update(self):
        self.frame = (self.frame + game_framework.frame_time * MegaTornado.FRAME_PER_SEC) % MegaTornado.nFrame
        self.x += self.speed * game_world.PIXEL_PER_METER * game_framework.frame_time
        if self.x > 800 - 50 or self.x < 0 + 50:
            game_world.erase_obj(self)

    def get_bb(self):
        frame = int(self.frame)
        return self.x - MegaTornado.frame[frame][2] * self.size // 2, self.y - MegaTornado.frame[frame][
            3] * self.size // 2, self.x + MegaTornado.frame[frame][2] * self.size // 2, self.y + \
               MegaTornado.frame[frame][
                   3] * self.size // 2

    def handle_collision(self, group, other):
        cur_time = time.time()
        if other.control_method.isHit(group) and cur_time - self.cooltime >= 0.05:
            other.hit(self.damage, self.rigid_coefficient)
            self.cooltime = cur_time


class MegaChargingShot:
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
        self.frame = MegaChargingShot.nFrame - 1
        self.size = 1
        self.damage = 0
        self.rigid_coefficient = 0
        game_world.add_obj(self, 1)

    def draw(self):
        frame = self.frame
        if self.dir == 1:
            self.img.clip_draw(*MegaChargingShot.frame[frame],
                               self.x, self.y,
                               MegaChargingShot.frame[frame][2] * self.size,
                               MegaChargingShot.frame[frame][3] * self.size)
        else:
            self.img.clip_composite_draw(*MegaChargingShot.frame[frame],
                                         0, 'h',
                                         self.x, self.y,
                                         MegaChargingShot.frame[frame][2] * self.size,
                                         MegaChargingShot.frame[frame][3] * self.size)
        draw_rectangle(*self.get_bb())

    def update(self):
        self.x += self.speed * game_world.PIXEL_PER_METER * game_framework.frame_time
        if self.x > 800 - 50 or self.x < 0 + 50:
            game_world.erase_obj(self)

    def get_bb(self):
        frame = int(self.frame)
        return self.x - MegaChargingShot.frame[frame][2] * self.size // 2, self.y - MegaChargingShot.frame[frame][
            3] * self.size // 2, self.x + MegaChargingShot.frame[frame][2] * self.size // 2, self.y + \
               MegaChargingShot.frame[frame][
                   3] * self.size // 2

    def handle_collision(self, group, other):
        if other.control_method.isHit(group):
            other.hit(self.damage, self.rigid_coefficient)
            game_world.erase_obj(self)


class MegaHurricane:
    frame = [(292, 394, 38, 36,),
             (336, 393, 35, 37,),
             (379, 393, 35, 37,), ]
    FRAME_PER_SEC = 6
    nFrame = 3
    damage = 1
    rigid_coefficient = 0.1

    def __init__(self, megamen):
        self.img = projectile
        self.x, self.y = megamen.x, megamen.y + megamen.state_machine.state.frame[int(megamen.frame)][3] * megamen.size
        self.megamen = megamen
        self.size = 2
        self.frame = 0
        self.cooltime = 0
        game_world.add_obj(self, 1)

    def draw(self):
        frame = int(self.frame)
        self.img.clip_draw(
            *MegaHurricane.frame[frame],
            self.x,
            self.y + MegaHurricane.frame[frame][3] * self.size // 2,
            MegaHurricane.frame[frame][2] * self.size,
            MegaHurricane.frame[frame][3] * self.size
        )
        draw_rectangle(*self.get_bb())

    def update(self):
        self.frame = (self.frame + game_framework.frame_time * MegaHurricane.FRAME_PER_SEC) % MegaBuster.nFrame
        megamen = self.megamen
        self.x = megamen.x
        self.y = megamen.y + megamen.state_machine.state.frame[int(megamen.frame)][3] * megamen.size

    def get_bb(self):
        frame = int(self.frame)
        return self.x - MegaChargingShot.frame[frame][2] * self.size // 2, self.y + MegaHurricane.frame[frame][
            3] * self.size // 2 - MegaChargingShot.frame[frame][
                   3] * self.size // 2, self.x + MegaChargingShot.frame[frame][2] * self.size // 2, self.y + \
               MegaHurricane.frame[frame][3] * self.size // 2 + \
               MegaChargingShot.frame[frame][
                   3] * self.size // 2

    def handle_collision(self, group, other):
        cur_time = time.time()
        if other.control_method.isHit(group) and cur_time - self.cooltime >= 0.1:
            other.hit(self.damage, self.rigid_coefficient)
            self.cooltime = cur_time


class MegaKnuckle:
    frame = [(340, 326, 10, 15,), ]
    damage = 5
    rigid_coefficient = 2

    def __init__(self, x, y, size):
        self.img = projectile
        self.x, self.y = x, y
        self.dir = 0
        self.frame = 0
        self.size = size
        self.speed = 0
        game_world.add_obj(self, 1)
        game_world.add_collision_pair("knuckle:ground", self, None)

    def draw(self):
        frame = self.frame
        self.img.clip_draw(*MegaKnuckle.frame[0],
                           self.x, self.y,
                           MegaKnuckle.frame[0][2] * self.size, MegaKnuckle.frame[0][3] * self.size)
        draw_rectangle(*self.get_bb())

    def update(self):
        self.y += self.speed * game_world.PIXEL_PER_METER * game_framework.frame_time
        self.speed -= game_framework.frame_time * game_world.g

    def get_bb(self):
        return self.x - MegaKnuckle.frame[0][2] * self.size // 2, self.y - MegaKnuckle.frame[0][
            3] * self.size // 2, self.x + MegaKnuckle.frame[0][2] * self.size // 2, self.y + \
               MegaKnuckle.frame[0][3] * self.size

    def handle_collision(self, group, other):
        print(group)
        if group == "knuckle:ground":
            game_world.erase_obj(self)
        elif other.control_method.isHit(group):
            other.hit(self.damage, self.rigid_coefficient)
            game_world.erase_obj(self)


class MegaCogwheel:
    frame = [(307, 571, 20, 20,),
             (332, 571, 20, 20,), ]
    FRAME_PER_SEC = 12
    nFrame = 2
    damage = 15
    rigid_coefficient = 4

    def __init__(self, x, y, dir):
        self.img = projectile
        self.x, self.y = x, y
        self.speed = 10 * dir
        self.dir = dir
        self.frame = 0
        self.size = 2
        game_world.add_obj(self, 1)

    def draw(self):
        frame = int(self.frame)
        if self.dir == 1:
            self.img.clip_draw(*MegaCogwheel.frame[frame],
                               self.x, self.y,
                               MegaCogwheel.frame[frame][2] * self.size, MegaCogwheel.frame[frame][3] * self.size)
        else:
            self.img.clip_composite_draw(*MegaCogwheel.frame[frame],
                                         0, 'h',
                                         self.x, self.y,
                                         MegaCogwheel.frame[frame][2] * self.size,
                                         MegaCogwheel.frame[frame][3] * self.size)
        draw_rectangle(*self.get_bb())

    def update(self):
        self.frame = (self.frame + game_framework.frame_time * MegaCogwheel.FRAME_PER_SEC) % MegaCogwheel.nFrame
        self.x += self.speed * game_world.PIXEL_PER_METER * game_framework.frame_time
        if self.x > 800 - 50 or self.x < 0 + 50:
            game_world.erase_obj(self)

    def get_bb(self):
        frame = int(self.frame)
        return self.x - MegaCogwheel.frame[frame][2] * self.size // 2, self.y - MegaCogwheel.frame[frame][
            3] * self.size // 2, self.x + MegaCogwheel.frame[frame][2] * self.size // 2, self.y + \
               MegaCogwheel.frame[frame][
                   3] * self.size // 2

    def handle_collision(self, group, other):
        if other.control_method.isHit(group):
            other.hit(self.damage, self.rigid_coefficient)
            game_world.erase_obj(self)
