from pico2d import *

import game_world


class Idle:
    l = [18, 45, 72, 99, 126, 153, 126, 99, 72, 45]
    t = [25, 24, 23, 23, 24, 25, 24, 23, 23, 24]
    w = [23, 23, 23, 24, 25, 25, 25, 24, 23, 23]
    h = [36, 37, 38, 38, 37, 36, 37, 38, 38, 37]
    nFrame = len(l)
    for i in range(len(t)):
        t[i] += h[i]

    @staticmethod
    def enter(mario, e):
        mario.frame = 0
        mario.speed = [0, 0]

    @staticmethod
    def do(mario):
        mario.frame = (mario.frame + 1) % Idle.nFrame

    @staticmethod
    def draw(mario):
        if mario.face_dir == "r":
            mario.img.clip_draw(
                Idle.l[mario.frame],
                mario.img.h - Idle.t[mario.frame],
                Idle.w[mario.frame],
                Idle.h[mario.frame],
                mario.x,
                mario.y,
                Idle.w[mario.frame] * mario.size,
                Idle.h[mario.frame] * mario.size,
            )
        elif mario.face_dir == "l":
            mario.img.clip_composite_draw(
                Idle.l[mario.frame],
                mario.img.h - Idle.t[mario.frame],
                Idle.w[mario.frame],
                Idle.h[mario.frame],
                0, 'h',
                mario.x,
                mario.y,
                Idle.w[mario.frame] * mario.size,
                Idle.h[mario.frame] * mario.size,
            )


class Attack2:
    l = [14, 14, 46, 46, 97, 142, 184, 224, 262, 301, 340, 340, 340]
    t = [999, 999, 1003, 1003, 1004, 1002, 1000, 1001, 1003, 1004, 1001, 1001, 1001]
    w = [26, 26, 45, 45, 39, 36, 34, 32, 33, 33, 25, 25, 25]
    h = [36, 36, 32, 32, 31, 33, 35, 34, 32, 31, 34, 34, 34]
    nFrame = len(l)
    for i in range(len(t)):
        t[i] += h[i]

    @staticmethod
    def enter(mario, e):
        mario.frame = 0

    @staticmethod
    def do(mario):
        mario.frame = (mario.frame + 1) % Attack2.nFrame

    @staticmethod
    def draw(mario):
        mario.img.clip_draw(
            Attack2.l[mario.frame],
            mario.img.h - Attack2.t[mario.frame],
            Attack2.w[mario.frame],
            Attack2.h[mario.frame],
            mario.x,
            mario.y,
            Attack2.w[mario.frame] * mario.size,
            Attack2.h[mario.frame] * mario.size,
        )


class Run:
    l = [12, 44, 82, 116, 146, 181, 220, 254]
    t = [148, 148, 149, 151, 149, 150, 149, 151]
    w = [28, 30, 29, 24, 28, 30, 28, 24]
    h = [36, 34, 36, 36, 36, 34, 36, 36]
    nFrame = len(l)
    for i in range(len(t)):
        t[i] += h[i]

    @staticmethod
    def enter(mario, e):
        if mario.control_method.move_r_down(e) or mario.control_method.move_l_up(e):
            mario.face_dir = "r"
            mario.speed[0] = 100
        elif mario.control_method.move_l_down(e) or mario.control_method.move_r_up(e):
            mario.face_dir = "l"
            mario.speed[0] = -100
        mario.frame = 0

    @staticmethod
    def do(mario):
        mario.frame = (mario.frame + 1) % Run.nFrame
        mario.x += mario.speed[0] * game_world.time_slice

    @staticmethod
    def draw(mario):
        if mario.face_dir == "r":
            mario.img.clip_draw(
                Run.l[mario.frame],
                mario.img.h - Run.t[mario.frame],
                Run.w[mario.frame],
                Run.h[mario.frame],
                mario.x,
                mario.y,
                Run.w[mario.frame] * mario.size,
                Run.h[mario.frame] * mario.size,
            )
        elif mario.face_dir == "l":
            mario.img.clip_composite_draw(
                Run.l[mario.frame],
                mario.img.h - Run.t[mario.frame],
                Run.w[mario.frame],
                Run.h[mario.frame],
                0, 'h',
                mario.x,
                mario.y,
                Run.w[mario.frame] * mario.size,
                Run.h[mario.frame] * mario.size,
            )


class Jump:
    l = [15, 45, 45, 45, 78, 111, 141, 171]
    t = [84, 84, 84, 84, 84, 92, 93, 92]
    w = [24, 27, 27, 27, 29, 26, 26, 26]
    h = [40, 39, 39, 39, 42, 34, 33, 34]
    nFrame = len(l)
    for i in range(len(t)):
        t[i] += h[i]

    @staticmethod
    def enter(mario, e):
        mario.frame = 0
        mario.speed[1] = 300

    @staticmethod
    def do(mario):
        mario.frame = (mario.frame + 1) % Jump.nFrame
        mario.x += mario.speed[0] * game_world.time_slice
        mario.y += mario.speed[1] * game_world.time_slice
        if mario.y > game_world.ground:
            mario.speed[1] -= game_world.g * game_world.time_slice
            if mario.frame > 4:
                mario.frame = 4
        else:
            mario.y = game_world.ground
            mario.speed[1] = 0
            if mario.frame == Jump.nFrame - 1:
                if mario.speed[0] == 0:
                    mario.state_machine.state = Idle
                    mario.state_machine.state.enter(mario, ("LAND", 0))
                else:
                    mario.state_machine.state = Run
                    mario.state_machine.state.enter(mario, ("LAND", 0))

    @staticmethod
    def draw(mario):
        if mario.face_dir == "r":
            mario.img.clip_draw(
                Jump.l[mario.frame],
                mario.img.h - Jump.t[mario.frame],
                Jump.w[mario.frame],
                Jump.h[mario.frame],
                mario.x,
                mario.y,
                Jump.w[mario.frame] * mario.size,
                Jump.h[mario.frame] * mario.size,
            )
        elif mario.face_dir == "l":
            mario.img.clip_composite_draw(
                Jump.l[mario.frame],
                mario.img.h - Jump.t[mario.frame],
                Jump.w[mario.frame],
                Jump.h[mario.frame],
                0, 'h',
                mario.x,
                mario.y,
                Jump.w[mario.frame] * mario.size,
                Jump.h[mario.frame] * mario.size,
            )



class Attack1:
    l = [12, 12, 54, 105, 152, 193, 233, 270, 307, 356, 356, 400, 400, 13, 13, 46, 46, 73, 73, 125, 125, 169, 169, 205,
         205, 232, 232]
    t = [261, 261, 263, 263, 263, 263, 261, 261, 263, 263, 263, 263, 263, 313, 310, 310, 310, 303, 303, 308, 308, 308,
         308, 308, 308, 314, 314]
    w = [36, 36, 48, 44, 34, 34, 31, 31, 44, 40, 40, 35, 35, 27, 27, 23, 23, 48, 48, 40, 40, 32, 32, 23, 23, 23, 26]
    h = [34, 34, 32, 32, 32, 32, 34, 34, 32, 32, 32, 32, 32, 34, 34, 36, 36, 43, 43, 38, 38, 38, 38, 37, 37, 33, 33]
    nFrame = len(l)
    for i in range(len(t)):
        t[i] += h[i]

    @staticmethod
    def enter(mario, e):
        mario.frame = 0

    @staticmethod
    def do(mario):
        mario.frame = (mario.frame + 1) % Attack1.nFrame

    @staticmethod
    def draw(mario):
        mario.img.clip_draw(
            Attack1.l[mario.frame],
            mario.img.h - Attack1.t[mario.frame],
            Attack1.w[mario.frame],
            Attack1.h[mario.frame],
            mario.x,
            mario.y,
            Attack1.w[mario.frame] * mario.size,
            Attack1.h[mario.frame] * mario.size,
        )


class Upper:
    l = [14, 14, 54, 54, 96, 54]
    t = [557, 557, 550, 550, 535, 550]
    w = [35, 35, 34, 34, 22, 34]
    h = [30, 30, 38, 38, 53, 38]
    nFrame = len(l)
    for i in range(len(t)):
        t[i] += h[i]

    @staticmethod
    def enter(mario, e):
        mario.frame = 0

    @staticmethod
    def do(mario):
        mario.frame = (mario.frame + 1) % Upper.nFrame

    @staticmethod
    def draw(mario):
        mario.img.clip_draw(
            Upper.l[mario.frame],
            mario.img.h - Upper.t[mario.frame],
            Upper.w[mario.frame],
            Upper.h[mario.frame],
            mario.x,
            mario.y,
            Upper.w[mario.frame] * mario.size,
            Upper.h[mario.frame] * mario.size,
        )


class SomersaultKick:
    l = [141, 141, 14, 57, 113, 156, 200, 244, 287, 316]
    t = [93, 93, 652, 644, 612, 632, 638, 645, 646, 647]
    w = [26, 26, 37, 50, 37, 38, 38, 37, 23, 29]
    h = [33, 33, 37, 26, 52, 32, 30, 31, 37, 42]
    nFrame = len(l)
    for i in range(len(t)):
        t[i] += h[i]

    @staticmethod
    def enter(mario, e):
        mario.frame = 0

    @staticmethod
    def do(mario):
        mario.frame = (mario.frame + 1) % SomersaultKick.nFrame

    @staticmethod
    def draw(mario):
        mario.img.clip_draw(
            SomersaultKick.l[mario.frame],
            mario.img.h - SomersaultKick.t[mario.frame],
            SomersaultKick.w[mario.frame],
            SomersaultKick.h[mario.frame],
            mario.x,
            mario.y,
            SomersaultKick.w[mario.frame] * mario.size,
            SomersaultKick.h[mario.frame] * mario.size,
        )


class MagicCape:
    l = [40, 80, 109, 168, 221, 275, 307, 340, 384, 418]
    t = [1337, 1337, 1336, 1340, 1322, 1321, 1336, 1339, 1340, 1340]
    w = [30, 23, 53, 47, 45, 26, 27, 38, 27, 25]
    h = [37, 37, 38, 34, 52, 53, 38, 35, 34, 34]
    nFrame = len(l)
    for i in range(len(t)):
        t[i] += h[i]

    @staticmethod
    def enter(mario, e):
        mario.frame = 0

    @staticmethod
    def do(mario):
        mario.frame = (mario.frame + 1) % MagicCape.nFrame

    @staticmethod
    def draw(mario):
        mario.img.clip_draw(
            MagicCape.l[mario.frame],
            mario.img.h - MagicCape.t[mario.frame],
            MagicCape.w[mario.frame],
            MagicCape.h[mario.frame],
            mario.x,
            mario.y + MagicCape.h[mario.frame] - MagicCape.h[0],
            MagicCape.w[mario.frame] * mario.size,
            MagicCape.h[mario.frame] * mario.size,
        )


class PalmStrike:
    l = [13, 43, 76, 108, 141, 141, 189, 232]
    t = [933, 931, 924, 926, 931, 931, 929, 932]
    w = [24, 27, 26, 27, 42, 42, 37, 25]
    h = [35, 32, 42, 40, 35, 35, 37, 34]
    nFrame = len(l)
    for i in range(len(t)):
        t[i] += h[i]

    @staticmethod
    def enter(mario, e):
        mario.frame = 0

    @staticmethod
    def do(mario):
        mario.frame = (mario.frame + 1) % PalmStrike.nFrame

    @staticmethod
    def draw(mario):
        mario.img.clip_draw(
            PalmStrike.l[mario.frame],
            mario.img.h - PalmStrike.t[mario.frame],
            PalmStrike.w[mario.frame],
            PalmStrike.h[mario.frame],
            mario.x,
            mario.y + PalmStrike.h[mario.frame] - PalmStrike.h[0],
            PalmStrike.w[mario.frame] * mario.size,
            PalmStrike.h[mario.frame] * mario.size,
        )


class StateMachine:
    def __init__(self, mario):
        self.state = Idle
        self.mario = mario
        self.table = {Idle: {mario.control_method.move_r_down: Run, mario.control_method.move_l_down: Run,
                             mario.control_method.move_r_up: Run, mario.control_method.move_l_up: Run,
                             mario.control_method.jump_down: Jump},
                      Run: {mario.control_method.move_r_down: Idle, mario.control_method.move_l_down: Idle,
                            mario.control_method.move_r_up: Idle, mario.control_method.move_l_up: Idle,
                            mario.control_method.jump_down: Jump
                            },
                      Jump: {}}

    def draw(self):
        self.state.draw(self.mario)

    def update(self):
        self.state.do(self.mario)

    def handle_events(self, e):
        for check, next_state in self.table[self.state].items():
            if check(("INPUT", e)):
                self.state = next_state
                self.state.enter(self.mario, ("INPUT", e))


class Mario:
    img = None

    def __init__(self, control_method):
        self.x, self.y = 400, 300
        self.frame = 0
        self.size = 2
        self.control_method = control_method
        self.face_dir = "r"
        self.speed = [0, 0]
        self.state_machine = StateMachine(self)
        if Mario.img == None:
            Mario.img = load_image('mario.png')

    def draw(self):
        self.state_machine.draw()

    def update(self):
        self.state_machine.update()
