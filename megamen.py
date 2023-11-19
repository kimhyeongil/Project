import time

from pico2d import load_image, draw_rectangle, load_font
import game_framework
import game_world
import megamen_projectile
import play_sever
import player1_control
import player2_control


def end_of_animation(e):
    return e[0] == "EOA"


def check_run(e):
    return e[0] == "CHECK_STATE" and e[1] != 0


def check_idle(e):
    return e[0] == "CHECK_STATE" and e[1] == 0


def land(e):
    return e[0] == "LAND"


def fall(e):
    return e == "FALL"


def time_out(e):
    return e[0] == "TIMEOUT"


def hit(e):
    return e[0] == "HIT"


class Fall:
    FRAME_INFO = [(98, 1622, 37, 50)]
    nFrame = 1

    FRAME_PER_SEC = 1

    @staticmethod
    def exit(megamen):
        pass

    @staticmethod
    def enter(megamen):
        megamen.frame = 0

    @staticmethod
    def do(megamen):
        megamen.next_frame()
        if not megamen.isFall:
            megamen.state_machine.handle_event(("LAND", 0))


class Hit:
    FRAME_INFO = [(13, 1297, 35, 47,)]
    nFrame = 1
    FRAME_PER_SEC = 0
    start_time = 0

    @staticmethod
    def enter(megamen):
        megamen.frame = 0
        Hit.start_time = time.time()

    @staticmethod
    def do(megamen):
        megamen.next_frame()
        if not megamen.isFall:
            megamen.speed[0] = megamen.speed[0] * (1 - game_framework.frame_time)
        if time.time() - Hit.start_time >= megamen.rigid_time and not megamen.isFall:
            megamen.state_machine.handle_event(("TIMEOUT", 0))

    @staticmethod
    def exit(megamen):
        pass


class Land:
    FRAME_INFO = [
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
        old_frame = int(megamen.frame)
        megamen.next_frame()
        int_frame = int(megamen.frame)
        if int_frame == 0 and int_frame != old_frame:
            megamen.state_machine.handle_event(("EOA", 0))


class AnimationEnd:
    @staticmethod
    def exit(megamen):
        pass

    @staticmethod
    def enter(megamen):
        megamen.frame = 0
        megamen.atk_box.reset()
        megamen.state_machine.handle_event(("CHECK_STATE", megamen.dir, megamen.up))


class Idle:
    FRAME_INFO = [(16, 1774, 31, 45),
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
    FRAME_INFO = [(62, 1434, 42, 43),
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
        old_frame = int(megamen.frame)
        megamen.next_frame()
        int_frame = int(megamen.frame)
        if int_frame != old_frame:
            if int_frame % 4 == 0 and int_frame != 0:
                megamen.fire_megabuster(RunShot.FRAME_INFO[int_frame][2],
                                        RunShot.FRAME_INFO[int_frame][3] * megamen.size // 2 + 5)
            if int_frame == 0:
                megamen.state_machine.handle_event(("EOA", 0))


class Run:
    FRAME_INFO = [(101, 1706, 30, 43),
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
            megamen.face_dir = "r"
        else:
            megamen.face_dir = "l"
        megamen.speed[0] = Run.RUN_SPEED * megamen.dir

    @staticmethod
    def do(megamen):
        megamen.next_frame()


class Jump:
    FRAME_INFO = [(16, 1622, 32, 44),
                  (55, 1622, 36, 49), ]
    nFrame = 2

    JUMP_POWER = 15
    FRAME_PER_SEC = 8

    @staticmethod
    def exit(megamen):
        pass

    @staticmethod
    def enter(megamen):
        megamen.frame = 0
        megamen.speed[1] = Jump.JUMP_POWER

    @staticmethod
    def do(megamen):
        megamen.next_frame()
        if megamen.speed[1] < 0:
            megamen.state_machine.handle_event("FALL")


class JumpKnuckle:
    FRAME_INFO = [(24, 305, 34, 46,),
                  (66, 311, 40, 39,),
                  (115, 306, 39, 45,),
                  (166, 306, 34, 46,),
                  (210, 308, 35, 47,),
                  (255, 306, 37, 50,),
                  ]
    nFrame = 6
    FRAME_PER_SEC = 8
    SPEED = 15

    @staticmethod
    def exit(megamen):
        pass

    @staticmethod
    def enter(megamen):
        megamen.frame = 0

    @staticmethod
    def do(megamen):
        old_frame = int(megamen.frame)
        megamen.next_frame()
        int_frame = int(megamen.frame)
        if int_frame != old_frame and int_frame == 2:
            megamen.fire_knuckle()
            megamen.speed[1] += JumpKnuckle.SPEED
        if not megamen.isFall:
            megamen.state_machine.handle_event(("LAND", 0))


class SmallShot:
    FRAME_INFO = [(13, 1491, 44, 44),
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
        old_frame = int(megamen.frame)
        megamen.next_frame()
        int_frame = int(megamen.frame)
        if int_frame != old_frame:
            if int_frame % 2 == 0 and int_frame != 0:
                megamen.fire_megabuster(SmallShot.FRAME_INFO[int_frame][2],
                                        SmallShot.FRAME_INFO[int_frame][3] * megamen.size // 2 + 5)
            if int_frame == 0:
                megamen.state_machine.handle_event(("EOA", 0))


class Uppercut:
    FRAME_INFO = [(20, 1031, 29, 42),
                  (56, 1031, 35, 39),
                  (97, 1031, 24, 56), ]
    nFrame = 3
    FRAME_PER_SEC = 15

    JUMP_POWER = 13

    ATK_INFO = (10, 1, 18.2, 0.1)
    ATK_BB_INFO = [(29, 42, 10, 10), (35, 39, 20, 30), (24, 280 / 3, 20, 30)]

    @staticmethod
    def exit(megamen):
        megamen.atk_box.reset()

    @staticmethod
    def enter(megamen):
        megamen.frame = 0
        megamen.speed[0] = 0
        megamen.set_atk_info(*Uppercut.ATK_INFO)

    @staticmethod
    def do(megamen):
        megamen.next_frame()
        int_frame = int(megamen.frame)
        state = Uppercut
        megamen.set_atk_bb(*state.ATK_BB_INFO[int_frame])
        if int_frame == 1:
            megamen.speed[1] = state.JUMP_POWER
        if int_frame >= 1 and megamen.speed[1] < 2:
            megamen.state_machine.handle_event(("EOA", 0))


class CogwheelShot:
    FRAME_INFO = [(27, 556, 31, 45,),
                  (68, 556, 31, 45,),
                  (111, 556, 42, 44,),
                  (158, 556, 40, 41,),
                  (205, 556, 34, 44,),
                  (252, 556, 31, 45,), ]

    nFrame = 6
    FRAME_PER_SEC = 9

    @staticmethod
    def exit(megamen):
        pass

    @staticmethod
    def enter(megamen):
        megamen.frame = 0
        megamen.speed[0] = 0
        megamen.control_method.ultimate_gage -= 1

    @staticmethod
    def do(megamen):
        old_frame = int(megamen.frame)
        megamen.next_frame()
        int_frame = int(megamen.frame)
        if int_frame != old_frame:
            if int_frame == 3:
                megamen.fire_cogwheel(CogwheelShot.FRAME_INFO[int_frame][2],
                                      CogwheelShot.FRAME_INFO[int_frame][3] * megamen.size // 2 - 5)
            elif int_frame == 0:
                megamen.state_machine.handle_event(("EOA", 0))


class ChargingShot:
    FRAME_INFO = [(355, 1491, 47, 42)]

    nFrame = 1
    FRAME_PER_SEC = 6
    start_time = 0

    projectile = None

    @staticmethod
    def enter(megamen):
        megamen.frame = 0
        megamen.speed[0] = 0
        ChargingShot.start_time = game_framework.time.time()
        ChargingShot.projectile = megamen_projectile.MegaChargingShot(megamen=megamen)

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
            megamen.fire_charging_shot(ChargingShot.FRAME_INFO[0][2] * megamen.size // 2,
                                       ChargingShot.FRAME_INFO[0][3] * megamen.size // 2, charged_time)


class FireSword:
    FRAME_INFO = [(23, 472, 37, 46),
                  (67, 472, 35, 44),
                  (123, 462, 57, 55),
                  (185, 464, 56, 55),
                  (248, 470, 54, 45),
                  (309, 472, 54, 46),
                  (364, 474, 35, 47),
                  (409, 472, 37, 50,), ]
    nFrame = 8
    FRAME_PER_SEC = 16

    ATK_INFO = (10, 1, 10, 2)
    ATK_BB_INFO = [(37, 46, 20, 46),
                   (35, 44, 20, 44),
                   (57, 55, 20, 55),
                   (56, 55, 20, 55),
                   (54, 45, 20, 45),
                   (54, 46, 20, 46),
                   (35, 47, 20, 47),
                   (37, 50, 20, 50)]

    @staticmethod
    def enter(megamen):
        megamen.frame = 0
        megamen.set_atk_info(*FireSword.ATK_INFO)
        megamen.control_method.ultimate_gage -= 1

    @staticmethod
    def do(megamen):
        old_frame = int(megamen.frame)
        megamen.next_frame()
        int_frame = int(megamen.frame)
        state = FireSword
        megamen.set_atk_bb(*state.ATK_BB_INFO[int_frame])
        if int_frame == state.nFrame - 2:
            megamen.atk_box.reset()
        if ((not megamen.isFall and int_frame == state.nFrame - 1)
                or (int_frame == 0 and int_frame != old_frame)):
            megamen.state_machine.handle_event(("EOA", 0))

    @staticmethod
    def exit(megamen):
        megamen.atk_box.reset()


class RushTornado:
    FRAME_INFO = [(22, 140, 34, 50),
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
            megamen.speed[0] = RushTornado.RUSH_SPEED
        else:
            megamen.speed[0] = -RushTornado.RUSH_SPEED
        megamen.fire_tornado(0, RushTornado.FRAME_INFO[0][3])
        megamen.control_method.ultimate_gage -= 3

    @staticmethod
    def do(megamen):
        old_frame = int(megamen.frame)
        megamen.next_frame()
        int_frame = int(megamen.frame)
        if int_frame == 0 and int_frame != old_frame:
            megamen.state_machine.handle_event(("EOA", 0))

    @staticmethod
    def exit(self):
        pass


class JumpShot:
    FRAME_INFO = [(52, 1369, 38, 49),
                  (95, 1369, 39, 50),
                  (139, 1369, 38, 46), ]
    nFrame = 3
    FRAME_PER_SEC = 9

    @staticmethod
    def enter(megamen):
        megamen.frame = 0

    @staticmethod
    def do(megamen):
        old_frame = int(megamen.frame)
        megamen.next_frame()
        int_frame = int(megamen.frame)
        if int_frame != old_frame:
            if int_frame == 1:
                megamen.fire_megabuster(JumpShot.FRAME_INFO[int_frame][2],
                                        JumpShot.FRAME_INFO[int_frame][3] * megamen.size // 2)
            if int_frame == JumpShot.nFrame - 1:
                megamen.state_machine.handle_event(("EOA", 0))

    @staticmethod
    def exit(megamen):
        pass


class UpTornado:
    FRAME_INFO = [(25, 387, 36, 50,),
                  (68, 387, 36, 50,),
                  (110, 387, 33, 50,),
                  (151, 387, 31, 51,),
                  (188, 387, 34, 50,),
                  (230, 387, 37, 50,), ]
    nFrame = 6
    FRAME_PER_SEC = 12
    JUMP_POWER = 12
    PROJECTILE = None

    @staticmethod
    def enter(megamen):
        megamen.frame = 0
        megamen.speed[1] = UpTornado.JUMP_POWER
        UpTornado.PROJECTILE = megamen_projectile.MegaHurricane(megamen)
        megamen.control_method.add_atk_collision(UpTornado.PROJECTILE)
        game_world.add_obj(UpTornado.PROJECTILE, 1)

    @staticmethod
    def do(megamen):
        megamen.next_frame()
        if int(megamen.frame) == UpTornado.nFrame - 1:
            game_world.erase_obj(UpTornado.PROJECTILE)
            megamen.state_machine.handle_event(("EOA", 0))

    @staticmethod
    def exit(megamen):
        game_world.erase_obj(UpTornado.PROJECTILE)
        pass


class StateMachine:
    def __init__(self, megamen):
        self.state = Idle
        self.megamen = megamen
        self.table = {Idle: {megamen.control_method.move_r_down: Run, megamen.control_method.move_l_down: Run,
                             megamen.control_method.move_r_up: Run, megamen.control_method.move_l_up: Run,
                             megamen.control_method.jump_down: Jump, hit: Hit,
                             megamen.control_method.atk1_down: SmallShot,
                             megamen.control_method.atk2_down: ChargingShot,
                             megamen.control_method.up_atk1_down: Uppercut,
                             megamen.control_method.up_atk2_down: UpTornado,
                             megamen.control_method.ultimate_down: CogwheelShot,
                             megamen.control_method.up_ultimate_down: RushTornado},
                      Run: {megamen.control_method.move_r_down: Idle, megamen.control_method.move_l_down: Idle,
                            megamen.control_method.move_r_up: Idle, megamen.control_method.move_l_up: Idle,
                            megamen.control_method.jump_down: Jump, hit: Hit,
                            megamen.control_method.atk1_down: RunShot,
                            megamen.control_method.atk2_down: ChargingShot,
                            megamen.control_method.up_atk1_down: Uppercut,
                            megamen.control_method.up_atk2_down: UpTornado,
                            megamen.control_method.ultimate_down: CogwheelShot,
                            megamen.control_method.up_ultimate_down: RushTornado
                            },
                      AnimationEnd: {check_run: Run, check_idle: Idle},
                      Land: {end_of_animation: AnimationEnd},
                      Jump: {fall: Fall, megamen.control_method.atk1_down: JumpShot,
                             megamen.control_method.atk2_down: JumpKnuckle, hit: Hit,
                             megamen.control_method.ultimate_down: FireSword},
                      RunShot: {megamen.control_method.move_r_down: Idle, megamen.control_method.move_l_down: Idle,
                                megamen.control_method.move_r_up: Idle, megamen.control_method.move_l_up: Idle,
                                end_of_animation: AnimationEnd},
                      SmallShot: {megamen.control_method.move_r_down: RunShot,
                                  megamen.control_method.move_l_down: RunShot,
                                  megamen.control_method.move_r_up: RunShot, megamen.control_method.move_l_up: RunShot,
                                  end_of_animation: AnimationEnd},
                      ChargingShot: {megamen.control_method.atk2_up: AnimationEnd},
                      Uppercut: {end_of_animation: Fall},
                      RushTornado: {end_of_animation: AnimationEnd},
                      FireSword: {end_of_animation: Land},
                      JumpShot: {end_of_animation: Fall},
                      UpTornado: {end_of_animation: Fall},
                      JumpKnuckle: {land: Land},
                      CogwheelShot: {end_of_animation: AnimationEnd},
                      Fall: {land: Land, megamen.control_method.atk1_down: JumpShot,
                             megamen.control_method.atk2_down: JumpKnuckle, hit: Hit,
                             megamen.control_method.ultimate_down: FireSword},
                      Hit: {time_out: AnimationEnd}}

    def draw(self):
        int_frame = int(self.megamen.frame)
        if self.megamen.face_dir == "r":
            self.megamen.img.clip_draw(
                *self.state.FRAME_INFO[int_frame],
                self.megamen.x,
                self.megamen.y + self.state.FRAME_INFO[int_frame][3] * self.megamen.size // 2,
                self.state.FRAME_INFO[int_frame][2] * self.megamen.size,
                self.state.FRAME_INFO[int_frame][3] * self.megamen.size
            )
        elif self.megamen.face_dir == "l":
            self.megamen.img.clip_composite_draw(
                *self.state.FRAME_INFO[int_frame],
                0, 'h',
                self.megamen.x,
                self.megamen.y + self.state.FRAME_INFO[int_frame][3] * self.megamen.size // 2,
                self.state.FRAME_INFO[int_frame][2] * self.megamen.size,
                self.state.FRAME_INFO[int_frame][3] * self.megamen.size
            )

    def update(self):
        self.megamen.move()
        self.state.do(self.megamen)

    def handle_event(self, e):
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
        self.hp = 125
        self.speed = [0, 0]
        self.atk_box = AtkBox()
        self.face_dir = control_method.start_face
        self.control_method = control_method
        self.state_machine = StateMachine(self)
        self.resist_coefficient = 0.5
        self.rigid_time = 0
        self.font = load_font('ENCR10B.TTF', 40)
        control_method.add_atk_collision(self.atk_box)
        self.up = False
        if MegaMen.img == None:
            MegaMen.img = load_image('megamen.png')

    def set_atk_bb(self, dx, dy, sx, sy):
        if self.face_dir == "l":
            atkX, atkY = self.x - dx, self.y + dy
            self.atk_box.bb = (atkX - sx, atkY - sy, atkX + sx, atkY + sy)
        else:
            atkX, atkY = self.x + dx, self.y + dy
            self.atk_box.bb = (atkX - sx, atkY - sy, atkX + sx, atkY + sy)

    def set_atk_info(self, DAMAGE, RIGID, KNOCK_UP=0, KNOCK_BACK=0):
        if self.face_dir == "l":
            KNOCK_BACK *= -1
        self.atk_box.set_info(DAMAGE, RIGID, KNOCK_UP, KNOCK_BACK)

    def fire_megabuster(self, fire_x, fire_y):
        if self.face_dir == "r":
            self.control_method.add_atk_collision(
                megamen_projectile.MegaBuster(self.x + fire_x, self.y + fire_y, 1))
        else:
            self.control_method.add_atk_collision(
                megamen_projectile.MegaBuster(self.x - fire_x, self.y + fire_y, -1))

    def fire_cogwheel(self, fire_x, fire_y):
        if self.face_dir == "r":
            self.control_method.add_atk_collision(megamen_projectile.MegaCogwheel(self.x + fire_x, self.y + fire_y, 1))
        else:
            self.control_method.add_atk_collision(megamen_projectile.MegaCogwheel(self.x - fire_x, self.y + fire_y, -1))

    def fire_charging_shot(self, fire_x, fire_y, charged_time):
        if self.face_dir == 'r':
            self.control_method.add_atk_collision(
                megamen_projectile.MegaChargingShot(
                    self.x + fire_x,
                    self.y + fire_y, 1, charged_time))
        else:
            self.control_method.add_atk_collision(
                megamen_projectile.MegaChargingShot(
                    self.x - fire_x,
                    self.y + fire_y, -1, charged_time))

    def fire_knuckle(self):
        self.control_method.add_atk_collision(megamen_projectile.MegaKnuckle(self.x, self.y, self.size))

    def fire_tornado(self, fire_x, fire_y):
        if self.face_dir == "r":
            self.control_method.add_atk_collision(
                megamen_projectile.MegaTornado(self.x + fire_x, self.y + fire_y, self.speed[0]))
        else:
            self.control_method.add_atk_collision(
                megamen_projectile.MegaTornado(self.x - fire_x, self.y + fire_y, self.speed[0]))

    def draw(self):
        self.state_machine.draw()
        int_frame = int(self.frame)
        state = self.state_machine.state
        draw_rectangle(*self.get_bb())
        if self.atk_box.get_bb():
            draw_rectangle(*self.atk_box.get_bb())
        self.font.draw(self.x, self.y + state.FRAME_INFO[int_frame][3] * self.size + 5, f"{self.hp}", (0, 0, 0))
        self.font.draw(self.x, 300, f"{round(self.control_method.ultimate_gage, 2)}", (0, 0, 0))

    def update(self):
        self.state_machine.update()
        self.control_method.ultimate_gage = min(self.control_method.ultimate_gage + game_framework.frame_time / 100, 3)

    def move(self):
        self.x += self.speed[0] * game_world.PIXEL_PER_METER * game_framework.frame_time
        self.y += self.speed[1] * game_world.PIXEL_PER_METER * game_framework.frame_time
        if self.speed[1] > 0:
            self.isFall = True
        if self.isFall:
            self.speed[1] -= game_world.g * game_framework.frame_time

    def handle_event(self, e):
        input_e = ("INPUT", e, self.up)
        if self.control_method.up_down(input_e):
            self.up = True
        elif self.control_method.up_up(input_e):
            self.up = False
        elif self.control_method.move_r_down(input_e) or self.control_method.move_l_up(input_e):
            self.dir += 1
        elif self.control_method.move_l_down(input_e) or self.control_method.move_r_up(input_e):
            self.dir -= 1
        self.state_machine.handle_event(input_e)

    def next_frame(self):
        state = self.state_machine.state
        self.frame = (self.frame + state.FRAME_PER_SEC * game_framework.frame_time) % state.nFrame
        if self.isFall:
            self.frame = min(self.frame, state.nFrame - 1)

    def get_bb(self):
        int_frame = int(self.frame)
        state = self.state_machine.state
        return self.x - state.FRAME_INFO[int_frame][2] * self.size // 2, self.y, self.x + state.FRAME_INFO[int_frame][
            2] * self.size // 2, self.y + state.FRAME_INFO[int_frame][3] * self.size

    def handle_collision(self, group, other):
        if group == "character:ground":
            self.y = other.y + 1
            if self.speed[1] > -30:
                self.speed[1] = 0
                self.isFall = False
            else:
                self.speed[1] = -(self.speed[1] + 30)

    def hit(self, damage, rigid=0, knock_up=0, knock_back=0):
        self.control_method.ultimate_gage = min(self.control_method.ultimate_gage + damage / 200, 3)
        self.rigid_time += rigid * self.resist_coefficient
        state = self.state_machine.state
        if state == Idle or state == Run or state == Jump or state == Fall or state == Hit:
            self.speed[1] += knock_up
            self.speed[0] = knock_back
        if self.speed[1] != 0:
            self.isFall = True
        self.hp -= damage
        self.state_machine.handle_event(("HIT", 0))


class AtkBox:
    def __init__(self):
        self.bb = None
        self.info = (0, 0, 0, 0)

    def get_bb(self):
        return self.bb

    def set_info(self, D, R, U, B):
        self.info = (D, R, U, B)

    def handle_collision(self, group, other):
        if other.control_method.isHit(group):
            if self.info[0] > 0:
                other.hit(*self.info)
                if group == "Player1:Player2":
                    player1_control.ultimate_gage += self.info[0] / 100
                else:
                    player2_control.ultimate_gage += self.info[0] / 100
                self.reset()

    def reset(self):
        self.bb = None
        self.info = (0, 0, 0, 0)
