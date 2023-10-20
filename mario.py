from pico2d import *


class Idle:
    l = [18, 18, 45, 45, 72, 72, 99, 99, 126, 126, 153, 153, 126, 126, 99, 99, 72, 72, 45, 45]
    t = [25, 25, 24, 24, 23, 23, 23, 23, 24, 24, 25, 25, 24, 24, 23, 23, 23, 23, 24, 24]
    w = [23, 23, 23, 23, 23, 23, 24, 24, 25, 25, 25, 25, 25, 25, 24, 24, 23, 23, 23, 23]
    h = [36, 36, 37, 37, 38, 38, 38, 38, 37, 37, 36, 36, 37, 37, 38, 38, 38, 38, 37, 37]
    nFrame = len(l)
    for i in range(len(t)):
        t[i] += h[i]

    @staticmethod
    def enter(mario, e):
        mario.frame = 0

    @staticmethod
    def do(mario):
        mario.frame = (mario.frame + 1) % Idle.nFrame

    @staticmethod
    def draw(mario):
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
        mario.frame = 0

    @staticmethod
    def do(mario):
        mario.frame = (mario.frame + 1) % Run.nFrame

    @staticmethod
    def draw(mario):
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


class StateMachine:
    def __init__(self, mario):
        self.state = Attack1
        self.mario = mario

    def draw(self):
        self.state.draw(self.mario)

    def update(self):
        self.state.do(self.mario)


class Mario:
    img = None

    def __init__(self):
        self.x, self.y = 400, 300
        self.frame = 0
        self.size = 2
        self.state_machine = StateMachine(self)
        if Mario.img == None:
            Mario.img = load_image('mario.png')

    def draw(self):
        self.state_machine.draw()

    def update(self):
        self.state_machine.update()
