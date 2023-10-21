from pico2d import *


class Idle:
    l = [16,16,16,52,52,]
    t = [115,115,115,115,115,]
    w = [31,31,31,31,31]
    h = [45,45,45,45,45]
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
            Idle.h[mario.frame],
            mario.x,
            mario.y,
            Attack2.w[mario.frame] * mario.size,
            Attack2.h[mario.frame] * mario.size,
        )


class Run:
    l = [101,149,189,232,278,326,373,414,457,503]
    t = [185,184,185,186,186,185,184,185,186,186]
    w = [30,27,37,42,37,30,28,33,40,38]
    h = [43,44,44,43,43,44,45,44,42,42]
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
    l = [15, 15, 45, 45, 45, 45, 45, 45, 78, 78, 111, 141, 141, 171]
    t = [84, 84, 84, 84, 84, 84, 84, 84, 84, 84, 92, 93, 93, 92]
    w = [24, 24, 27, 27, 27, 27, 27, 27, 29, 29, 26, 26, 26, 26]
    h = [40, 40, 39, 39, 39, 39, 39, 39, 42, 42, 34, 33, 33, 34]
    nFrame = len(l)
    for i in range(len(t)):
        t[i] += h[i]

    @staticmethod
    def enter(mario, e):
        mario.frame = 0

    @staticmethod
    def do(mario):
        mario.frame = (mario.frame + 1) % Jump.nFrame

    @staticmethod
    def draw(mario):
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
    def __init__(self, megemen):
        self.state = Run
        self.megemen = megemen

    def draw(self):
        self.state.draw(self.megemen)

    def update(self):
        self.state.do(self.megemen)


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
