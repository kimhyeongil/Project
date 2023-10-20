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


class StateMachine:
    def __init__(self, mario):
        self.state = Jump
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
