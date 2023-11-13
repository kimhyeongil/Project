from pico2d import load_image, draw_rectangle
import game_framework
import game_world
import megamen_projectile
import play_sever


# state = CogwheelShot
# for i in range(len(state.l)):
#     print(f"({state.l[i]},{megamen.img.h - state.t[i] - state.h[i]},{state.w[i]},{state.h[i]},),")
# print(len(state.l))


def end_of_animation(e):
    return e[0] == "EOA"


def check_run(e):
    return e[0] == "CHECK_STATE" and e[1] != 0


def check_idle(e):
    return e[0] == "CHECK_STATE" and e[1] == 0


def land(e):
    return e[0] == "LAND"


class Land:
    frame = [
        (226, 1621, 38, 39),
        (268, 1622, 38, 39),
        (184, 1622, 38, 39), ]

    nFrame = 3
    FRAME_PER_SEC = 18

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
        megamen.next_frame()
        if int(megamen.frame) == 0 and isRepeat:
            megamen.state_machine.handle_event(("EOA", 0))


class AnimationEnd:
    @staticmethod
    def exit(megamen):
        pass

    @staticmethod
    def enter(megamen):
        megamen.frame = 0
        megamen.state_machine.handle_event(("CHECK_STATE", megamen.dir, megamen.up))


class Idle:
    frame = [(16, 1774, 31, 45),
             (52, 1774, 31, 45),
             (16, 1774, 31, 45), ]
    nFrame = 3
    FRAME_PER_SEC = 2

    @staticmethod
    def enter(megamen):
        megamen.speed = [0, 0]
        megamen.dir = 0

    @staticmethod
    def do(megamen):
        megamen.next_frame()

    @staticmethod
    def exit(megamen):
        pass


class RunShot:
    frame = [(62, 1434, 42, 43),
             (110, 1434, 39, 44),
             (218, 1556, 44, 44),
             (170, 1433, 46, 43),
             (239, 1433, 45, 43),
             (287, 1433, 42, 44),
             (334, 1433, 40, 45),
             (314, 1562, 44, 44),
             (394, 1435, 46, 42),
             (464, 1434, 45, 42), ]
    nFrame = 10

    FRAME_PER_SEC = 12
    RUN_SPEED = 2.5

    @staticmethod
    def exit(megamen):
        pass

    @staticmethod
    def enter(megamen):
        megamen.frame = 0
        megamen.speed[0] = Run.RUN_SPEED * megamen.dir
        if megamen.dir == 1:
            megamen.face_dir = "r"
        else:
            megamen.face_dir = "l"

    @staticmethod
    def do(megamen):
        isRepeat = False if int(megamen.frame) == 0 else True
        isShot = False if int(megamen.frame) % 4 == 0 else True
        megamen.next_frame()
        if int(megamen.frame) % 4 == 0 and isShot and int(megamen.frame) != 0:
            game_world.add_obj(
                megamen_projectile.MegaBuster(megamen.x + RunShot.frame[int(megamen.frame)][2] * megamen.dir,
                                              megamen.y + RunShot.frame[int(megamen.frame)][3] * megamen.size // 2,
                                              megamen.dir), 1)
        if int(megamen.frame) == 0 and isRepeat:
            megamen.state_machine.handle_event(("EOA", 0))


class Run:
    frame = [(101, 1706, 30, 43),
             (149, 1706, 27, 44),
             (189, 1705, 37, 44),
             (232, 1705, 42, 43),
             (278, 1705, 37, 43),
             (326, 1705, 30, 44),
             (373, 1705, 28, 45),
             (414, 1705, 33, 44),
             (457, 1706, 40, 42),
             (503, 1706, 38, 42), ]
    nFrame = 10

    RUN_SPEED = 2.5
    FRAME_PER_SEC = 12

    @staticmethod
    def exit(megamen):
        pass

    @staticmethod
    def enter(megamen):
        if megamen.dir == 1:
            megamen.speed[0] = Run.RUN_SPEED
            megamen.face_dir = "r"
        else:
            megamen.speed[0] = -Run.RUN_SPEED
            megamen.face_dir = "l"

    @staticmethod
    def do(megamen):
        megamen.next_frame()


class Jump:
    frame = [(16, 1622, 32, 44),
             (55, 1622, 36, 49),
             (98, 1622, 37, 50),
             (142, 1622, 33, 46),
             ]
    nFrame = 4

    JUMP_POWER = 15
    FRAME_PER_SEC = 8

    @staticmethod
    def exit(megamen):
        pass

    @staticmethod
    def enter(megamen):
        megamen.frame = 0
        megamen.isFall = True
        megamen.speed[1] = Jump.JUMP_POWER

    @staticmethod
    def do(megamen):
        megamen.next_frame()
        if megamen.isFall:
            megamen.frame = min(megamen.frame, 2)
        else:
            megamen.state_machine.handle_event(("LAND", 0))


class JumpKnuckle:
    frame = [(24, 305, 34, 46,),
             (66, 311, 40, 39,),
             (115, 306, 39, 45,),
             (166, 306, 34, 46,),
             (210, 308, 35, 47,),
             (255, 306, 37, 50,),
             ]
    nFrame = 6
    FRAME_PER_SEC = 8

    @staticmethod
    def exit(megamen):
        pass

    @staticmethod
    def enter(megamen):
        megamen.frame = 0

    @staticmethod
    def do(megamen):
        isShot = True if int(megamen.frame) == 2 else False
        megamen.next_frame()
        if not isShot and int(megamen.frame) == 2:
            knuckle = megamen_projectile.MegaKnuckle(megamen.x, megamen.y, megamen.size)
            game_world.add_collision_pair("knuckle:ground", knuckle, play_sever.ground)
            game_world.add_obj(knuckle, 1)
        if megamen.isFall:
            megamen.frame = min(megamen.frame, JumpKnuckle.nFrame - 1)
        else:
            megamen.state_machine.handle_event(("LAND", 0))


class SmallShot:
    frame = [(13, 1491, 44, 44),
             (62, 1491, 46, 44),
             (113, 1491, 44, 44),
             (163, 1491, 45, 44),
             (214, 1491, 46, 44),
             (265, 1491, 44, 44), ]
    nFrame = 6
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
        megamen.next_frame()
        if int(megamen.frame) % 2 == 0 and isShot and int(megamen.frame) != 0:
            megamen.fire_megabuster(SmallShot.frame[int(megamen.frame)][2],
                                    SmallShot.frame[int(megamen.frame)][3] * megamen.size // 2)
        if int(megamen.frame) == 0 and isRepeat:
            megamen.state_machine.handle_event(("EOA", 0))


class Uppercut:
    frame = [(20, 1031, 29, 42),
             (56, 1031, 35, 39),
             (97, 1031, 24, 56),
             (130, 1035, 21, 56), ]
    nFrame = 4

    FRAME_PER_SEC = 13
    JUMP_POWER = 13

    @staticmethod
    def get_bb(megamen):
        frame = int(megamen.frame)
        head = (megamen.x - Uppercut.frame[frame][2] * megamen.size // 3,
                megamen.y + Uppercut.frame[frame][3] * megamen.size // 2,
                megamen.x + Uppercut.frame[frame][2] * megamen.size // 3,
                megamen.y + Uppercut.frame[frame][3] * megamen.size)
        body = (megamen.x - Uppercut.frame[frame][2] * megamen.size // 2,
                megamen.y,
                megamen.x + Uppercut.frame[frame][2] * megamen.size // 2,
                megamen.y + Uppercut.frame[frame][3] * megamen.size // 2)
        hitbox = [head, body]
        return hitbox

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
        megamen.next_frame()
        if megamen.isFall:
            megamen.frame = min(megamen.frame, 3)
        else:
            if int(megamen.frame) == 0 and isRepeat:
                megamen.state_machine.handle_event(("LAND", 0))
            elif int(megamen.frame) == 1:
                megamen.isFall = True
                megamen.speed[1] = Uppercut.JUMP_POWER


class CogwheelShot:
    frame = [(27, 556, 31, 45,),
             (68, 556, 31, 45,),
             (111, 556, 42, 44,),
             (158, 556, 40, 41,),
             (205, 556, 34, 44,),
             (252, 556, 31, 45,), ]

    nFrame = 6
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
        isShot = True if int(megamen.frame) == 3 else False
        megamen.next_frame()
        if int(megamen.frame) == 3 and not isShot:
            megamen.fire_cogwheel(CogwheelShot.frame[int(megamen.frame)][2],
                                  CogwheelShot.frame[int(megamen.frame)][3] * megamen.size // 2)
        if int(megamen.frame) == 0 and isRepeat:
            megamen.state_machine.handle_event(("EOA", 0))


class ChargingShot:
    frame = [(355, 1491, 47, 42)]

    nFrame = 1
    FRAME_PER_SEC = 6
    start_time = 0

    projectile = None

    @staticmethod
    def enter(megamen):
        megamen.frame = 0
        megamen.speed[0] = 0
        ChargingShot.start_time = game_framework.time.time()
        if megamen.face_dir == 'r':
            ChargingShot.projectile = megamen_projectile.MegaChargingShot(
                megamen.x + ChargingShot.frame[0][2] * megamen.size // 2,
                megamen.y + megamen.size * ChargingShot.frame[0][3] // 2,
                1)
        else:
            ChargingShot.projectile = megamen_projectile.MegaChargingShot(
                megamen.x - ChargingShot.frame[0][2] * megamen.size // 2,
                megamen.y + megamen.size * ChargingShot.frame[0][3] // 2,
                -1)
        ChargingShot.projectile.frame = 0
        ChargingShot.projectile.speed = 0
        game_world.add_obj(ChargingShot.projectile, 1)

    @staticmethod
    def do(megamen):
        charged_time = game_framework.time.time() - ChargingShot.start_time
        if charged_time >= 0.5:
            ChargingShot.projectile.frame = 1
        if charged_time >= 2:
            ChargingShot.projectile.frame = 2

    @staticmethod
    def exit(megamen):
        game_world.erase_obj(ChargingShot.projectile)
        charged_time = game_framework.time.time() - ChargingShot.start_time
        if charged_time > 0.5:
            if megamen.face_dir == 'r':
                projectile = megamen_projectile.MegaChargingShot(megamen.x + ChargingShot.frame[0][2] * megamen.size // 2,
                                                                 megamen.y + megamen.size * ChargingShot.frame[0][3] // 2, 1)
            else:
                projectile = megamen_projectile.MegaChargingShot(megamen.x - ChargingShot.frame[0][2] * megamen.size // 2,
                                                                 megamen.y + megamen.size * ChargingShot.frame[0][3] // 2, -1)
            projectile.size = min(charged_time, 2)
            game_world.add_obj(projectile, 1)


class FireSword:
    frame = [(23, 472, 37, 46),
             (67, 472, 35, 44),
             (123, 462, 57, 55),
             (185, 464, 56, 55),
             (248, 470, 54, 45),
             (309, 472, 54, 46),
             (364, 474, 35, 47,),
             (409, 472, 37, 50,), ]
    nFrame = 8
    FRAME_PER_SEC = 16

    @staticmethod
    def enter(megamen):
        megamen.frame = 0

    @staticmethod
    def do(megamen):
        megamen.next_frame()
        if not megamen.isFall:
            megamen.state_machine.handle_event(("LAND", 0))

    @staticmethod
    def exit(megamen):
        pass


class Tornado:
    frame = [(22, 140, 34, 50),
             (60, 140, 37, 50),
             (102, 140, 26, 50),
             (134, 140, 31, 50),
             (174, 140, 34, 50),
             (216, 140, 26, 50),
             (253, 140, 31, 47),
             (292, 143, 40, 40),
             (336, 143, 38, 40),
             (380, 145, 38, 39),
             (424, 145, 34, 44), ]
    nFrame = 11
    FRAME_PER_SEC = 22
    RUSH_SPEED = 5

    @staticmethod
    def enter(megamen):
        megamen.frame = 0
        if megamen.face_dir == "r":
            megamen.speed[0] = Tornado.RUSH_SPEED
        else:
            megamen.speed[0] = -Tornado.RUSH_SPEED
        megamen.fire_tornado(0, Tornado.frame[megamen.frame][3])

    @staticmethod
    def do(megamen):
        isRepeat = False if int(megamen.frame) == 0 else True
        megamen.next_frame()
        if isRepeat and int(megamen.frame) == 0:
            megamen.state_machine.handle_event(("EOA", 0))

    @staticmethod
    def exit(self):
        pass


class JumpShot:
    frame = [(52, 1369, 38, 49),
             (95, 1369, 39, 50),
             (139, 1369, 38, 46), ]
    nFrame = 3
    FRAME_PER_SEC = 6

    @staticmethod
    def enter(megamen):
        megamen.frame = 0

    @staticmethod
    def do(megamen):
        isShot = False if int(megamen.frame) == 1 else True
        megamen.next_frame()
        if int(megamen.frame) == 1 and isShot:
            megamen.fire_megabuster(JumpShot.frame[int(megamen.frame)][2],
                                    JumpShot.frame[int(megamen.frame)][3] * megamen.size // 2)
        if megamen.y <= game_world.ground:
            megamen.state_machine.handle_event(("LAND", 0))

    @staticmethod
    def exit(megamen):
        pass


class JumpHurricane:
    frame = [(25, 387, 36, 50,),
             (68, 387, 36, 50,),
             (110, 387, 33, 50,),
             (151, 387, 31, 51,),
             (188, 387, 34, 50,),
             (230, 387, 37, 50,), ]
    nFrame = 6
    FRAME_PER_SEC = 12
    PROJECTILE = None

    @staticmethod
    def enter(megamen):
        megamen.frame = 0
        JumpHurricane.PROJECTILE = megamen_projectile.MegaHurricane(megamen)
        game_world.add_obj(JumpHurricane.PROJECTILE, 1)

    @staticmethod
    def do(megamen):
        megamen.next_frame()
        if int(megamen.frame) == JumpHurricane.nFrame - 1:
            game_world.erase_obj(JumpHurricane.PROJECTILE)
        if megamen.isFall:
            megamen.frame = min(megamen.frame, JumpHurricane.nFrame - 1)
        else:
            megamen.state_machine.handle_event(("LAND", 0))

    @staticmethod
    def exit(megamen):
        game_world.erase_obj(JumpHurricane.PROJECTILE)
        pass


class StateMachine:
    def __init__(self, megamen):
        self.state = Idle
        self.megamen = megamen
        self.table = {Idle: {megamen.control_method.move_r_down: Run, megamen.control_method.move_l_down: Run,
                             megamen.control_method.move_r_up: Run, megamen.control_method.move_l_up: Run,
                             megamen.control_method.jump_down: Jump,
                             megamen.control_method.atk1_down: SmallShot,
                             megamen.control_method.atk2_down: ChargingShot,
                             megamen.control_method.up_atk1_down: Uppercut,
                             megamen.control_method.ultimate_down: CogwheelShot,
                             megamen.control_method.up_ultimate_down: Tornado},
                      Run: {megamen.control_method.move_r_down: Idle, megamen.control_method.move_l_down: Idle,
                            megamen.control_method.move_r_up: Idle, megamen.control_method.move_l_up: Idle,
                            megamen.control_method.jump_down: Jump,
                            megamen.control_method.atk1_down: RunShot,
                            megamen.control_method.atk2_down: ChargingShot,
                            megamen.control_method.up_atk1_down: Uppercut,
                            megamen.control_method.ultimate_down: CogwheelShot,
                            megamen.control_method.up_ultimate_down: Tornado
                            },
                      AnimationEnd: {check_run: Run, check_idle: Idle},
                      Land: {end_of_animation: AnimationEnd},
                      Jump: {land: Land, megamen.control_method.atk1_down: JumpShot,
                             megamen.control_method.up_ultimate_down: JumpHurricane,
                             megamen.control_method.atk2_down: JumpKnuckle,
                             megamen.control_method.ultimate_down: FireSword},
                      RunShot: {megamen.control_method.move_r_down: Idle, megamen.control_method.move_l_down: Idle,
                                megamen.control_method.move_r_up: Idle, megamen.control_method.move_l_up: Idle,
                                end_of_animation: AnimationEnd},
                      SmallShot: {megamen.control_method.move_r_down: RunShot,
                                  megamen.control_method.move_l_down: RunShot,
                                  megamen.control_method.move_r_up: RunShot, megamen.control_method.move_l_up: RunShot,
                                  end_of_animation: AnimationEnd},
                      ChargingShot: {megamen.control_method.atk2_up: AnimationEnd},
                      Uppercut: {land: Land},
                      Tornado: {end_of_animation: AnimationEnd},
                      FireSword: {land: Land},
                      JumpShot: {land: Land, megamen.control_method.atk1_down: JumpShot},
                      JumpHurricane: {land: Land},
                      JumpKnuckle: {land: Land},
                      CogwheelShot: {end_of_animation: AnimationEnd}}

    def draw(self):
        frame = int(self.megamen.frame)
        if self.megamen.face_dir == "r":
            self.megamen.img.clip_draw(
                *self.state.frame[frame],
                self.megamen.x,
                self.megamen.y + self.megamen.size * self.state.frame[frame][3] // 2,
                self.state.frame[frame][2] * self.megamen.size,
                self.state.frame[frame][3] * self.megamen.size
            )
        elif self.megamen.face_dir == "l":
            self.megamen.img.clip_composite_draw(
                *self.state.frame[frame],
                0, 'h',
                self.megamen.x,
                self.megamen.y + self.megamen.size * self.state.frame[frame][3] // 2,
                self.state.frame[frame][2] * self.megamen.size,
                self.state.frame[frame][3] * self.megamen.size
            )
        draw_rectangle(*self.megamen.get_bb())

    def update(self):
        self.megamen.move()
        self.state.do(self.megamen)

    def handle_event(self, e):
        if self.megamen.control_method.up_down(e):
            self.megamen.up = True
        elif self.megamen.control_method.up_up(e):
            self.megamen.up = False
        elif self.megamen.control_method.move_r_down(e) or self.megamen.control_method.move_l_up(e):
            self.megamen.dir += 1
        elif self.megamen.control_method.move_l_down(e) or self.megamen.control_method.move_r_up(e):
            self.megamen.dir -= 1
        for check, next_state in self.table[self.state].items():
            if check(e):
                self.state.exit(self.megamen)
                self.state = next_state
                self.state.enter(self.megamen)


class MegaMen:
    img = None

    def __init__(self, control_method):
        self.isFall = True
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

    def fire_megabuster(self, fire_x, fire_y):
        if self.face_dir == "r":
            game_world.add_obj(megamen_projectile.MegaBuster(self.x + fire_x, self.y + fire_y, 1), 1)
        else:
            game_world.add_obj(megamen_projectile.MegaBuster(self.x - fire_x, self.y + fire_y, -1), 1)

    def fire_cogwheel(self, fire_x, fire_y):
        if self.face_dir == "r":
            game_world.add_obj(megamen_projectile.MegaCogwheel(self.x + fire_x, self.y + fire_y, 1), 1)
        else:
            game_world.add_obj(megamen_projectile.MegaCogwheel(self.x - fire_x, self.y + fire_y, -1), 1)

    def fire_tornado(self, fire_x, fire_y):
        if self.face_dir == "r":
            game_world.add_obj(megamen_projectile.MegaTornado(self.x + fire_x, self.y + fire_y, self.speed[0]), 0)
        else:
            game_world.add_obj(megamen_projectile.MegaTornado(self.x - fire_x, self.y + fire_y, self.speed[0]), 0)

    def draw(self):
        self.state_machine.draw()

    def update(self):
        self.state_machine.update()

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
        if group == "character:ground" and self.isFall:
            self.y = other.y + 1
            self.speed[1] = 0
            self.isFall = False
