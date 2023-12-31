import time

from pico2d import *

import game_framework
import game_world
import play_server

projectile = None


class Sound:
    def __init__(self, sound_name, volume=20):
        self.sound = load_wav(sound_name)
        self.sound.set_volume(volume)

    def play(self):
        self.sound.repeat_play()


class MegaBuster:
    FRAME_INFO = [(546, 1439, 9, 7,),
                  (559, 1439, 10, 7,), ]
    FRAME_PER_SEC = 5
    nFrame = 2
    ATK_INFO = (1, 0.6, 0, 1)
    shot_sound = None
    atk_sound = None

    def __init__(self, x, y, dir):
        self.img = projectile
        self.x, self.y = x, y
        self.speed = 10 * dir
        self.dir = dir
        self.ATK_INFO = list(MegaBuster.ATK_INFO)
        self.ATK_INFO[3] *= dir
        self.frame = 0
        self.size = get_canvas_height() / 200
        game_world.add_obj(self, 1)
        if MegaBuster.shot_sound == None:
            MegaBuster.shot_sound = load_wav("sound/megabuster.wav")
            MegaBuster.shot_sound.set_volume(10)
            MegaBuster.atk_sound = load_wav("sound/ouch.wav")
            MegaBuster.atk_sound.set_volume(50)
        MegaBuster.shot_sound.play()

    def draw(self):
        frame = int(self.frame)
        if self.dir == 1:
            self.img.clip_draw(*self.FRAME_INFO[frame],
                               self.x, self.y,
                               self.FRAME_INFO[frame][2] * self.size, self.FRAME_INFO[frame][3] * self.size)
        else:
            self.img.clip_composite_draw(*self.FRAME_INFO[frame],
                                         0, 'h',
                                         self.x, self.y,
                                         self.FRAME_INFO[frame][2] * self.size, self.FRAME_INFO[frame][3] * self.size)
        draw_rectangle(*self.get_bb())

    def update(self):
        self.frame = (self.frame + game_framework.frame_time * self.FRAME_PER_SEC) % self.nFrame
        self.x += self.speed * game_world.PIXEL_PER_METER * game_framework.frame_time
        if self.x > get_canvas_width() + 50 or self.x < 0 - 50:
            game_world.erase_obj(self)

    def get_bb(self):
        int_frame = int(self.frame)
        return (self.x - self.FRAME_INFO[int_frame][2] * self.size // 2,
                self.y - self.FRAME_INFO[int_frame][3] * self.size // 2,
                self.x + self.FRAME_INFO[int_frame][2] * self.size // 2,
                self.y + self.FRAME_INFO[int_frame][3] * self.size // 2)

    def handle_collision(self, group, other):
        if other.control_method.isHit(group):
            MegaBuster.atk_sound.play()
            if self.dir > 0:
                other.hit(*self.ATK_INFO, atk_pos=self.get_bb()[0])
            else:
                other.hit(*self.ATK_INFO, atk_pos=self.get_bb()[2])
            if group == "Player1:Player2":
                play_server.player1.ultimate_gage = min(play_server.player1.ultimate_gage + self.ATK_INFO[0] / 50, 3)
            else:
                play_server.player2.ultimate_gage = min(play_server.player2.ultimate_gage + self.ATK_INFO[0] / 50, 3)
            game_world.erase_obj(self)


class MegaTornado:
    FRAME_INFO = [(534, 141, 71, 58,),
                  (613, 136, 72, 66,),
                  (697, 143, 66, 59,), ]
    nFrame = 3
    FRAME_PER_SEC = 18
    ATK_INFO = (1, 0.1)
    wind_sound = None

    def __init__(self, x, y, speed):
        self.img = projectile
        self.x, self.y = x, y
        self.speed = speed
        self.frame = 0
        self.size = 3
        self.cooltime = 0.01
        game_world.add_obj(self, 0)
        if MegaTornado.wind_sound == None:
            MegaTornado.wind_sound = load_wav("sound/wind_atk.wav")
        self.wind_sound.set_volume(50)

    def draw(self):
        int_frame = int(self.frame)
        self.img.clip_draw(*self.FRAME_INFO[int_frame],
                           self.x, self.y,
                           self.FRAME_INFO[int_frame][2] * self.size, self.FRAME_INFO[int_frame][3] * self.size)
        draw_rectangle(*self.get_bb())

    def update(self):
        self.frame = (self.frame + game_framework.frame_time * self.FRAME_PER_SEC) % self.nFrame
        self.x += self.speed * game_world.PIXEL_PER_METER * game_framework.frame_time
        if self.x > get_canvas_width() + 50 or self.x < 0 - 50:
            game_world.erase_obj(self)

    def get_bb(self):
        int_frame = int(self.frame)
        return (self.x - self.FRAME_INFO[int_frame][2] * self.size // 2,
                self.y - self.FRAME_INFO[int_frame][3] * self.size // 2,
                self.x + self.FRAME_INFO[int_frame][2] * self.size // 2,
                self.y + self.FRAME_INFO[int_frame][3] * self.size // 2)

    def handle_collision(self, group, other):
        self.cooltime -= game_framework.frame_time
        if other.control_method.isHit(group) and self.cooltime <= 0:
            self.wind_sound.play()
            other.hit(*self.ATK_INFO,
                      knock_back=-(int(other.x) - int(self.x)) / (abs(int(other.x) - int(self.x)) + 1) * abs(
                          self.speed), atk_pos=self.x)
            if group == "Player1:Player2":
                play_server.player1.ultimate_gage = min(play_server.player1.ultimate_gage + self.ATK_INFO[0] / 50, 3)
            else:
                play_server.player2.ultimate_gage = min(play_server.player2.ultimate_gage + self.ATK_INFO[0] / 50, 3)
            self.cooltime = 0.01


class MegaChargingShot:
    FRAME_INFO = [(415, 1628, 23, 23,),
                  (444, 1618, 35, 42,),
                  (484, 1615, 45, 48,),
                  (693, 1621, 94, 40,), ]
    nFrame = 4
    shot_sound = None
    atk_sound = None

    def __init__(self, x=0, y=0, dir=0, charged_time=0, megamen=None):
        self.img = projectile
        self.frame = 0
        self.size = get_canvas_height() / 200
        self.megamen = None
        self.x, self.y = x, y
        self.frame = MegaChargingShot.nFrame - 1
        self.speed = 10 * dir
        self.dir = dir
        self.size = max(charged_time, 1)
        damage = int(7.5 * charged_time)
        rigid = 0.5 * charged_time
        back = 6 * max(charged_time - 0.5, 0) * dir
        up = 7 * max(charged_time - 0.7, 0)
        self.ATK_INFO = (damage, rigid, up, back)
        if MegaChargingShot.shot_sound == None:
            MegaChargingShot.shot_sound = load_wav("sound/megabuster.wav")
            MegaChargingShot.shot_sound.set_volume(20)
            MegaChargingShot.atk_sound = load_wav("sound/ouch.wav")
            MegaChargingShot.atk_sound.set_volume(50)
        if megamen:
            if megamen.face_dir == "r":
                self.dir = 1
            else:
                self.dir = -1
            self.x = megamen.x + (megamen.state_machine.state.FRAME_INFO[int(megamen.frame)][
                                      2] * megamen.size // 2 + 10) * self.dir
            self.y = megamen.y + megamen.state_machine.state.FRAME_INFO[int(megamen.frame)][3] * megamen.size // 2 + 5
            self.megamen = megamen
        else:
            MegaChargingShot.shot_sound.play()
        self.charging_sound = Sound("sound/charging.wav", 40)
        self.charging_sound.play()
        game_world.add_obj(self, 1)

    def draw(self):
        frame = self.frame
        if self.dir == 1:
            self.img.clip_draw(*self.FRAME_INFO[frame],
                               self.x, self.y,
                               self.FRAME_INFO[frame][2] * self.size,
                               self.FRAME_INFO[frame][3] * self.size)
        else:
            self.img.clip_composite_draw(*self.FRAME_INFO[frame],
                                         0, 'h',
                                         self.x, self.y,
                                         self.FRAME_INFO[frame][2] * self.size,
                                         self.FRAME_INFO[frame][3] * self.size)
        draw_rectangle(*self.get_bb())

    def update(self):
        if self.megamen:
            megamen = self.megamen
            if megamen.face_dir == "r":
                self.dir = 1
            else:
                self.dir = -1
            self.x = megamen.x + (megamen.state_machine.state.FRAME_INFO[int(megamen.frame)][
                                      2] * megamen.size // 2 + 10) * self.dir
            self.y = megamen.y + megamen.state_machine.state.FRAME_INFO[int(megamen.frame)][3] * megamen.size // 2 + 5
        else:
            self.x += self.speed * game_world.PIXEL_PER_METER * game_framework.frame_time
        if self.x > get_canvas_width() + 50 or self.x < 0 - 50:
            game_world.erase_obj(self)

    def get_bb(self):
        frame = int(self.frame)
        if self.speed > 0:
            return (self.x,
                    self.y - self.FRAME_INFO[frame][3] * self.size // 2,
                    self.x + self.FRAME_INFO[frame][2] * self.size // 2,
                    self.y + self.FRAME_INFO[frame][3] * self.size // 2)
        else:
            return (self.x - self.FRAME_INFO[frame][2] * self.size // 2,
                    self.y - self.FRAME_INFO[frame][3] * self.size // 2,
                    self.x,
                    self.y + self.FRAME_INFO[frame][3] * self.size // 2)

    def handle_collision(self, group, other):
        if other.control_method.isHit(group):
            MegaChargingShot.atk_sound.play()
            if self.dir > 0:
                other.hit(*self.ATK_INFO, atk_pos=self.get_bb()[0])
            else:
                other.hit(*self.ATK_INFO, atk_pos=self.get_bb()[2])
            if group == "Player1:Player2":
                play_server.player1.ultimate_gage = min(play_server.player1.ultimate_gage + self.ATK_INFO[0] / 50, 3)
            else:
                play_server.player2.ultimate_gage = min(play_server.player2.ultimate_gage + self.ATK_INFO[0] / 50, 3)
            game_world.erase_obj(self)


class MegaHurricane:
    FRAME_INFO = [(292, 394, 38, 36,),
                  (336, 393, 35, 37,),
                  (379, 393, 35, 37,), ]
    FRAME_PER_SEC = 6
    nFrame = 3
    ATK_INFO = (5, 0.1, 1)
    atk_sound = None

    def __init__(self, megamen):
        self.img = projectile
        self.x, self.y = megamen.x, megamen.y + megamen.state_machine.state.FRAME_INFO[int(megamen.frame)][
            3] * megamen.size
        self.megamen = megamen
        self.size = get_canvas_height() / 200
        self.frame = 0
        self.cooltime = 0
        game_world.add_obj(self, 1)
        if MegaHurricane.atk_sound == None:
            MegaHurricane.atk_sound = load_wav("sound/wind_atk.wav")
            MegaHurricane.atk_sound.set_volume(128)

    def draw(self):
        frame = int(self.frame)
        self.img.clip_draw(
            *self.FRAME_INFO[frame],
            self.x,
            self.y + MegaHurricane.FRAME_INFO[frame][3] * self.size // 2,
            self.FRAME_INFO[frame][2] * self.size,
            self.FRAME_INFO[frame][3] * self.size
        )
        draw_rectangle(*self.get_bb())

    def update(self):
        self.frame = (self.frame + game_framework.frame_time * self.FRAME_PER_SEC) % self.nFrame
        megamen = self.megamen
        self.x = megamen.x
        self.y = megamen.y + megamen.state_machine.state.FRAME_INFO[int(megamen.frame)][3] * megamen.size

    def get_bb(self):
        frame = int(self.frame)
        return (self.x - self.FRAME_INFO[frame][2] * self.size // 2,
                self.y,
                self.x + self.FRAME_INFO[frame][2] * self.size // 2,
                self.y + self.FRAME_INFO[frame][3] * self.size)

    def handle_collision(self, group, other):
        cur_time = time.time()
        if other.control_method.isHit(group) and cur_time - self.cooltime >= 0.1:
            self.atk_sound.play()
            other.hit(*self.ATK_INFO, atk_pos=self.x)
            if group == "Player1:Player2":
                play_server.player1.ultimate_gage = min(play_server.player1.ultimate_gage + self.ATK_INFO[0] / 50, 3)
            else:
                play_server.player2.ultimate_gage = min(play_server.player2.ultimate_gage + self.ATK_INFO[0] / 50, 3)
            self.cooltime = cur_time


class MegaKnuckle:
    FRAME_INFO = [(340, 326, 10, 15,)]
    ATK_INFO = (5, 2)
    atk_sound = None

    def __init__(self, x, y, size):
        self.img = projectile
        self.x, self.y = x, y
        self.dir = 0
        self.frame = 0
        self.size = size
        self.speed = -10
        game_world.add_obj(self, 1)
        game_world.add_collision_pair("knuckle:ground", self, None)
        if MegaKnuckle.atk_sound == None:
            MegaKnuckle.atk_sound = load_wav("sound/ouch.wav")
            MegaKnuckle.atk_sound.set_volume(50)

    def draw(self):
        frame = self.frame
        self.img.clip_draw(*self.FRAME_INFO[0],
                           self.x, self.y,
                           self.FRAME_INFO[0][2] * self.size, self.FRAME_INFO[0][3] * self.size)
        draw_rectangle(*self.get_bb())

    def update(self):
        self.y += self.speed * game_world.PIXEL_PER_METER * game_framework.frame_time
        self.speed -= game_framework.frame_time * game_world.g

    def get_bb(self):
        return (self.x - self.FRAME_INFO[0][2] * self.size // 2,
                self.y - self.FRAME_INFO[0][3] * self.size // 2,
                self.x + self.FRAME_INFO[0][2] * self.size // 2,
                self.y + self.FRAME_INFO[0][3] * self.size // 2)

    def handle_collision(self, group, other):
        if group == "knuckle:ground":
            game_world.erase_obj(self)
        elif other.control_method.isHit(group):
            MegaKnuckle.atk_sound.play()
            if self.dir > 0:
                other.hit(*self.ATK_INFO, knock_up=self.speed - 20, atk_pos=self.get_bb()[0])
            else:
                other.hit(*self.ATK_INFO, knock_up=self.speed - 20, atk_pos=self.get_bb()[2])
            if group == "Player1:Player2":
                play_server.player1.ultimate_gage = min(play_server.player1.ultimate_gage + self.ATK_INFO[0] / 50, 3)
            else:
                play_server.player2.ultimate_gage = min(play_server.player2.ultimate_gage + self.ATK_INFO[0] / 50, 3)
            game_world.erase_obj(self)


class MegaBlade:
    FRAME_INFO = [(307, 571, 20, 20,),
                  (332, 571, 20, 20,), ]
    FRAME_PER_SEC = 12
    nFrame = 2
    ATK_INFO = (25, 2, 0, 8)

    def __init__(self, x, y, dir):
        self.img = projectile
        self.x, self.y = x, y
        self.speed = 10 * dir
        self.ATK_INFO = list(MegaBlade.ATK_INFO)
        self.ATK_INFO[3] *= dir
        self.dir = dir
        self.frame = 0
        self.size = get_canvas_height() / 200
        self.sound = Sound("sound/blade_sound.wav")
        self.sound.play()
        game_world.add_obj(self, 1)

    def draw(self):
        frame = int(self.frame)
        if self.dir == 1:
            self.img.clip_draw(*self.FRAME_INFO[frame],
                               self.x, self.y,
                               self.FRAME_INFO[frame][2] * self.size, self.FRAME_INFO[frame][3] * self.size)
        else:
            self.img.clip_composite_draw(*self.FRAME_INFO[frame],
                                         0, 'h',
                                         self.x, self.y,
                                         self.FRAME_INFO[frame][2] * self.size,
                                         self.FRAME_INFO[frame][3] * self.size)
        draw_rectangle(*self.get_bb())

    def update(self):
        self.frame = (self.frame + game_framework.frame_time * self.FRAME_PER_SEC) % self.nFrame
        self.x += self.speed * game_world.PIXEL_PER_METER * game_framework.frame_time
        if self.x > get_canvas_width() + 50 or self.x < 0 - 50:
            game_world.erase_obj(self)

    def get_bb(self):
        frame = int(self.frame)
        return (self.x - self.FRAME_INFO[frame][2] * self.size // 2,
                self.y - self.FRAME_INFO[frame][3] * self.size // 2,
                self.x + self.FRAME_INFO[frame][2] * self.size // 2,
                self.y + self.FRAME_INFO[frame][3] * self.size // 2)

    def handle_collision(self, group, other):
        if other.control_method.isHit(group):
            if self.dir > 0:
                other.hit(*self.ATK_INFO, atk_pos=self.get_bb()[0])
            else:
                other.hit(*self.ATK_INFO, atk_pos=self.get_bb()[2])
            if group == "Player1:Player2":
                play_server.player1.ultimate_gage = min(play_server.player1.ultimate_gage + self.ATK_INFO[0] / 50, 3)
            else:
                play_server.player2.ultimate_gage = min(play_server.player2.ultimate_gage + self.ATK_INFO[0] / 50, 3)
            self.sound = None
            game_world.erase_obj(self)
