from pico2d import *

import game_framework
import game_world


def end_of_animation(e):
    return e[0] == "EOA"


def check_up_run(e):
    return e[0] == "CHECK_STATE" and e[1] != 0 and e[2]


def check_run(e):
    return e[0] == "CHECK_STATE" and e[1] != 0 and not e[2]


def check_idle(e):
    return e[0] == "CHECK_STATE" and e[1] == 0 and not e[2]


def check_up_idle(e):
    return e[0] == "CHECK_STATE" and e[1] == 0 and e[2]


def land(e):
    return e[0] == "LAND"


class Land:
    frame = [
        (111, 2401, 26, 34),
        (141, 2401, 26, 33), ]

    FRAME_PER_SEC = 15
    @staticmethod
    def enter(mario):
        mario.frame = 0
        mario.speed[0] = 0

    @staticmethod
    def do(mario):
        isRepeat = False if int(mario.frame) == 0 else True
        mario.frame = (mario.frame + Land.FRAME_PER_SEC * game_framework.frame_time) % len(Land.frame)
        if int(mario.frame) == 0 and isRepeat:
            mario.state_machine.handle_event(("EOA", 0))


class AnimationEnd:
    @staticmethod
    def enter(mario):
        mario.frame = 0
        mario.state_machine.handle_event(("CHECK_STATE", mario.dir, mario.up))


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
    FRAME_PER_SEC = 10

    @staticmethod
    def enter(mario):
        mario.speed = [0, 0]
        mario.dir = 0

    @staticmethod
    def do(mario):
        mario.frame = (mario.frame + Idle.FRAME_PER_SEC * game_framework.frame_time) % len(Idle.frame)


class UpIdle:
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

    FRAME_PER_SEC = 10

    @staticmethod
    def enter(mario):
        mario.speed = [0, 0]
        mario.dir = 0

    @staticmethod
    def do(mario):
        mario.frame = (mario.frame + UpIdle.FRAME_PER_SEC * game_framework.frame_time) % len(UpIdle.frame)


class TurnKick:
    frame = [(14, 1492, 26, 36),
             (14, 1492, 26, 36),
             (46, 1492, 45, 32),
             (46, 1492, 45, 32),
             (97, 1492, 39, 31),
             (142, 1492, 36, 33),
             (184, 1492, 34, 35),
             (224, 1492, 32, 34),
             (262, 1492, 33, 32),
             (301, 1492, 33, 31),
             (340, 1492, 25, 34),
             (340, 1492, 25, 34),
             (340, 1492, 25, 34), ]

    FRAME_PER_SEC = 25

    @staticmethod
    def enter(mario):
        mario.frame = 0
        mario.speed[0] = 0

    @staticmethod
    def do(mario):
        isRepeat = False if int(mario.frame) == 0 else True
        mario.frame = (mario.frame + TurnKick.FRAME_PER_SEC * game_framework.frame_time) % len(TurnKick.frame)
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
    RUN_SPEED = 3
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
        mario.frame = (mario.frame + Run.FRAME_PER_SEC * game_framework.frame_time) % len(Run.frame)


class UpRun:
    frame = [(12, 2343, 28, 36),
             (44, 2345, 30, 34),
             (82, 2342, 29, 36),
             (116, 2340, 24, 36),
             (146, 2342, 28, 36),
             (181, 2343, 30, 34),
             (220, 2342, 28, 36),
             (254, 2340, 24, 36), ]

    RUN_SPEED = 3
    FRAME_PER_SEC = 8

    @staticmethod
    def enter(mario):
        if mario.dir == 1:
            mario.speed[0] = Run.RUN_SPEED
            mario.face_dir = "r"
        else:
            mario.speed[0] = -Run.RUN_SPEED
            mario.face_dir = "l"

    @staticmethod
    def do(mario):
        mario.frame = (mario.frame + UpRun.FRAME_PER_SEC * game_framework.frame_time) % len(UpRun.frame)


class Jump:
    frame = [(15, 2403, 24, 40),
             (45, 2404, 27, 39),
             (78, 2401, 29, 42)
             ]

    JUMP_POWER = 15
    FRAME_PER_SEC = 10

    @staticmethod
    def enter(mario):
        mario.frame = 0
        mario.speed[1] = Jump.JUMP_POWER

    @staticmethod
    def do(mario):
        mario.frame = (mario.frame + Jump.FRAME_PER_SEC * game_framework.frame_time) % len(Jump.frame)
        if mario.y > game_world.ground:
            if (mario.speed[1] < 10):
                mario.frame = min(mario.frame, 2)
            else:
                mario.frame = min(mario.frame, 0)
        elif int(mario.frame) == 0:
            mario.state_machine.handle_event(("LAND", 0))


class OneJabTwoStraightThreeKick:
    frame = [(12, 2232, 36, 34),
             (12, 2232, 36, 34),
             (54, 2232, 48, 32),
             (105, 2232, 44, 32),
             (152, 2232, 34, 32),
             (193, 2232, 34, 32),
             (233, 2232, 31, 34),
             (270, 2232, 31, 34),
             (307, 2232, 44, 32),
             (356, 2232, 40, 32),
             (356, 2232, 40, 32),
             (400, 2232, 35, 32),
             (400, 2232, 35, 32),
             (13, 2180, 27, 34),
             (13, 2183, 27, 34),
             (46, 2181, 23, 36),
             (46, 2181, 23, 36),
             (73, 2181, 48, 43),
             (73, 2181, 48, 43),
             (125, 2181, 40, 38),
             (125, 2181, 40, 38),
             (169, 2181, 32, 38),
             (169, 2181, 32, 38),
             (205, 2182, 23, 37),
             (205, 2182, 23, 37),
             (232, 2180, 23, 33),
             (232, 2180, 26, 33), ]

    FRAME_PER_SEC = 30

    @staticmethod
    def enter(mario):
        mario.frame = 0
        mario.speed[0] = 0

    @staticmethod
    def do(mario):
        isRepeat = False if int(mario.frame) == 0 else True
        mario.frame = (mario.frame + OneJabTwoStraightThreeKick.FRAME_PER_SEC * game_framework.frame_time) % len(
            OneJabTwoStraightThreeKick.frame)
        if int(mario.frame) == 0 and isRepeat:
            mario.state_machine.handle_event(("EOA", 0))


class Uppercut:
    frame = [(14, 1940, 35, 30),
             (14, 1940, 35, 30),
             (54, 1939, 34, 38),
             (96, 1939, 22, 53),
             (54, 1939, 34, 38), ]

    FRAME_PER_SEC = 13
    JUMP_POWER = 13

    @staticmethod
    def enter(mario):
        mario.frame = 0
        mario.speed[0] = 0

    @staticmethod
    def do(mario):
        isRepeat = False if int(mario.frame) == 0 else True
        mario.frame = (mario.frame + Uppercut.FRAME_PER_SEC * game_framework.frame_time) % len(Uppercut.frame)
        if mario.y > game_world.ground:
            mario.frame = min(mario.frame, 3)
        elif int(mario.frame) == 0 and isRepeat:
            mario.state_machine.handle_event(("EOA", 0))
        elif int(mario.frame) == 1:
            mario.speed[1] = Uppercut.JUMP_POWER


class SomersaultKick:
    frame = [(141, 2401, 26, 33),
             (141, 2401, 26, 33),
             (14, 1838, 37, 37),
             (57, 1857, 50, 26),
             (113, 1863, 37, 52),
             (156, 1863, 38, 32),
             (200, 1859, 38, 30),
             (244, 1851, 37, 31),
             (287, 1844, 23, 37),
             (316, 1838, 29, 42), ]

    FRAME_PER_SEC = 15
    JUMP_POWER = 12

    @staticmethod
    def enter(mario):
        mario.frame = 0
        mario.speed[0] = 0

    @staticmethod
    def do(mario):
        isRepeat = False if int(mario.frame) == 0 else True
        mario.frame = (mario.frame + SomersaultKick.FRAME_PER_SEC * game_framework.frame_time) % len(
            SomersaultKick.frame)
        if mario.y > game_world.ground:
            mario.frame = min(mario.frame, 9)
        elif int(mario.frame) == 0 and isRepeat:
            mario.state_machine.handle_event(("EOA", 0))
        elif int(mario.frame) == 3:
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

    FRAME_PER_SEC = 12
    @staticmethod
    def enter(mario):
        mario.frame = 0

    @staticmethod
    def do(mario):
        isRepeat = False if int(mario.frame) == 0 else True
        mario.frame = (mario.frame + MagicCape.FRAME_PER_SEC * game_framework.frame_time) % len(MagicCape.frame)
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

    FRAME_PER_SEC = 12

    @staticmethod
    def enter(mario):
        mario.frame = 0

    @staticmethod
    def do(mario):
        isRepeat = False if int(mario.frame) == 0 else True
        mario.frame = (mario.frame + PalmStrike.FRAME_PER_SEC * game_framework.frame_time) % len(PalmStrike.frame)
        if int(mario.frame) == 0 and isRepeat:
            mario.state_machine.handle_event(("EOA", 0))


class StateMachine:
    def __init__(self, mario):
        self.state = Idle
        self.mario = mario
        self.table = {Idle: {mario.control_method.move_r_down: Run, mario.control_method.move_l_down: Run,
                             mario.control_method.move_r_up: Run, mario.control_method.move_l_up: Run,
                             mario.control_method.up_down: UpIdle,
                             mario.control_method.jump_down: Jump,
                             mario.control_method.atk1_down: OneJabTwoStraightThreeKick,
                             mario.control_method.atk2_down: TurnKick
                             },
                      UpIdle: {mario.control_method.move_r_down: UpRun, mario.control_method.move_l_down: UpRun,
                               mario.control_method.move_r_up: UpRun, mario.control_method.move_l_up: UpRun,
                               mario.control_method.up_down: Idle,
                               mario.control_method.jump_down: Jump,
                               mario.control_method.atk1_down: Uppercut,
                               mario.control_method.atk2_down: SomersaultKick},
                      Run: {mario.control_method.move_r_up: Idle, mario.control_method.move_l_up: Idle,
                            mario.control_method.move_r_down: Idle, mario.control_method.move_l_down: Idle,
                            mario.control_method.jump_down: Jump,
                            mario.control_method.up_down: UpRun,
                            mario.control_method.atk1_down: OneJabTwoStraightThreeKick,
                            mario.control_method.atk2_down: TurnKick
                            },
                      UpRun: {mario.control_method.move_r_up: UpIdle, mario.control_method.move_l_up: UpIdle,
                              mario.control_method.move_r_down: UpIdle, mario.control_method.move_l_down: UpIdle,
                              mario.control_method.jump_down: Jump,
                              mario.control_method.atk1_down: Uppercut,
                              mario.control_method.atk2_down: SomersaultKick},
                      AnimationEnd: {check_run: Run, check_idle: Idle, check_up_run: UpRun, check_up_idle: UpIdle},
                      Land: {end_of_animation: AnimationEnd},
                      Jump: {land: Land},
                      OneJabTwoStraightThreeKick: {end_of_animation: AnimationEnd},
                      TurnKick: {end_of_animation: AnimationEnd},
                      SomersaultKick: {end_of_animation: Land},
                      Uppercut: {end_of_animation: Land},
                      MagicCape: {end_of_animation: AnimationEnd},
                      PalmStrike: {end_of_animation: AnimationEnd}
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
        self.x, self.y = control_method.x, game_world.ground
        self.frame = 0
        self.size = 2
        self.control_method = control_method
        self.face_dir = control_method.start_face
        self.dir = 0
        self.speed = [0, 0]
        self.state_machine = StateMachine(self)
        self.up = False
        if Mario.img == None:
            Mario.img = load_image('mario.png')

    def draw(self):
        self.state_machine.draw()

    def update(self):
        self.state_machine.update()

    def move(self):
        self.x += self.speed[0] * game_world.PIXEL_PER_METER * game_framework.frame_time
        self.y += self.speed[1] * game_world.PIXEL_PER_METER * game_framework.frame_time
        if self.y > game_world.ground:
            self.speed[1] -= game_world.g * game_framework.frame_time
        else:
            self.y = game_world.ground
            self.speed[1] = 0

    def handle_event(self, e):
        self.state_machine.handle_event(("INPUT", e))
