from pico2d import load_image

import game_world
import megabuster


class Idle:
    l = [16, 16, 16, 52, 52, ]
    t = [115, 115, 115, 115, 115, ]
    w = [31, 31, 31, 31, 31]
    h = [45, 45, 45, 45, 45]
    nFrame = len(l)
    for i in range(len(t)):
        t[i] += h[i]

    @staticmethod
    def enter(megamen, e):
        megamen.frame = 0

    @staticmethod
    def do(megemen):
        megemen.frame = (megemen.frame + 1) % Idle.nFrame

    @staticmethod
    def draw(megemen):
        megemen.img.clip_draw(
            Idle.l[megemen.frame],
            megemen.img.h - Idle.t[megemen.frame],
            Idle.w[megemen.frame],
            Idle.h[megemen.frame],
            megemen.x,
            megemen.y,
            Idle.w[megemen.frame] * megemen.size,
            Idle.h[megemen.frame] * megemen.size,
        )


class RunShot:
    l = [62, 110, 218, 170, 239, 287, 334, 314, 394, 464]
    t = [457, 456, 334, 458, 458, 457, 456, 328, 457, 458]
    w = [42, 39, 44, 46, 45, 42, 40, 44, 46, 45]
    h = [43, 44, 44, 43, 43, 44, 45, 44, 42, 42]
    nFrame = len(l)
    for i in range(len(t)):
        t[i] += h[i]

    @staticmethod
    def enter(megamen, e):
        megamen.frame = 0

    @staticmethod
    def do(megamen):
        megamen.frame = (megamen.frame + 1) % RunShot.nFrame
        if megamen.frame == 3 or megamen.frame == 8:
            game_world.add_obj(megabuster.MegaBuster(megamen.x + RunShot.w[megamen.frame], megamen.y), 1)

    @staticmethod
    def draw(megamen):
        megamen.img.clip_draw(
            RunShot.l[megamen.frame],
            megamen.img.h - RunShot.t[megamen.frame],
            RunShot.w[megamen.frame],
            RunShot.h[megamen.frame],
            megamen.x,
            megamen.y,
            RunShot.w[megamen.frame] * megamen.size,
            RunShot.h[megamen.frame] * megamen.size,
        )


class Run:
    l = [101, 149, 189, 232, 278, 326, 373, 414, 457, 503]
    t = [185, 184, 185, 186, 186, 185, 184, 185, 186, 186]
    w = [30, 27, 37, 42, 37, 30, 28, 33, 40, 38]
    h = [43, 44, 44, 43, 43, 44, 45, 44, 42, 42]
    nFrame = len(l)
    for i in range(len(t)):
        t[i] += h[i]

    @staticmethod
    def enter(megamen, e):
        megamen.frame = 0

    @staticmethod
    def do(megamen):
        megamen.frame = (megamen.frame + 1) % Run.nFrame

    @staticmethod
    def draw(megamen):
        megamen.img.clip_draw(
            Run.l[megamen.frame],
            megamen.img.h - Run.t[megamen.frame],
            Run.w[megamen.frame],
            Run.h[megamen.frame],
            megamen.x,
            megamen.y,
            Run.w[megamen.frame] * megamen.size,
            Run.h[megamen.frame] * megamen.size,
        )


class Jump:
    l = [16, 55, 98, 142, 184, 226, 268]
    t = [268, 263, 262, 266, 273, 274, 273]
    w = [32, 36, 37, 33, 38, 38, 38]
    h = [44, 49, 50, 46, 39, 39, 39]
    nFrame = len(l)
    for i in range(len(t)):
        t[i] += h[i]

    @staticmethod
    def enter(megamen, e):
        megamen.frame = 0

    @staticmethod
    def do(megamen):
        megamen.frame = (megamen.frame + 1) % Jump.nFrame

    @staticmethod
    def draw(megamen):
        megamen.img.clip_draw(
            Jump.l[megamen.frame],
            megamen.img.h - Jump.t[megamen.frame],
            Jump.w[megamen.frame],
            Jump.h[megamen.frame],
            megamen.x,
            megamen.y,
            Jump.w[megamen.frame] * megamen.size,
            Jump.h[megamen.frame] * megamen.size,
        )


class SmallShot:
    l = [13, 62, 113, 163, 214, 265]
    t = [399, 399, 399, 399, 399, 399]
    w = [44, 46, 44, 45, 46, 44]
    h = [44, 44, 44, 44, 44, 44]
    nFrame = len(l)
    for i in range(len(t)):
        t[i] += h[i]

    @staticmethod
    def enter(megamen, e):
        megamen.frame = 0

    @staticmethod
    def do(megamen):
        megamen.frame = (megamen.frame + 1) % SmallShot.nFrame
        if megamen.frame == 3:
            game_world.add_obj(megabuster.MegaBuster(megamen.x + SmallShot.w[megamen.frame], megamen.y), 1)

    @staticmethod
    def draw(megamen):
        megamen.img.clip_draw(
            SmallShot.l[megamen.frame],
            megamen.img.h - SmallShot.t[megamen.frame],
            SmallShot.w[megamen.frame],
            SmallShot.h[megamen.frame],
            megamen.x,
            megamen.y,
            SmallShot.w[megamen.frame] * megamen.size,
            SmallShot.h[megamen.frame] * megamen.size,
        )


class Upper:
    l = [20, 56, 97, 130]
    t = [861, 864, 847, 843]
    w = [29, 35, 24, 21, ]
    h = [42, 39, 56, 56]
    nFrame = len(l)
    for i in range(len(t)):
        t[i] += h[i]

    @staticmethod
    def enter(megamen, e):
        megamen.frame = 0

    @staticmethod
    def do(megamen):
        megamen.frame = (megamen.frame + 1) % Upper.nFrame

    @staticmethod
    def draw(megamen):
        megamen.img.clip_draw(
            Upper.l[megamen.frame],
            megamen.img.h - Upper.t[megamen.frame],
            Upper.w[megamen.frame],
            Upper.h[megamen.frame],
            megamen.x,
            megamen.y,
            Upper.w[megamen.frame] * megamen.size,
            Upper.h[megamen.frame] * megamen.size,
        )


class FireSword:
    l = [23, 67, 123, 185, 248, 309, ]
    t = [1416, 1418, 1417, 1415, 1419, 1416, ]
    w = [37, 35, 57, 56, 54, 54, ]
    h = [46, 44, 55, 55, 45, 46, ]
    nFrame = len(l)
    for i in range(len(t)):
        t[i] += h[i]

    @staticmethod
    def enter(megamen, e):
        megamen.frame = 0

    @staticmethod
    def do(megamen):
        megamen.frame = (megamen.frame + 1) % FireSword.nFrame

    @staticmethod
    def draw(megamen):
        megamen.img.clip_draw(
            FireSword.l[megamen.frame],
            megamen.img.h - FireSword.t[megamen.frame],
            FireSword.w[megamen.frame],
            FireSword.h[megamen.frame],
            megamen.x,
            megamen.y,
            FireSword.w[megamen.frame] * megamen.size,
            FireSword.h[megamen.frame] * megamen.size,
        )


class Tornado:
    l = [22, 60, 102, 134, 174, 216, 253, 292, 336, 380, 424]
    t = [1744, 1744, 1744, 1744, 1744, 1744, 1747, 1751, 1751, 1750, 1745]
    w = [34, 37, 26, 31, 34, 26, 31, 40, 38, 38, 34]
    h = [50, 50, 50, 50, 50, 50, 47, 40, 40, 39, 44]
    nFrame = len(l)
    for i in range(len(t)):
        t[i] += h[i]
    tornado_l = [534, 613, 697]
    tornado_t = [1735, 1732, 1732]
    tornado_w = [71, 72, 66]
    tornado_h = [58, 66, 59]

    for i in range(len(tornado_t)):
        tornado_t[i] += tornado_h[i]

    @staticmethod
    def enter(megamen, e):
        megamen.frame = 0

    @staticmethod
    def do(megamen):
        megamen.frame = (megamen.frame + 1) % Tornado.nFrame

    @staticmethod
    def draw(megamen):
        if megamen.frame < 7:
            megamen.img.clip_draw(
                Tornado.tornado_l[megamen.frame % 3],
                megamen.img.h - Tornado.tornado_t[megamen.frame % 3],
                Tornado.tornado_w[megamen.frame % 3],
                Tornado.tornado_h[megamen.frame % 3],
                megamen.x,
                megamen.y,
                Tornado.tornado_w[megamen.frame % 3] * megamen.size,
                Tornado.tornado_h[megamen.frame % 3] * megamen.size,
            )
        megamen.img.clip_draw(
            Tornado.l[megamen.frame],
            megamen.img.h - Tornado.t[megamen.frame],
            Tornado.w[megamen.frame],
            Tornado.h[megamen.frame],
            megamen.x,
            megamen.y + Tornado.h[megamen.frame] - Tornado.h[0],
            Tornado.w[megamen.frame] * megamen.size,
            Tornado.h[megamen.frame] * megamen.size,
        )


class JumpShot:
    l = [13,52,95,139,181,223,265]
    t = [521,516,515,519,526,527,526]
    w = [37,38,39,38,40,40,40]
    h = [44,49,50,46,39,38,39]
    nFrame = len(l)
    for i in range(len(t)):
        t[i] += h[i]

    @staticmethod
    def enter(megamen, e):
        megamen.frame = 0

    @staticmethod
    def do(megamen):
        megamen.frame = (megamen.frame + 1) % JumpShot.nFrame
        if megamen.frame == 2:
            game_world.add_obj(megabuster.MegaBuster(megamen.x + JumpShot.w[megamen.frame],
                                                     megamen.y + JumpShot.h[megamen.frame] // 2),1)

    @staticmethod
    def draw(megamen):
        megamen.img.clip_draw(
            JumpShot.l[megamen.frame],
            megamen.img.h - JumpShot.t[megamen.frame],
            JumpShot.w[megamen.frame],
            JumpShot.h[megamen.frame],
            megamen.x,
            megamen.y + JumpShot.h[megamen.frame] - JumpShot.h[0],
            JumpShot.w[megamen.frame] * megamen.size,
            JumpShot.h[megamen.frame] * megamen.size,
        )


class StateMachine:
    def __init__(self, megamen):
        self.state = RunShot
        self.megamen = megamen

    def draw(self):
        self.state.draw(self.megamen)

    def update(self):
        self.state.do(self.megamen)


class MegaMen:
    img = None

    def __init__(self):
        self.x, self.y = 400, 300
        self.frame = 0
        self.size = 2
        self.state_machine = StateMachine(self)
        if MegaMen.img == None:
            MegaMen.img = load_image('megamen.png')

    def draw(self):
        self.state_machine.draw()

    def update(self):
        self.state_machine.update()
