from pico2d import load_image

import game_framework
import game_world
import megamen_projectile


class Idle:
    l = [16, 16, 16, 52, 52, ]
    t = [115, 115, 115, 115, 115, ]
    w = [31, 31, 31, 31, 31]
    h = [45, 45, 45, 45, 45]
    nFrame = len(l)
    for i in range(len(t)):
        t[i] += h[i]
    FRAME_PER_SEC = 4

    @staticmethod
    def enter(megamen):
        megamen.frame = 0
        megamen.speed = [0, 0]
        megamen.dir = 0

    @staticmethod
    def do(megamen):
        megamen.frame = (megamen.frame + Idle.FRAME_PER_SEC * game_framework.frame_time) % Idle.nFrame

    @staticmethod
    def exit(megamen):
        pass


class RUN_ATK1:
    l = [62, 110, 218, 170, 239, 287, 334, 314, 394, 464]
    t = [457, 456, 334, 458, 458, 457, 456, 328, 457, 458]
    w = [42, 39, 44, 46, 45, 42, 40, 44, 46, 45]
    h = [43, 44, 44, 43, 43, 44, 45, 44, 42, 42]
    nFrame = len(l)
    for i in range(len(t)):
        t[i] += h[i]

    FRAME_PER_SEC = 12
    RUN_SPEED = 2.5

    @staticmethod
    def enter(megamen):
        megamen.frame = 0
        megamen.speed[0] = RUN_ATK1.RUN_SPEED * megamen.dir

    @staticmethod
    def do(megamen):
        isRepeat = False if int(megamen.frame) == 0 else True
        isShot = False if int(megamen.frame) % 4 == 0 else True
        megamen.frame = (megamen.frame + RUN_ATK1.FRAME_PER_SEC * game_framework.frame_time) % RUN_ATK1.nFrame
        if int(megamen.frame) % 4 == 0 and isShot and int(megamen.frame) != 0:
            game_world.add_obj(
                megamen_projectile.MegaBuster(megamen.x + RUN_ATK1.w[int(megamen.frame)] * megamen.dir,
                                              megamen.y + RUN_ATK1.h[int(megamen.frame)] * megamen.size // 2,
                                              megamen.dir), 1)
        if int(megamen.frame) == 0 and isRepeat:
            if megamen.dir == 0:
                megamen.state_machine.state = Idle
            else:
                megamen.state_machine.state = Run
            megamen.state_machine.state.enter(megamen)

    @staticmethod
    def exit(megamen):
        pass


class Run:
    l = [101, 149, 189, 232, 278, 326, 373, 414, 457, 503]
    t = [185, 184, 185, 186, 186, 185, 184, 185, 186, 186]
    w = [30, 27, 37, 42, 37, 30, 28, 33, 40, 38]
    h = [43, 44, 44, 43, 43, 44, 45, 44, 42, 42]
    nFrame = len(l)
    for i in range(len(t)):
        t[i] += h[i]

    RUN_SPEED = 2.5
    FRAME_PER_SEC = 12

    @staticmethod
    def exit(megamen):
        pass

    @staticmethod
    def enter(megamen):
        megamen.frame = 0
        if megamen.dir == 1:
            megamen.speed[0] = Run.RUN_SPEED
            megamen.face_dir = "r"
        else:
            megamen.speed[0] = -Run.RUN_SPEED
            megamen.face_dir = "l"

    @staticmethod
    def do(megamen):
        megamen.frame = (megamen.frame + Run.FRAME_PER_SEC * game_framework.frame_time) % Run.nFrame


class Jump:
    l = [16, 55, 98, 142, 184, 226, 268]
    t = [268, 263, 262, 266, 273, 274, 273]
    w = [32, 36, 37, 33, 38, 38, 38]
    h = [44, 49, 50, 46, 39, 39, 39]
    nFrame = len(l)
    for i in range(len(t)):
        t[i] += h[i]

    JUMP_POWER = 15
    FRAME_PER_SEC = 8

    @staticmethod
    def exit(megamen):
        pass

    @staticmethod
    def enter(mario):
        mario.frame = 0
        mario.speed[1] = Jump.JUMP_POWER

    @staticmethod
    def do(mario):
        mario.frame = (mario.frame + Jump.FRAME_PER_SEC * game_framework.frame_time) % Jump.nFrame
        if mario.y > game_world.ground:
            if int(mario.frame) > 2:
                mario.frame = 2
        else:
            if int(mario.frame) == 0:
                if mario.dir == 0:
                    mario.state_machine.state = Idle
                else:
                    mario.state_machine.state = Run
                mario.state_machine.state.enter(mario)


class ATK1:
    l = [13, 62, 113, 163, 214, 265]
    t = [399, 399, 399, 399, 399, 399]
    w = [44, 46, 44, 45, 46, 44]
    h = [44, 44, 44, 44, 44, 44]
    nFrame = len(l)
    for i in range(len(t)):
        t[i] += h[i]

    FRAME_PER_SEC = 6

    @staticmethod
    def exit(megamen):
        pass

    @staticmethod
    def enter(megamen):
        megamen.frame = 0
        megamen.speed[0] = 0

    @staticmethod
    def do(megamen):
        isRepeat = False if int(megamen.frame) == 0 else True
        isShot = False if int(megamen.frame) % 2 == 0 else True
        megamen.frame = (megamen.frame + ATK1.FRAME_PER_SEC * game_framework.frame_time) % ATK1.nFrame
        if int(megamen.frame) % 2 == 0 and isShot and int(megamen.frame) != 0:
            if megamen.face_dir == "r":
                game_world.add_obj(
                    megamen_projectile.MegaBuster(
                        megamen.x + ATK1.w[int(megamen.frame)],
                        megamen.y + ATK1.h[int(megamen.frame)] * megamen.size // 2, 1), 1)
            else:
                game_world.add_obj(
                    megamen_projectile.MegaBuster(
                        megamen.x - ATK1.w[int(megamen.frame)],
                        megamen.y + ATK1.h[int(megamen.frame)] * megamen.size // 2, -1), 1)
        if int(megamen.frame) == 0 and isRepeat:
            if megamen.dir == 0:
                megamen.state_machine.state = Idle
            else:
                megamen.state_machine.state = Run
            megamen.state_machine.state.enter(megamen)


class UP_ATK1:
    l = [20, 56, 97, 130]
    t = [861, 864, 847, 843]
    w = [29, 35, 24, 21, ]
    h = [42, 39, 56, 56]
    nFrame = len(l)
    for i in range(len(t)):
        t[i] += h[i]

    FRAME_PER_SEC = 13
    JUMP_POWER = 13

    @staticmethod
    def exit(megamen):
        pass

    @staticmethod
    def enter(megamen):
        megamen.frame = 0
        megamen.speed[0] = 0

    @staticmethod
    def do(megamen):
        isRepeat = False if int(megamen.frame) == 0 else True
        megamen.frame = (megamen.frame + UP_ATK1.FRAME_PER_SEC * game_framework.frame_time) % UP_ATK1.nFrame
        if megamen.y > game_world.ground:
            if int(megamen.frame) >= 3:
                megamen.frame = 3
        elif int(megamen.frame) == 0 and isRepeat:
            if megamen.dir == 0:
                megamen.state_machine.state = Idle
            else:
                megamen.state_machine.state = Run
            megamen.state_machine.state.enter(megamen)
        elif int(megamen.frame) == 1:
            megamen.speed[1] = UP_ATK1.JUMP_POWER


class ATK2:
    l = [355]
    t = [443]
    w = [47]
    h = [42]

    nFrame = 1
    FRAME_PER_SEC = 6
    start_time = 0

    projectile = None

    @staticmethod
    def enter(megamen):
        megamen.frame = 0
        megamen.speed[0] = 0
        ATK2.start_time = game_framework.time.time()
        if megamen.face_dir == 'r':
            ATK2.projectile = megamen_projectile.ChargeShot(megamen.x + ATK2.w[0] * megamen.size // 2,
                                                            megamen.y + megamen.size * ATK2.h[0] // 2, 1)
        else:
            ATK2.projectile = megamen_projectile.ChargeShot(megamen.x - ATK2.w[0] * megamen.size // 2,
                                                            megamen.y + megamen.size * ATK2.h[0] // 2, -1)
        ATK2.projectile.frame = 0
        ATK2.projectile.speed = 0
        game_world.add_obj(ATK2.projectile, 1)

    @staticmethod
    def do(megamen):
        if game_framework.time.time() - ATK2.start_time >= 1:
            ATK2.projectile.frame = 1

    @staticmethod
    def exit(megamen):
        game_world.erase_obj(ATK2.projectile)
        if megamen.face_dir == 'r':
            projectile = megamen_projectile.ChargeShot(megamen.x + ATK2.w[0] * megamen.size // 2,
                                                       megamen.y + megamen.size * ATK2.h[0] // 2, 1)
        else:
            projectile = megamen_projectile.ChargeShot(megamen.x - ATK2.w[0] * megamen.size // 2,
                                                       megamen.y + megamen.size * ATK2.h[0] // 2, -1)
        projectile.size = min(game_framework.time.time() - ATK2.start_time, 2)
        game_world.add_obj(projectile, 1)


# game_world.add_obj(megamen, 1)


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


class Tornado:
    l = [22, 60, 102, 134, 174, 216, 253, 292, 336, 380, 424]
    t = [1744, 1744, 1744, 1744, 1744, 1744, 1747, 1751, 1751, 1750, 1745]
    w = [34, 37, 26, 31, 34, 26, 31, 40, 38, 38, 34]
    h = [50, 50, 50, 50, 50, 50, 47, 40, 40, 39, 44]
    nFrame = len(l)
    for i in range(len(t)):
        t[i] += h[i]

    @staticmethod
    def enter(megamen, e):
        megamen.frame = 0
        game_world.add_obj(megamen_projectile.MegaTornado(megamen.x, megamen.y + Tornado.h[megamen.frame], 100), 1)

    @staticmethod
    def do(megamen):
        megamen.frame = (megamen.frame + 1) % Tornado.nFrame


class JumpShot:
    l = [13, 52, 95, 139, 181, 223, 265]
    t = [521, 516, 515, 519, 526, 527, 526]
    w = [37, 38, 39, 38, 40, 40, 40]
    h = [44, 49, 50, 46, 39, 38, 39]
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
                                                     megamen.y + JumpShot.h[megamen.frame] // 2), 1)

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
        self.state = Idle
        self.megamen = megamen
        self.table = {Idle: {megamen.control_method.move_r_down: Run, megamen.control_method.move_l_down: Run,
                             megamen.control_method.move_r_up: Run, megamen.control_method.move_l_up: Run,
                             megamen.control_method.jump_down: Jump,
                             megamen.control_method.atk1_down: ATK1,
                             megamen.control_method.atk2_down: ATK2},
                      Run: {megamen.control_method.move_r_down: Idle, megamen.control_method.move_l_down: Idle,
                            megamen.control_method.move_r_up: Idle, megamen.control_method.move_l_up: Idle,
                            megamen.control_method.jump_down: Jump,
                            megamen.control_method.atk1_down: RUN_ATK1,
                            megamen.control_method.atk2_down: RUN_ATK1
                            },
                      Jump: {},
                      RUN_ATK1: {megamen.control_method.move_r_down: Idle, megamen.control_method.move_l_down: Idle,
                                 megamen.control_method.move_r_up: Idle, megamen.control_method.move_l_up: Idle},
                      ATK2: {megamen.control_method.atk2_up: Idle},
                      Tornado: {}}

    def start(self):
        self.state.enter(self.megamen)

    def draw(self):
        frame = int(self.megamen.frame)
        if self.megamen.face_dir == "r":
            self.megamen.img.clip_draw(
                self.state.l[frame],
                self.megamen.img.h - self.state.t[frame],
                self.state.w[frame],
                self.state.h[frame],
                self.megamen.x,
                self.megamen.y + self.megamen.size * self.state.h[frame] // 2,
                self.state.w[frame] * self.megamen.size,
                self.state.h[frame] * self.megamen.size
            )
        elif self.megamen.face_dir == "l":
            self.megamen.img.clip_composite_draw(
                self.state.l[frame],
                self.megamen.img.h - self.state.t[frame],
                self.state.w[frame],
                self.state.h[frame],
                0, 'h',
                self.megamen.x,
                self.megamen.y + self.megamen.size * self.state.h[frame] // 2,
                self.state.w[frame] * self.megamen.size,
                self.state.h[frame] * self.megamen.size
            )

    def update(self):
        self.megamen.move()
        self.state.do(self.megamen)

    def handle_events(self, e):
        if self.megamen.control_method.up_down(("INPUT", e)):
            self.megamen.up = True
        elif self.megamen.control_method.up_up(("INPUT", e)):
            self.megamen.up = False
        elif self.megamen.control_method.move_r_down(("INPUT", e)) or self.megamen.control_method.move_l_up(
                ("INPUT", e)):
            self.megamen.dir += 1
        elif self.megamen.control_method.move_l_down(("INPUT", e)) or self.megamen.control_method.move_r_up(
                ("INPUT", e)):
            self.megamen.dir -= 1
        if self.table.get(self.state) != None:
            for check, next_state in self.table[self.state].items():
                if check(("INPUT", e)):
                    if self.megamen.up:
                        if next_state == ATK1 or next_state == RUN_ATK1:
                            next_state = UP_ATK1
                        elif next_state == ATK2:
                            next_state = UP_ATK2
                    self.state.exit(self.megamen)
                    self.state = next_state
                    self.state.enter(self.megamen)


class MegaMen:
    img = None

    def __init__(self, control_method):
        self.x, self.y = control_method.x, game_world.ground
        self.frame = 0
        self.size = 2
        self.dir = 0
        self.speed = [0, 0]
        self.face_dir = control_method.start_face
        self.control_method = control_method
        self.state_machine = StateMachine(self)
        self.up = False
        if MegaMen.img == None:
            MegaMen.img = load_image('megamen.png')

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
