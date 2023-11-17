import time

from pico2d import *

import game_framework
import game_world


# state = JumpSuperPunch
# for i in range(len(state.l)):
#     print(f"({state.l[i]},{mario.img.h - state.t[i] - state.h[i]},{state.w[i]},{state.h[i]},),")
# print(len(state.l))

def end_of_animation(e):
    return e[0] == "EOA"


def check_run(e):
    return e[0] == "CHECK_STATE" and e[1] != 0


def check_idle(e):
    return e[0] == "CHECK_STATE" and e[1] == 0


def land(e):
    return e[0] == "LAND"


def time_out(e):
    return e[0] == "TIMEOUT"


def hit(e):
    return e[0] == "HIT"


class Hit:
    frame = [(15, 973, 26, 34,), ]
    nFrame = 1
    FRAME_PER_SEC = 15
    start_time = 0

    @staticmethod
    def enter(mario):
        mario.frame = 0
        mario.speed[0] = 0
        Hit.start_time = time.time()

    @staticmethod
    def do(mario):
        mario.next_frame()
        if time.time() - Hit.start_time >= mario.rigid_time and not mario.isFall:
            mario.state_machine.handle_event(("TIMEOUT", 0))


class Land:
    frame = [(111, 2401, 26, 34,),
             (141, 2401, 26, 33,),
             (171, 2401, 26, 34,), ]

    nFrame = 3
    FRAME_PER_SEC = 15

    @staticmethod
    def enter(mario):
        mario.frame = 0
        mario.speed[0] = 0

    @staticmethod
    def do(mario):
        isRepeat = False if int(mario.frame) == 0 else True
        mario.next_frame()
        if int(mario.frame) == 0 and isRepeat:
            mario.state_machine.handle_event(("EOA", 0))


class AnimationEnd:
    @staticmethod
    def enter(mario):
        mario.frame = 0
        mario.rigid_time = 0
        mario.state_machine.handle_event(("CHECK_STATE", mario.dir))


class Idle:
    frame = [(18, 2466, 23, 36),
             (45, 2466, 23, 37),
             (72, 2466, 23, 38),
             (99, 2466, 24, 38),
             (126, 2466, 25, 37),
             (153, 2466, 25, 36),
             (126, 2466, 25, 37),
             (99, 2466, 24, 38),
             (72, 2466, 23, 38),
             (45, 2466, 23, 37)]
    nFrame = 10
    FRAME_PER_SEC = 10

    @staticmethod
    def enter(mario):
        mario.speed = [0, 0]
        mario.dir = 0

    @staticmethod
    def do(mario):
        mario.next_frame()


class TurnKick:
    frame = [(14, 1492, 26, 36),
             (46, 1492, 45, 32),
             (97, 1492, 39, 31),
             (142, 1492, 36, 33),
             (184, 1492, 34, 35),
             (224, 1492, 32, 34),
             (262, 1492, 33, 32),
             (301, 1492, 33, 31),
             (340, 1492, 25, 34), ]
    nFrame = 9
    FRAME_PER_SEC = 18

    @staticmethod
    def enter(mario):
        mario.frame = 0
        mario.speed[0] = 0

    @staticmethod
    def do(mario):
        isRepeat = False if int(mario.frame) == 0 else True
        mario.next_frame()
        if int(mario.frame) == 0 and isRepeat:
            mario.state_machine.handle_event(("EOA", 0))


class Run:
    frame = [(12, 2343, 28, 36),
             (44, 2345, 30, 34),
             (82, 2342, 29, 36),
             (116, 2340, 24, 36),
             (146, 2342, 28, 36),
             (181, 2343, 30, 34),
             (220, 2342, 28, 36),
             (254, 2340, 24, 36), ]
    nFrame = 8
    RUN_SPEED = 3.5
    FRAME_PER_SEC = 8

    @staticmethod
    def enter(mario):
        mario.speed[0] = Run.RUN_SPEED * mario.dir
        if mario.dir == 1:
            mario.face_dir = "r"
        else:
            mario.face_dir = "l"

    @staticmethod
    def do(mario):
        mario.next_frame()


class Jump:
    frame = [(15, 2403, 24, 40),
             (45, 2404, 27, 39),
             (78, 2401, 29, 42)]
    nFrame = 3
    JUMP_POWER = 15
    FRAME_PER_SEC = 10

    @staticmethod
    def enter(mario):
        mario.frame = 0
        mario.isFall = True
        mario.speed[1] = Jump.JUMP_POWER

    @staticmethod
    def do(mario):
        mario.next_frame()
        if mario.isFall:
            if (mario.speed[1] > 10):
                mario.frame = min(mario.frame, 0)
        else:
            mario.state_machine.handle_event(("LAND", 0))


class JumpKick:
    frame = [(11, 2101, 31, 40,),
             (48, 2110, 36, 30,),
             (48, 2110, 36, 30,),
             (90, 2101, 30, 40,),
             (126, 2099, 29, 42,), ]

    nFrame = 5
    FRAME_PER_SEC = 12
    SPEED = 1

    @staticmethod
    def enter(mario):
        mario.frame = 0
        if mario.face_dir == "r":
            mario.speed[0] += JumpKick.SPEED
        else:
            mario.speed[0] -= JumpKick.SPEED

    @staticmethod
    def do(mario):
        mario.next_frame()
        if not mario.isFall:
            mario.state_machine.handle_event(("LAND", 0))


class JumpSuperPunch:
    frame = [(14, 1419, 32, 40,),
             (52, 1419, 32, 40,),
             (90, 1419, 32, 40,),
             (129, 1419, 35, 40,),
             (170, 1420, 29, 38,),
             (205, 1421, 44, 38,),
             (255, 1421, 42, 36,),
             (303, 1419, 32, 38,),
             (341, 1419, 30, 40,),
             (377, 1426, 34, 32,),
             (417, 1436, 36, 21,),
             (16, 1378, 35, 29,),
             (57, 1373, 35, 34,),
             (98, 1374, 36, 34,),
             (140, 1371, 36, 31,),
             (181, 1374, 34, 34,), ]

    nFrame = 16
    FRAME_PER_SEC = 24
    SPEED = 5

    @staticmethod
    def enter(mario):
        mario.frame = 0
        if mario.face_dir == "r":
            mario.speed[0] += JumpSpinKick.SPEED
        else:
            mario.speed[0] -= JumpSpinKick.SPEED
        mario.speed[1] = 0
        mario.control_method.ultimate_gage -= 1

    @staticmethod
    def do(mario):
        mario.next_frame()
        if not int(mario.frame) == JumpSuperPunch.nFrame - 1:
            mario.speed[1] = 0
        if not mario.isFall:
            mario.state_machine.handle_event(("LAND", 0))


class JumpSpinKick:
    frame = [(14, 1316, 31, 40,),
             (51, 1322, 39, 26,),
             (96, 1324, 39, 20,),
             (141, 1316, 39, 36,),
             (186, 1323, 39, 27,),
             (231, 1326, 39, 20,),
             (276, 1327, 39, 22,),
             (321, 1318, 39, 36,),
             (367, 1316, 30, 40,),
             (403, 1314, 29, 42,), ]

    nFrame = 10
    FRAME_PER_SEC = 25
    SPEED = 2

    @staticmethod
    def enter(mario):
        mario.frame = 0
        if mario.face_dir == "r":
            mario.speed[0] += JumpSpinKick.SPEED
        else:
            mario.speed[0] -= JumpSpinKick.SPEED

    @staticmethod
    def do(mario):
        mario.next_frame()
        if not mario.isFall:
            mario.state_machine.handle_event(("LAND", 0))


class OneJabTwoPunchThreeKick:
    frame = [(12, 2232, 36, 34),
             (54, 2232, 48, 32),
             (105, 2232, 44, 32),
             (152, 2232, 34, 32),
             (193, 2232, 34, 32),
             (233, 2232, 31, 34),
             (270, 2232, 31, 34),
             (307, 2232, 44, 32),
             (356, 2232, 40, 32),
             (400, 2232, 35, 32),
             (13, 2180, 27, 34),
             (46, 2181, 23, 36),
             (73, 2181, 48, 43),
             (125, 2181, 40, 38),
             (169, 2181, 32, 38),
             (205, 2182, 23, 37),
             (232, 2180, 23, 33), ]
    nFrame = 17
    FRAME_PER_SEC = 25

    @staticmethod
    def enter(mario):
        mario.frame = 0
        mario.speed[0] = 0

    @staticmethod
    def do(mario):
        isRepeat = False if int(mario.frame) == 0 else True
        mario.next_frame()
        if int(mario.frame) == 0 and isRepeat:
            mario.state_machine.handle_event(("EOA", 0))


class Uppercut:
    frame = [(14, 1940, 35, 30),
             (54, 1939, 34, 38),
             (96, 1939, 22, 53),
             (54, 1939, 34, 38), ]
    nFrame = 4
    FRAME_PER_SEC = 12
    JUMP_POWER = 13

    @staticmethod
    def enter(mario):
        mario.frame = 0
        mario.speed[0] = 0

    @staticmethod
    def do(mario):
        isRepeat = False if int(mario.frame) == 0 else True
        mario.next_frame()
        if mario.isFall:
            mario.frame = min(mario.frame, 2)
        else:
            if int(mario.frame) == 0 and isRepeat:
                mario.state_machine.handle_event(("EOA", 0))
            if int(mario.frame) == 1:
                mario.isFall = True
                mario.speed[1] = Uppercut.JUMP_POWER


class SomersaultKick:
    frame = [(141, 2401, 26, 33),
             (14, 1838, 37, 37),
             (57, 1857, 50, 26),
             (113, 1863, 37, 52),
             (156, 1863, 38, 32),
             (200, 1859, 38, 30),
             (244, 1851, 37, 31),
             (287, 1844, 23, 37),
             (316, 1838, 29, 42), ]
    nFrame = 9
    FRAME_PER_SEC = 15
    JUMP_POWER = 12

    @staticmethod
    def enter(mario):
        mario.frame = 0
        mario.speed[0] = 0

    @staticmethod
    def do(mario):
        isRepeat = False if int(mario.frame) == 0 else True
        mario.next_frame()
        if not mario.isFall:
            if int(mario.frame) == 0 and isRepeat:
                mario.state_machine.handle_event(("EOA", 0))
            elif int(mario.frame) == 2:
                mario.isFall = True
                mario.speed[1] = SomersaultKick.JUMP_POWER


class MagicCape:
    frame = [(40, 1153, 30, 37),
             (80, 1153, 23, 37),
             (109, 1153, 53, 38),
             (168, 1153, 47, 34),
             (221, 1153, 45, 52),
             (275, 1153, 26, 53),
             (307, 1153, 27, 38),
             (340, 1153, 38, 35),
             (384, 1153, 27, 34),
             (418, 1153, 25, 34), ]
    nFrame = 10
    FRAME_PER_SEC = 12

    @staticmethod
    def enter(mario):
        mario.frame = 0
        mario.control_method.ultimate_gage -= 3

    @staticmethod
    def do(mario):
        isRepeat = False if int(mario.frame) == 0 else True
        mario.next_frame()
        if int(mario.frame) == 0 and isRepeat:
            mario.state_machine.handle_event(("EOA", 0))


class PalmStrike:
    frame = [(13, 1559, 24, 35),
             (43, 1564, 27, 32),
             (76, 1561, 26, 42),
             (108, 1561, 27, 40),
             (141, 1561, 42, 35),
             (141, 1561, 42, 35),
             (189, 1561, 37, 37),
             (232, 1561, 25, 34), ]
    nFrame = 8
    FRAME_PER_SEC = 12

    @staticmethod
    def enter(mario):
        mario.frame = 0
        mario.control_method.ultimate_gage -= 1

    @staticmethod
    def do(mario):
        isRepeat = False if int(mario.frame) == 0 else True
        mario.next_frame()
        if int(mario.frame) == 0 and isRepeat:
            mario.state_machine.handle_event(("EOA", 0))


class StateMachine:
    def __init__(self, mario):
        self.state = Idle
        self.mario = mario
        self.table = {Idle: {mario.control_method.move_r_down: Run, mario.control_method.move_l_down: Run,
                             mario.control_method.move_r_up: Run, mario.control_method.move_l_up: Run,
                             mario.control_method.jump_down: Jump, hit: Hit,
                             mario.control_method.atk1_down: OneJabTwoPunchThreeKick,
                             mario.control_method.atk2_down: TurnKick,
                             mario.control_method.up_atk1_down: Uppercut,
                             mario.control_method.up_atk2_down: SomersaultKick,
                             mario.control_method.ultimate_down: PalmStrike,
                             mario.control_method.up_ultimate_down: MagicCape
                             },
                      Run: {mario.control_method.move_r_up: Idle, mario.control_method.move_l_up: Idle,
                            mario.control_method.move_r_down: Idle, mario.control_method.move_l_down: Idle,
                            mario.control_method.jump_down: Jump, hit: Hit,
                            mario.control_method.atk1_down: OneJabTwoPunchThreeKick,
                            mario.control_method.atk2_down: TurnKick,
                            mario.control_method.up_atk1_down: Uppercut,
                            mario.control_method.up_atk2_down: SomersaultKick,
                            mario.control_method.ultimate_down: PalmStrike,
                            mario.control_method.up_ultimate_down: MagicCape
                            },
                      AnimationEnd: {check_run: Run, check_idle: Idle},
                      Land: {end_of_animation: AnimationEnd},
                      Jump: {land: Land, mario.control_method.atk1_down: JumpKick,
                             mario.control_method.atk2_down: JumpSpinKick, hit: Hit,
                             mario.control_method.ultimate_down: JumpSuperPunch},
                      OneJabTwoPunchThreeKick: {end_of_animation: AnimationEnd},
                      TurnKick: {end_of_animation: AnimationEnd},
                      SomersaultKick: {end_of_animation: Land},
                      Uppercut: {end_of_animation: Land},
                      MagicCape: {end_of_animation: AnimationEnd},
                      PalmStrike: {end_of_animation: AnimationEnd},
                      JumpKick: {land: Land},
                      JumpSpinKick: {land: Land},
                      JumpSuperPunch: {land: Land},
                      Hit: {time_out: AnimationEnd}
                      }

    def start(self):
        self.state.enter(self.mario, ("START", 0))

    def draw(self):
        frame = int(self.mario.frame)
        if self.mario.face_dir == "r":
            self.mario.img.clip_draw(
                *self.state.frame[frame],
                self.mario.x,
                self.mario.y + self.mario.size * self.state.frame[frame][3] // 2,
                self.state.frame[frame][2] * self.mario.size,
                self.state.frame[frame][3] * self.mario.size
            )
        elif self.mario.face_dir == "l":
            self.mario.img.clip_composite_draw(
                *self.state.frame[frame],
                0, 'h',
                self.mario.x,
                self.mario.y + self.mario.size * self.state.frame[frame][3] // 2,
                self.state.frame[frame][2] * self.mario.size,
                self.state.frame[frame][3] * self.mario.size
            )

    def update(self):
        self.mario.move()
        self.state.do(self.mario)

    def handle_event(self, e):
        if self.mario.control_method.up_down(e):
            self.mario.up = True
        elif self.mario.control_method.up_up(e):
            self.mario.up = False
        elif self.mario.control_method.move_r_down(e) or self.mario.control_method.move_l_up(e):
            self.mario.dir += 1
        elif self.mario.control_method.move_l_down(e) or self.mario.control_method.move_r_up(e):
            self.mario.dir -= 1
        for check, next_state in self.table[self.state].items():
            if check(e):
                self.state = next_state
                self.state.enter(self.mario)


class Mario:
    img = None

    def __init__(self, control_method):
        self.isFall = True
        self.x, self.y = control_method.x, game_world.ground
        self.frame = 0
        self.size = 2
        self.control_method = control_method
        self.face_dir = control_method.start_face
        self.dir = 0
        self.speed = [0, 0]
        self.atk_box = None
        self.hp = 100
        self.rigid_time = 0
        self.resist_coefficient = 0.25
        self.font = load_font('ENCR10B.TTF', 40)
        self.state_machine = StateMachine(self)
        self.up = False
        if Mario.img == None:
            Mario.img = load_image('mario.png')

    def draw(self):
        self.state_machine.draw()
        frame = int(self.frame)
        state = self.state_machine.state
        draw_rectangle(*self.get_bb())
        self.font.draw(self.x, self.y + state.frame[frame][3] * self.size + 5, f"{self.hp}", (0, 0, 0))
        self.font.draw(self.x, 300, f"{round(self.control_method.ultimate_gage, 2)}", (0, 0, 0))

    def update(self):
        self.state_machine.update()
        self.control_method.ultimate_gage = min(self.control_method.ultimate_gage + game_framework.frame_time, 3)

    def move(self):
        self.x += self.speed[0] * game_world.PIXEL_PER_METER * game_framework.frame_time
        self.y += self.speed[1] * game_world.PIXEL_PER_METER * game_framework.frame_time
        if self.isFall:
            self.speed[1] -= game_world.g * game_framework.frame_time

    def handle_event(self, e):
        self.state_machine.handle_event(("INPUT", e, self.up))

    def get_hitbox(self):
        pass

    def next_frame(self):
        state = self.state_machine.state
        self.frame = (self.frame + state.FRAME_PER_SEC * game_framework.frame_time) % state.nFrame
        if self.isFall:
            self.frame = min(self.frame, state.nFrame - 1)

    def get_bb(self):
        frame = int(self.frame)
        state = self.state_machine.state
        return self.x - state.frame[frame][2] * self.size // 2, self.y, self.x + state.frame[frame][
            2] * self.size // 2, self.y + state.frame[frame][3] * self.size

    def handle_collision(self, group, other):
        if group == "character:ground":
            self.y = other.y + 1
            self.speed[1] = 0
            self.isFall = False
        if self.control_method.isHit(group):
            self.state_machine.handle_event(("HIT", 0))

    def hit(self, damage, rigid):
        self.control_method.ultimate_gage = min(self.control_method.ultimate_gage + damage / 2, 3)
        self.rigid_time += rigid * self.hp / 100 * self.resist_coefficient
        self.hp -= damage
