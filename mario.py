import time

from pico2d import *

import game_framework
import game_world
import play_sever


# state = JumpSuperPunch
# for i in range(len(state.l)):
#     print(f"({state.l[i]},{mario.img.h - state.t[i] - state.h[i]},{state.w[i]},{state.h[i]},),")
# print(len(state.l))

# state = TurnKick
# int_frame = int(mario.frame)
# dx, dy, sx, sy = state.FRAME_INFO[int_frame][2] * mario.size // 2, state.FRAME_INFO[int_frame][
#     3] * mario.size // 2, 0, 0
# if int_frame == 1:
#     sx, sy = 25, 13
# elif int_frame == 2:
#     sx, sy = 20, 11
#     dy -= 1
# elif int_frame == 3:
#     sx, sy = 15, 10
#     dy -= 3
# elif int_frame == 4:
#     sx, sy = 12, 10
#     dy -= 5
# if int_frame <= 4:
#     dx = dx - sx + 5
#     print(f"{int_frame}:{(dx, dy, sx, sy)}")
#     mario.set_atk_bb(dx, dy, sx, sy)
def end_of_animation(e):
    return e[0] == "EOA"


def check_run(e):
    return e[0] == "CHECK_RUN" and e[1] != 0


def land(e):
    return e[0] == "LAND"


def fall(e):
    return e == "FALL"


def time_out(e):
    return e[0] == "TIMEOUT"


def hit(e):
    return e[0] == "HIT"


def defense_fail(e):
    return e[0] == "DEFENSE_FAIL"


class Fall:
    FRAME_INFO = [(78, 2401, 29, 42)]
    nFrame = 1

    FRAME_PER_SEC = 1

    @staticmethod
    def exit(mario):
        pass

    @staticmethod
    def enter(mario):
        mario.frame = 0

    @staticmethod
    def do(mario):
        if not mario.isFall:
            mario.state_machine.handle_event(("LAND", 0))


class Defense:
    FRAME_INFO = [(154, 881, 26, 34,),
                  (186, 881, 28, 34,),
                  (220, 881, 23, 34,)]
    nFrame = 3
    FRAME_PER_SEC = 36

    @staticmethod
    def exit(mario):
        pass

    @staticmethod
    def enter(mario):
        mario.frame = 0
        mario.speed[0] = 0

    @staticmethod
    def do(mario):
        mario.next_frame()
        mario.frame = min(mario.frame, 2)


class Hit:
    FRAME_INFO = [(15, 973, 26, 34,), ]
    nFrame = 1
    FRAME_PER_SEC = 15
    start_time = 0

    @staticmethod
    def exit(mario):
        mario.rigid_time = 0

    @staticmethod
    def enter(mario):
        mario.frame = 0
        Hit.start_time = time.time()

    @staticmethod
    def do(mario):
        if time.time() - Hit.start_time >= mario.rigid_time and not mario.isFall:
            mario.state_machine.handle_event(("TIMEOUT", 0))


class Land:
    FRAME_INFO = [(111, 2401, 26, 34,),
                  (141, 2401, 26, 33,),
                  (171, 2401, 26, 34,), ]

    nFrame = 3
    FRAME_PER_SEC = 15

    @staticmethod
    def exit(mario):
        pass

    @staticmethod
    def enter(mario):
        mario.frame = 0
        mario.speed[0] = 0

    @staticmethod
    def do(mario):
        old_frame = int(mario.frame)
        mario.next_frame()
        int_frame = int(mario.frame)
        if int_frame == 0 and int_frame != old_frame:
            mario.state_machine.handle_event(("EOA", 0))


class Idle:
    FRAME_INFO = [(18, 2466, 23, 36),
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
    def exit(mario):
        pass

    @staticmethod
    def enter(mario):
        mario.speed = [0, 0]
        mario.state_machine.handle_event(("CHECK_RUN", mario.dir))

    @staticmethod
    def do(mario):
        mario.next_frame()


class TurnKick:
    FRAME_INFO = [(14, 1492, 26, 36),
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
    ATK_BB_INFO = {0: (31, 36, 0, 0),
                   1: (25, 32, 25, 13),
                   2: (24, 30, 20, 11),
                   3: (26, 30, 15, 10),
                   4: (27, 30, 12, 10)}
    ATK_INFO = (5, 0.1, 6, 4)

    @staticmethod
    def exit(mario):
        mario.atk_box.reset()

    @staticmethod
    def enter(mario):
        mario.frame = 0
        mario.speed[0] = 0
        mario.set_atk_info(*TurnKick.ATK_INFO)

    @staticmethod
    def do(mario):
        old_frame = int(mario.frame)
        mario.next_frame()
        state = TurnKick
        int_frame = int(mario.frame)

        if state.ATK_BB_INFO.get(int_frame):
            mario.set_atk_bb(*state.ATK_BB_INFO[int_frame])
        else:
            mario.atk_box.reset()
        if int_frame == 0 and int_frame != old_frame:
            mario.state_machine.handle_event(("EOA", 0))


class Run:
    FRAME_INFO = [(12, 2343, 28, 36),
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
    def exit(mario):
        pass

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
        mario.speed[0] = Run.RUN_SPEED * mario.dir


class Jump:
    FRAME_INFO = [(15, 2403, 24, 40),
                  (45, 2404, 27, 39)]
    nFrame = 2
    JUMP_POWER = 15
    FRAME_PER_SEC = 10

    @staticmethod
    def exit(mario):
        pass

    @staticmethod
    def enter(mario):
        mario.frame = 0
        mario.speed[1] = Jump.JUMP_POWER

    @staticmethod
    def do(mario):
        mario.next_frame()
        if mario.speed[1] > 10:
            mario.frame = min(mario.frame, 0)
        elif mario.speed[1] < 0:
            mario.state_machine.handle_event("FALL")


class JumpKick:
    FRAME_INFO = [(11, 2101, 31, 40,),
                  (48, 2110, 36, 30,),
                  (90, 2101, 30, 40,)]

    nFrame = 3
    FRAME_PER_SEC = 6
    SPEED = 1
    ATK_BB_INFO = (26, 15, 20, 20)
    ATK_INFO = (5, 0.3, 0)

    @staticmethod
    def exit(mario):
        mario.atk_box.reset()

    @staticmethod
    def enter(mario):
        mario.frame = 0
        if mario.face_dir == "r":
            mario.speed[0] += JumpKick.SPEED
        else:
            mario.speed[0] -= JumpKick.SPEED

    @staticmethod
    def do(mario):
        old_frame = int(mario.frame)
        mario.next_frame()
        state = JumpKick
        int_frame = int(mario.frame)
        if int_frame == 1:
            if int_frame != old_frame:
                mario.y += 20
                mario.set_atk_bb(*state.ATK_BB_INFO)
                mario.set_atk_info(*state.ATK_INFO, abs(mario.speed[0]) + 5)
        else:
            mario.atk_box.box_info = None
        if not mario.isFall:
            mario.state_machine.handle_event(("LAND", 0))


class JumpSuperPunch:
    FRAME_INFO = [(14, 1419, 32, 40,),
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
    SPEED = 3
    ATK_BB_INFO = [(-30, 40, 12, 13),
                   (-14, 63, 20, 13),
                   (29, 46, 20, 30),
                   (32, 31, 15, 15),
                   (22, 28, 15, 20)]
    ATK_INFO = (15, 0.1, -40)

    @staticmethod
    def exit(mario):
        mario.atk_box.reset()

    @staticmethod
    def enter(mario):
        mario.frame = 0
        if mario.face_dir == "r":
            mario.speed[0] += JumpSpinKick.SPEED
        else:
            mario.speed[0] -= JumpSpinKick.SPEED
        mario.speed[1] = 0
        mario.ultimate_gage -= 1

    @staticmethod
    def do(mario):
        old_frame = int(mario.frame)
        mario.next_frame()
        state = JumpSuperPunch
        int_frame = int(mario.frame)
        if 3 <= int_frame <= 7:
            if int_frame == 3 and int_frame != old_frame:
                mario.set_atk_info(*state.ATK_INFO, abs(mario.speed[0] * 1.3))
            mario.set_atk_bb(*state.ATK_BB_INFO[int_frame - 3])
        else:
            mario.atk_box.box_info = None
        if not int_frame == state.nFrame - 1:
            mario.speed[1] = 0
        if not mario.isFall:
            mario.state_machine.handle_event(("LAND", 0))


class JumpSpinKick:
    FRAME_INFO = [(14, 1316, 31, 40,),
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
    FRAME_PER_SEC = 15
    SPEED = 2
    ATK_BB_INFO = [(19, 29, 25, 17),
                   (19, 23, 25, 17),
                   (19, 39, 25, 17),
                   (19, 23, 25, 17),
                   (19, 16, 25, 17),
                   (19, 18, 25, 17),
                   (19, 32, 25, 17)]
    ATK_INFO = (2, 0.2, 1, -1)

    @staticmethod
    def exit(mario):
        mario.atk_box.reset()

    @staticmethod
    def enter(mario):
        mario.frame = 0
        if mario.face_dir == "r":
            mario.speed[0] += JumpSpinKick.SPEED
        else:
            mario.speed[0] -= JumpSpinKick.SPEED
        mario.speed[1] = max(mario.speed[1] + 5, 5)

    @staticmethod
    def do(mario):
        old_frame = int(mario.frame)
        mario.next_frame()
        state = JumpSpinKick
        int_frame = int(mario.frame)
        if 1 <= int_frame <= 7:
            if int_frame != old_frame:
                mario.set_atk_bb(*state.ATK_BB_INFO[int_frame - 1])
                mario.set_atk_info(*state.ATK_INFO)
        else:
            mario.atk_box.box_info = None
        if not mario.isFall:
            mario.state_machine.handle_event(("LAND", 0))


class OneJabTwoPunchThreeKick:
    FRAME_INFO = [(12, 2232, 36, 34),
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
                  (232, 2180, 26, 33), ]
    nFrame = 17
    FRAME_PER_SEC = 17
    JUMP_POWER = 5
    ATK_BB_INFO = {1: (33, 32, 20, 20),
                   2: (29, 22, 20, 20),
                   6: (14, 24, 12, 12),
                   7: (24, 32, 25, 25),
                   8: (20, 32, 25, 25),
                   9: (15, 32, 25, 25),
                   12: (28, 53, 25, 43),
                   13: (20, 48, 25, 38),
                   14: (17, 48, 10, 15)}
    ATK_INFO = {1: (5, 0.3, 0, 1),
                6: (3, 0.4, 0, 0.5),
                12: (7, 0.1, 10, 0.3)}

    @staticmethod
    def exit(mario):
        mario.atk_box.reset()

    @staticmethod
    def enter(mario):
        mario.frame = 0
        mario.speed[0] = 0

    @staticmethod
    def do(mario):
        old_frame = int(mario.frame)
        mario.next_frame()
        state = OneJabTwoPunchThreeKick
        int_frame = int(mario.frame)
        if int_frame != old_frame:
            if int_frame == 1 or int_frame == 6 or int_frame == 12:
                mario.set_atk_info(*state.ATK_INFO[int_frame])
            if int_frame == 12:
                mario.speed[1] = OneJabTwoPunchThreeKick.JUMP_POWER

        if state.ATK_BB_INFO.get(int_frame):
            mario.set_atk_bb(*state.ATK_BB_INFO[int_frame])
        else:
            mario.atk_box.reset()
        if int_frame == 0 and int_frame != old_frame:
            mario.state_machine.handle_event(("EOA", 0))


class Uppercut:
    FRAME_INFO = [(14, 1940, 35, 30),
                  (54, 1939, 34, 38),
                  (96, 1939, 22, 53), ]
    nFrame = 3
    FRAME_PER_SEC = 15
    JUMP_POWER = 13
    ATK_BB_INFO = [(17, 13.5, 13, 13),
                   (24, 38, 20, 20),
                   (12, 88.5, 20, 35)]
    ATK_INFO = (10, 0.1, 15, 0)

    @staticmethod
    def exit(mario):
        mario.atk_box.reset()

    @staticmethod
    def enter(mario):
        mario.frame = 0
        mario.speed[0] = 0
        mario.set_atk_info(*Uppercut.ATK_INFO)

    @staticmethod
    def do(mario):
        old_frame = int(mario.frame)
        mario.next_frame()
        state = Uppercut
        int_frame = int(mario.frame)
        mario.set_atk_bb(*state.ATK_BB_INFO[int_frame])
        if mario.speed[1] < 1 and mario.isFall:
            mario.state_machine.handle_event(("EOA", 0))
        if int_frame == 1 and int_frame != old_frame:
            mario.speed[1] = state.JUMP_POWER


class SomersaultKick:
    FRAME_INFO = [(141, 2401, 26, 33),
                  (14, 1838, 37, 37),
                  (57, 1857, 50, 26),
                  (113, 1863, 37, 52),
                  (156, 1863, 38, 32),
                  (200, 1859, 38, 30),
                  (244, 1851, 37, 31),
                  (287, 1844, 23, 37), ]
    nFrame = 9
    FRAME_PER_SEC = 14
    JUMP_POWER = 12
    ATK_BB_INFO = [(27, 47, 15, 20),
                   (40, 36, 15, 16),
                   (0, 79, 37, 30),
                   (-33, 47, 12, 30),
                   (-15, 6, 20, 12)]
    ATK_INFO = [(10, 0.1, 15, 0),
                (10, 0.1, -35, 0)]

    @staticmethod
    def exit(mario):
        mario.atk_box.reset()

    @staticmethod
    def enter(mario):
        mario.frame = 0
        mario.speed[0] = 0
        mario.set_atk_info(*SomersaultKick.ATK_INFO[0])

    @staticmethod
    def do(mario):
        old_frame = int(mario.frame)
        mario.next_frame()
        state = SomersaultKick
        int_frame = int(mario.frame)
        if 1 <= int_frame <= 5:
            mario.set_atk_bb(*state.ATK_BB_INFO[int_frame - 1])
            if int_frame == 4 and int_frame != old_frame:
                mario.set_atk_info(*state.ATK_INFO[1])
        else:
            mario.atk_box.box_info = None
        if int_frame == 8:
            mario.state_machine.handle_event(("EOA", 0))
        elif int_frame == 1 and not mario.isFall:
            mario.speed[1] = state.JUMP_POWER


class MagicCape:
    FRAME_INFO = [(40, 1153, 30, 37),
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
    FRAME_PER_SEC = 15
    ATK_BB_INFO = (1000, 52, 1000, 1000)
    ATK_INFO = (15, 0.1, 0, 0)

    @staticmethod
    def exit(mario):
        mario.atk_box.reset()

    @staticmethod
    def enter(mario):
        mario.frame = 0
        mario.ultimate_gage -= 3
        mario.atk_box.effect = "reflect"

    @staticmethod
    def do(mario):
        old_frame = int(mario.frame)
        mario.next_frame()
        state = MagicCape
        int_frame = int(mario.frame)
        if int_frame == 4:
            if int_frame != old_frame:
                mario.set_atk_bb(*state.ATK_BB_INFO)
                mario.set_atk_info(*state.ATK_INFO)
        else:
            mario.atk_box.box_info = None
        if int_frame == 0 and int_frame != old_frame:
            mario.state_machine.handle_event(("EOA", 0))


class PalmStrike:
    FRAME_INFO = [(13, 1559, 24, 35),
                  (43, 1564, 27, 32),
                  (76, 1561, 26, 42),
                  (108, 1561, 27, 40),
                  (141, 1561, 42, 35),
                  (141, 1561, 42, 35),
                  (189, 1561, 37, 37),
                  (232, 1561, 25, 34), ]
    nFrame = 8
    FRAME_PER_SEC = 12
    ATK_BB_INFO = (34, 35, 15, 20)
    ATK_INFO = (20, 0.1, 10, 10)

    @staticmethod
    def exit(mario):
        mario.atk_box.reset()

    @staticmethod
    def enter(mario):
        mario.frame = 0
        mario.speed[0] = 0
        mario.ultimate_gage -= 1

    @staticmethod
    def do(mario):
        old_frame = int(mario.frame)
        mario.next_frame()
        state = PalmStrike
        int_frame = int(mario.frame)
        if 4 <= int_frame <= 5:
            if int_frame == 4 and int_frame != old_frame:
                mario.set_atk_info(*state.ATK_INFO)
            mario.set_atk_bb(*state.ATK_BB_INFO)
        else:
            mario.atk_box.box_info = None
        if int_frame == 0 and int_frame != old_frame:
            mario.state_machine.handle_event(("EOA", 0))


class StateMachine:
    def __init__(self, mario):
        self.state = Idle
        self.mario = mario
        self.table = {Idle: {mario.control_method.move_r_down: Run, mario.control_method.move_l_down: Run,
                             mario.control_method.move_r_up: Run, mario.control_method.move_l_up: Run,
                             mario.control_method.jump_down: Jump, hit: Hit, check_run: Run,
                             mario.control_method.atk1_down: OneJabTwoPunchThreeKick,
                             mario.control_method.atk2_down: TurnKick, mario.control_method.defence_down: Defense,
                             mario.control_method.up_atk1_down: Uppercut,
                             mario.control_method.up_atk2_down: SomersaultKick,
                             mario.control_method.ultimate_down: PalmStrike,
                             mario.control_method.up_ultimate_down: MagicCape
                             },
                      Run: {mario.control_method.move_r_up: Idle, mario.control_method.move_l_up: Idle,
                            mario.control_method.move_r_down: Idle, mario.control_method.move_l_down: Idle,
                            mario.control_method.jump_down: Jump, hit: Hit, mario.control_method.defence_down: Defense,
                            mario.control_method.atk1_down: OneJabTwoPunchThreeKick,
                            mario.control_method.atk2_down: TurnKick,
                            mario.control_method.up_atk1_down: Uppercut,
                            mario.control_method.up_atk2_down: SomersaultKick,
                            mario.control_method.ultimate_down: PalmStrike,
                            mario.control_method.up_ultimate_down: MagicCape
                            },
                      Defense: {mario.control_method.defence_up: Idle, defense_fail: Hit},
                      Land: {end_of_animation: Idle, hit: Hit},
                      Jump: {fall: Fall, mario.control_method.atk1_down: JumpKick,
                             mario.control_method.atk2_down: JumpSpinKick, hit: Hit,
                             mario.control_method.ultimate_down: JumpSuperPunch,
                             mario.control_method.up_atk1_down: JumpKick,
                             mario.control_method.up_atk2_down: JumpSpinKick},
                      Fall: {land: Land, mario.control_method.atk1_down: JumpKick,
                             mario.control_method.atk2_down: JumpSpinKick, hit: Hit,
                             mario.control_method.ultimate_down: JumpSuperPunch,
                             mario.control_method.up_atk1_down: JumpKick,
                             mario.control_method.up_atk2_down: JumpSpinKick},
                      OneJabTwoPunchThreeKick: {end_of_animation: Idle, hit: Hit},
                      TurnKick: {end_of_animation: Idle, hit: Hit},
                      SomersaultKick: {end_of_animation: Fall},
                      Uppercut: {end_of_animation: Fall},
                      MagicCape: {end_of_animation: Idle},
                      PalmStrike: {end_of_animation: Idle},
                      JumpKick: {land: Land},
                      JumpSpinKick: {land: Land},
                      JumpSuperPunch: {land: Land},
                      Hit: {time_out: Idle},
                      }

    def start(self):
        self.state.enter(self.mario, ("START", 0))

    def draw(self):
        frame = int(self.mario.frame)
        if self.mario.face_dir == "r":
            self.mario.img.clip_draw(
                *self.state.FRAME_INFO[frame],
                self.mario.x,
                self.mario.y + self.mario.size * self.state.FRAME_INFO[frame][3] // 2,
                self.state.FRAME_INFO[frame][2] * self.mario.size,
                self.state.FRAME_INFO[frame][3] * self.mario.size
            )
        elif self.mario.face_dir == "l":
            self.mario.img.clip_composite_draw(
                *self.state.FRAME_INFO[frame],
                0, 'h',
                self.mario.x,
                self.mario.y + self.mario.size * self.state.FRAME_INFO[frame][3] // 2,
                self.state.FRAME_INFO[frame][2] * self.mario.size,
                self.state.FRAME_INFO[frame][3] * self.mario.size
            )

    def update(self):
        self.state.do(self.mario)
        self.mario.move()

    def handle_event(self, e):
        for check, next_state in self.table[self.state].items():
            if check(e):
                self.state.exit(self.mario)
                self.state = next_state
                self.state.enter(self.mario)


class Mario:
    img = None
    resist_coefficient = 0.25
    size = 2
    maxHp = 100 * 1.5
    weight = 75

    def __init__(self, control_method):
        self.isFall = True
        self.x, self.y = control_method.x, game_world.ground
        self.frame = 0
        self.control_method = control_method
        self.face_dir = control_method.start_face
        self.dir = 0
        self.hp = Mario.maxHp
        self.debuff = None
        self.debuff_time = 0
        self.speed = [0, 0]
        self.atk_box = AtkBox(self)
        self.rigid_time = 0
        self.ultimate_gage = 3
        self.font = load_font('ENCR10B.TTF', 40)
        self.state_machine = StateMachine(self)
        self.up = False
        control_method.add_atk_collision(self.atk_box)
        if Mario.img == None:
            Mario.img = load_image('mario.png')

    def set_atk_bb(self, dx, dy, sx, sy):
        self.atk_box.box_info = (dx, dy, sx, sy)
        if self.face_dir == "r":
            self.atk_box.x = self.get_bb()[0]
        else:
            self.atk_box.x = self.get_bb()[2]

    def set_atk_info(self, DAMAGE, RIGID, KNOCK_UP=0, KNOCK_BACK=0):
        if self.face_dir == "l":
            KNOCK_BACK *= -1
        self.atk_box.set_info(DAMAGE, RIGID, KNOCK_UP, KNOCK_BACK)

    def draw(self):
        self.state_machine.draw()
        frame = int(self.frame)
        state = self.state_machine.state
        draw_rectangle(*self.get_bb())
        if self.atk_box.get_bb():
            draw_rectangle(*self.atk_box.get_bb())
        self.font.draw(self.x, self.y + state.FRAME_INFO[frame][3] * self.size + 5, f"{self.hp}", (0, 0, 0))
        self.font.draw(self.x, 300, f"{round(self.ultimate_gage, 2)}", (0, 0, 0))

    def update(self):
        self.state_machine.update()
        self.debuff_time -= game_framework.frame_time
        if self.debuff_time < 0:
            if self.debuff == "confusion":
                self.dir *= -1
                if self.dir == 1:
                    self.face_dir = "r"
                elif self.dir == -1:
                    self.face_dir = "l"
            if self.debuff == "burn":
                self.hp -= 2 * - self.debuff_time
            self.debuff = None
        else:
            if self.debuff == "burn":
                self.hp -= 2 * game_framework.frame_time
                if self.debuff_time < 2 and self.debuff_time + game_framework.frame_time >= 2:
                    self.rigid_time += 0.5 * self.resist_coefficient * self.resist_coefficient ** self.rigid_time
                    self.speed[0] = 0
                    self.state_machine.handle_event(("HIT", 0))
                if self.debuff_time < 1 and self.debuff_time + game_framework.frame_time >= 1:
                    self.rigid_time += 0.5 * self.resist_coefficient * self.resist_coefficient ** self.rigid_time
                    self.speed[0] = 0
                    self.state_machine.handle_event(("HIT", 0))
        if not game_world.collide(play_sever.ground, self):
            self.isFall = True
        else:
            self.y = play_sever.ground.y
            if self.speed[1] > -30:
                self.speed[1] = 0
                self.isFall = False
            else:
                self.speed[1] = -(self.speed[1] + 30)
        self.ultimate_gage = min(self.ultimate_gage + game_framework.frame_time / 100, 3)

    def move(self):
        self.x += self.speed[0] * game_world.PIXEL_PER_METER * game_framework.frame_time
        self.y += self.speed[1] * game_world.PIXEL_PER_METER * game_framework.frame_time
        if self.isFall:
            self.speed[1] -= game_world.g * game_framework.frame_time
        else:
            if self.speed[0] > 0.001:
                self.speed[0] -= 0.5 * 10 * game_framework.frame_time
                if self.speed[0] <= 0.001:
                    self.speed[0] = 0
            elif self.speed[0] < -0.001:
                self.speed[0] += 0.5 * 10 * game_framework.frame_time
                if -0.001 <= self.speed[0]:
                    self.speed[0] = 0

    def handle_event(self, e):
        input_e = ("INPUT", e, self.up, self.ultimate_gage)
        if self.control_method.up_down(input_e):
            self.up = True
        elif self.control_method.up_up(input_e):
            self.up = False
        elif self.control_method.move_r_down(input_e) or self.control_method.move_l_up(input_e):
            if self.debuff == "confusion":
                self.dir -= 1
            else:
                self.dir += 1
        elif self.control_method.move_l_down(input_e) or self.control_method.move_r_up(input_e):
            if self.debuff == "confusion":
                self.dir += 1
            else:
                self.dir -= 1
        self.state_machine.handle_event(input_e)

    def next_frame(self):
        state = self.state_machine.state
        self.frame = (self.frame + state.FRAME_PER_SEC * game_framework.frame_time) % state.nFrame
        if self.isFall:
            self.frame = min(self.frame, state.nFrame - 1)

    def get_bb(self):
        frame = int(self.frame)
        state = self.state_machine.state
        return self.x - state.FRAME_INFO[frame][2] * self.size // 2, self.y, self.x + state.FRAME_INFO[frame][
            2] * self.size // 2, self.y + state.FRAME_INFO[frame][3] * self.size

    def handle_collision(self, group, other):
        pass

    def hit(self, damage, rigid=0, knock_up=0, knock_back=0, atk_pos=None):
        self.ultimate_gage = min(self.ultimate_gage + damage / 200, 3)
        if self.state_machine.state == Defense:
            if (self.face_dir == "r" and atk_pos > self.x) or (self.face_dir == "l" and atk_pos < self.x):
                damage /= 2
                self.speed[0] = knock_back / 2
            else:
                self.state_machine.handle_event(("DEFENSE_FAIL", 0))
        self.state_machine.handle_event(("HIT", 0))
        if self.state_machine.state == Hit:
            self.rigid_time += rigid * self.resist_coefficient * self.resist_coefficient ** self.rigid_time
            self.speed[1] += 6 * (Mario.maxHp / (self.hp + Mario.maxHp)) * (damage + 2) / self.weight * 2 * knock_up
            self.speed[0] = knock_back
        self.hp -= damage


class AtkBox:
    def __init__(self, mario):
        self.box_info = None
        self.ATK_INFO = (0, 0, 0, 0)
        self.effect = None
        self.mario = mario
        self.x = None

    def get_bb(self):
        if self.box_info:
            if self.mario.face_dir == "l":
                atkX, atkY = self.mario.x - self.box_info[0], self.mario.y + self.box_info[1]
            else:
                atkX, atkY = self.mario.x + self.box_info[0], self.mario.y + self.box_info[1]
            return atkX - self.box_info[2], atkY - self.box_info[3], atkX + self.box_info[2], atkY + self.box_info[3]

    def set_info(self, D, R, U, B):
        self.ATK_INFO = (D, R, U, B)

    def handle_collision(self, group, other):
        if other.control_method.isHit(group):
            if self.ATK_INFO[0] > 0:
                other.hit(*self.ATK_INFO, atk_pos=self.x)
                if self.effect == "reflect":
                    if other.face_dir == "l":
                        other.face_dir = "r"
                    else:
                        other.face_dir = "l"
                    other.dir *= -1
                    other.debuff_time = 5
                    other.debuff = "confusion"
                self.mario.ultimate_gage = min(self.mario.ultimate_gage + self.ATK_INFO[0] / 100, 3)
                self.reset()

    def reset(self):
        self.box_info = None
        self.ATK_INFO = (0, 0, 0, 0)
        self.effect = None
