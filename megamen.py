import time

from pico2d import load_image, draw_rectangle, load_font, clamp, get_canvas_width, get_canvas_height, load_wav
import game_framework
import game_world
import play_mode
from gage_bar import GageBar
from hp_bar import HPBar
from megamen_projectile import MegaChargingShot, MegaBuster, MegaTornado, MegaKnuckle, MegaHurricane, MegaBlade
import play_server
from portrait import Portrait


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


class Win:
    FRAME_INFO = [(24, 871, 34, 46),
                  (65, 871, 34, 45),
                  (108, 871, 31, 45),
                  (144, 871, 31, 50),
                  (188, 871, 31, 51),
                  (231, 871, 31, 50),
                  ]
    nFrame = 6
    FRAME_PER_SEC = 9
    l = [24, 65, 108, 144, 188, 231]
    t = [1017, 1018, 1018, 1013, 1012, 1013]
    w = [34, 34, 31, 31, 31, 31]
    h = [46, 45, 45, 50, 51, 50]

    @staticmethod
    def exit(megamen, e):
        pass

    @staticmethod
    def enter(megamen):
        state = Win
        for i in range(len(state.l)):
            print(f"({state.l[i]},{megamen.img.h - state.t[i] - state.h[i]},{state.w[i]},{state.h[i]}),")
        print(len(state.l))
        megamen.frame = 0
        megamen.speed = [0, 0]

    @staticmethod
    def do(megamen):
        old_frame = int(megamen.frame)
        megamen.next_frame()
        int_frame = int(megamen.frame)
        if int_frame != old_frame and int_frame == 0:
            megamen.frame = Win.nFrame - 4


class Defense:
    FRAME_INFO = [(26, 635, 31, 45,),
                  (64, 635, 31, 43,),
                  (101, 635, 31, 43,)]
    nFrame = 3
    FRAME_PER_SEC = 36

    @staticmethod
    def exit(megamen, e):
        pass

    @staticmethod
    def enter(megamen):
        megamen.frame = 0
        megamen.speed[0] = 0

    @staticmethod
    def do(megamen):
        megamen.next_frame()
        megamen.frame = min(megamen.frame, 2)


class Fall:
    FRAME_INFO = [(98, 1622, 37, 50)]
    nFrame = 1

    FRAME_PER_SEC = 1

    @staticmethod
    def exit(megamen, e):
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
    def exit(megamen, e):
        megamen.rigid_time = 0


class Land:
    FRAME_INFO = [
        (226, 1621, 38, 39),
        (268, 1622, 38, 39),
        (184, 1622, 38, 39), ]

    nFrame = 3
    FRAME_PER_SEC = 30

    @staticmethod
    def exit(megamen, e):
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


class Idle:
    FRAME_INFO = [(16, 1774, 31, 45),
                  (52, 1774, 31, 45),
                  (16, 1774, 31, 45), ]
    nFrame = 3
    FRAME_PER_SEC = 2

    @staticmethod
    def enter(megamen):
        megamen.speed = [0, 0]
        megamen.frame = 0
        megamen.state_machine.handle_event(("CHECK_RUN", megamen.dir))

    @staticmethod
    def do(megamen):
        megamen.next_frame()

    @staticmethod
    def exit(megamen, e):
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
    def exit(megamen, e):
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
        megamen.speed[0] = Run.RUN_SPEED * megamen.dir
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
    def exit(megamen, e):
        pass

    @staticmethod
    def enter(megamen):
        megamen.frame = 0
        if megamen.dir == 1:
            megamen.face_dir = "r"
        else:
            megamen.face_dir = "l"

    @staticmethod
    def do(megamen):
        megamen.next_frame()
        megamen.speed[0] = Run.RUN_SPEED * megamen.dir


class Jump:
    FRAME_INFO = [(16, 1622, 32, 44),
                  (55, 1622, 36, 49), ]
    nFrame = 2

    JUMP_POWER = 15
    FRAME_PER_SEC = 8

    @staticmethod
    def exit(megamen, e):
        pass

    @staticmethod
    def enter(megamen):
        megamen.frame = 0
        megamen.speed[1] = Jump.JUMP_POWER
        megamen.jump_sound.play()

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
    def exit(megamen, e):
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
    def exit(megamen, e):
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
    def exit(megamen, e):
        megamen.atk_box.reset()

    @staticmethod
    def enter(megamen):
        megamen.frame = 0
        megamen.speed[0] = 0
        megamen.set_atk_info(*Uppercut.ATK_INFO)

    @staticmethod
    def do(megamen):
        old_frame = int(megamen.frame)
        megamen.next_frame()
        int_frame = int(megamen.frame)
        state = Uppercut
        megamen.set_atk_bb(*state.ATK_BB_INFO[int_frame])
        if megamen.speed[1] < 1 and megamen.isFall:
            megamen.state_machine.handle_event(("EOA", 0))
        if int_frame == 1 and int_frame != old_frame:
            megamen.speed[1] = state.JUMP_POWER


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
    def exit(megamen, e):
        pass

    @staticmethod
    def enter(megamen):
        megamen.frame = 0
        megamen.speed[0] = 0
        megamen.ultimate_gage -= 1

    @staticmethod
    def do(megamen):
        old_frame = int(megamen.frame)
        megamen.next_frame()
        int_frame = int(megamen.frame)
        if int_frame != old_frame:
            if int_frame == 3:
                megamen.fire_blade(CogwheelShot.FRAME_INFO[int_frame][2],
                                   CogwheelShot.FRAME_INFO[int_frame][3] * megamen.size // 2 - 5)
            elif int_frame == 0:
                megamen.state_machine.handle_event(("EOA", 0))


class ChargingShot:
    FRAME_INFO = [(355, 1491, 47, 42)]

    nFrame = 1
    FRAME_PER_SEC = 6

    @staticmethod
    def enter(megamen):
        megamen.frame = 0
        megamen.speed[0] = 0
        megamen.start_time = game_framework.time.time()
        megamen.charged_time = 0
        megamen.charged_effect = MegaChargingShot(megamen=megamen)
        megamen.charged_effect.frame = 0

    @staticmethod
    def do(megamen):
        megamen.charged_time += game_framework.frame_time
        if megamen.charged_time >= 0.5:
            megamen.charged_effect.frame = 1
        if megamen.charged_time >= 2:
            megamen.charged_effect.frame = 2

    @staticmethod
    def exit(megamen, e):
        game_world.erase_obj(megamen.charged_effect)
        megamen.charged_effect = None
        if not hit(e) and megamen.charged_time >= 0.5:
            megamen.fire_charging_shot(ChargingShot.FRAME_INFO[0][2] * megamen.size // 2,
                                       ChargingShot.FRAME_INFO[0][3] * megamen.size // 2)


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

    ATK_INFO = (2, 1, 5, 2)
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
        megamen.ultimate_gage -= 1
        megamen.atk_box.effect = "ignition"

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
    def exit(megamen, e):
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
        megamen.ultimate_gage -= 3

    @staticmethod
    def do(megamen):
        if megamen.face_dir == "r":
            megamen.speed[0] = RushTornado.RUSH_SPEED
        else:
            megamen.speed[0] = -RushTornado.RUSH_SPEED
        old_frame = int(megamen.frame)
        megamen.next_frame()
        int_frame = int(megamen.frame)
        if int_frame == 0 and int_frame != old_frame:
            megamen.state_machine.handle_event(("EOA", 0))

    @staticmethod
    def exit(megamen, e):
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
    def exit(megamen, e):
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
        UpTornado.PROJECTILE = MegaHurricane(megamen)
        megamen.control_method.add_atk_collision(UpTornado.PROJECTILE)
        game_world.add_obj(UpTornado.PROJECTILE, 1)
        megamen.set_atk_bb(0, 0, 72, 100)
        megamen.set_atk_info(1, 0.1, 15, 0)

    @staticmethod
    def do(megamen):
        old_frame = int(megamen.frame)
        megamen.next_frame()
        int_frame = int(megamen.frame)
        if int_frame != old_frame and int_frame == 1:
            megamen.atk_box.reset()
        if int(megamen.frame) == UpTornado.nFrame - 1:
            game_world.erase_obj(UpTornado.PROJECTILE)
            megamen.state_machine.handle_event(("EOA", 0))

    @staticmethod
    def exit(megamen, e):
        game_world.erase_obj(UpTornado.PROJECTILE)


class StateMachine:
    def __init__(self, megamen):
        self.state = Idle
        self.megamen = megamen
        self.table = {Idle: {megamen.control_method.move_r_down: Run, megamen.control_method.move_l_down: Run,
                             megamen.control_method.move_r_up: Run, megamen.control_method.move_l_up: Run,
                             megamen.control_method.jump_down: Jump, hit: Hit, check_run: Run,
                             megamen.control_method.atk1_down: SmallShot, megamen.control_method.defence_down: Defense,
                             megamen.control_method.atk2_down: ChargingShot,
                             megamen.control_method.up_atk1_down: Uppercut,
                             megamen.control_method.up_atk2_down: UpTornado,
                             megamen.control_method.ultimate_down: CogwheelShot,
                             megamen.control_method.up_ultimate_down: RushTornado},
                      Run: {megamen.control_method.move_r_down: Idle, megamen.control_method.move_l_down: Idle,
                            megamen.control_method.move_r_up: Idle, megamen.control_method.move_l_up: Idle,
                            megamen.control_method.jump_down: Jump, hit: Hit,
                            megamen.control_method.atk1_down: RunShot, megamen.control_method.defence_down: Defense,
                            megamen.control_method.atk2_down: ChargingShot,
                            megamen.control_method.up_atk1_down: Uppercut,
                            megamen.control_method.up_atk2_down: UpTornado,
                            megamen.control_method.ultimate_down: CogwheelShot,
                            megamen.control_method.up_ultimate_down: RushTornado
                            },
                      Land: {end_of_animation: Idle, hit: Hit},
                      Jump: {fall: Fall, megamen.control_method.atk1_down: JumpShot,
                             megamen.control_method.atk2_down: JumpKnuckle, hit: Hit,
                             megamen.control_method.up_atk1_down: JumpShot,
                             megamen.control_method.up_atk2_down: JumpKnuckle,
                             megamen.control_method.ultimate_down: FireSword},
                      Fall: {land: Land, megamen.control_method.atk1_down: JumpShot,
                             megamen.control_method.atk2_down: JumpKnuckle, hit: Hit,
                             megamen.control_method.up_atk1_down: JumpShot,
                             megamen.control_method.ultimate_down: FireSword},
                      RunShot: {megamen.control_method.move_r_down: Idle, megamen.control_method.move_l_down: Idle,
                                megamen.control_method.move_r_up: Idle, megamen.control_method.move_l_up: Idle,
                                end_of_animation: Idle, hit: Hit},
                      SmallShot: {megamen.control_method.move_r_down: RunShot,
                                  megamen.control_method.move_l_down: RunShot,
                                  megamen.control_method.move_r_up: RunShot, megamen.control_method.move_l_up: RunShot,
                                  end_of_animation: Idle, hit: Hit},
                      ChargingShot: {megamen.control_method.atk2_up: Idle, hit: Hit},
                      Uppercut: {end_of_animation: Fall},
                      RushTornado: {end_of_animation: Idle},
                      FireSword: {end_of_animation: Land},
                      JumpShot: {end_of_animation: Fall, hit: Hit},
                      UpTornado: {end_of_animation: Fall},
                      JumpKnuckle: {land: Land},
                      CogwheelShot: {end_of_animation: Idle},
                      Hit: {time_out: Idle}, Win: {},
                      Defense: {megamen.control_method.defence_up: Idle, defense_fail: Hit}, }

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
        self.state.do(self.megamen)
        self.megamen.move()

    def handle_event(self, e):
        for check, next_state in self.table[self.state].items():
            if check(e):
                self.state.exit(self.megamen, e)
                self.state = next_state
                self.state.enter(self.megamen)


class MegaMen:
    img = None
    maxHp = 125 * 1.5
    resist_coefficient = 0.375
    size = 2
    jump_sound = None

    def __init__(self, control_method):
        self.isFall = True
        self.x, self.y = control_method.x, play_server.ground.y
        self.frame = 0
        self.dir = 0
        self.speed = [0, 0]
        self.charged_time = 0
        self.charged_effect = None
        self.atk_box = AtkBox(self)
        self.debuff = None
        self.debuff_time = 0
        self.face_dir = control_method.start_face
        self.control_method = control_method
        self.state_machine = StateMachine(self)
        self.rigid_time = 0
        self.hp = MegaMen.maxHp
        self.ultimate_gage = 0
        self.font = load_font('ENCR10B.TTF', 40)
        control_method.add_atk_collision(self.atk_box)
        self.up = False
        if MegaMen.img == None:
            MegaMen.img = load_image('megamen.png')
            MegaMen.jump_sound = load_wav("sound/megamen_jump.wav")
            MegaMen.jump_sound.set_volume(20)
        game_world.add_obj(Portrait(load_image("megamen_portrait.png"), control_method.portrait_pos), 1)
        self.HPBar = HPBar(control_method.hp_bar_pos, MegaMen.maxHp, control_method.hp_bar_dir)
        game_world.add_obj(self.HPBar, 1)
        self.GageBar = GageBar(control_method.gage_pos, control_method.gage_dir)
        game_world.add_obj(self.GageBar, 2)

    def win(self):
        self.state_machine.state.exit(self, ("", 0))
        self.state_machine.state = Win
        self.state_machine.state.enter(self)
        self.x = get_canvas_width() / 2
        self.y = get_canvas_height() / 2 - 100
        self.size = 5
        self.isFall = False

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

    def fire_megabuster(self, fire_x, fire_y):
        if self.face_dir == "r":
            self.control_method.add_atk_collision(MegaBuster(self.x + fire_x, self.y + fire_y, 1))
        else:
            self.control_method.add_atk_collision(MegaBuster(self.x - fire_x, self.y + fire_y, -1))

    def fire_blade(self, fire_x, fire_y):
        if self.face_dir == "r":
            self.control_method.add_atk_collision(MegaBlade(self.x + fire_x, self.y + fire_y, 1))
        else:
            self.control_method.add_atk_collision(MegaBlade(self.x - fire_x, self.y + fire_y, -1))

    def fire_charging_shot(self, fire_x, fire_y):
        self.charged_time = min(self.charged_time, 2)
        if self.face_dir == 'r':
            self.control_method.add_atk_collision(
                MegaChargingShot(self.x + fire_x, self.y + fire_y, 1, self.charged_time))
        else:
            self.control_method.add_atk_collision(
                MegaChargingShot(self.x - fire_x, self.y + fire_y, -1, self.charged_time))

    def fire_knuckle(self):
        self.control_method.add_atk_collision(MegaKnuckle(self.x, self.y, self.size))

    def fire_tornado(self, fire_x, fire_y):
        if self.face_dir == "r":
            self.control_method.add_atk_collision(MegaTornado(self.x + fire_x, self.y + fire_y, self.speed[0]))
        else:
            self.control_method.add_atk_collision(MegaTornado(self.x - fire_x, self.y + fire_y, self.speed[0]))

    def draw(self):
        self.state_machine.draw()
        # int_frame = int(self.frame)
        # state = self.state_machine.state
        # draw_rectangle(*self.get_bb())
        # if self.atk_box.get_bb():
        #     draw_rectangle(*self.atk_box.get_bb())
        # self.font1.draw(self.x, self.y + state.FRAME_INFO[int_frame][3] * self.size + 5, f"{self.hp}", (0, 0, 0))
        # self.font1.draw(self.x, 300, f"{round(self.ultimate_gage, 2)}", (0, 0, 0))

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
        if play_server.ground:
            if not game_world.collide(play_server.ground, self):
                self.isFall = True
            else:
                self.y = play_server.ground.y
                if self.speed[1] > -30:
                    self.speed[1] = 0
                    self.isFall = False
                else:
                    self.speed[1] = -(self.speed[1] + 30)
        self.ultimate_gage = min(self.ultimate_gage + game_framework.frame_time / 100, 3)
        self.HPBar.HP = self.hp
        self.GageBar.gage = self.ultimate_gage

    def move(self):
        self.x += self.speed[0] * game_world.PIXEL_PER_METER * game_framework.frame_time
        self.x = clamp(0 + 50, self.x, get_canvas_width() - 50)
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
        int_frame = int(self.frame)
        state = self.state_machine.state
        return self.x - state.FRAME_INFO[int_frame][2] * self.size // 2, self.y, self.x + state.FRAME_INFO[int_frame][
            2] * self.size // 2, self.y + state.FRAME_INFO[int_frame][3] * self.size

    def handle_collision(self, group, other):
        pass

    def hit(self, damage, rigid=0, knock_up=0, knock_back=0, atk_pos=None):
        self.ultimate_gage = min(self.ultimate_gage + damage / 20, 3)
        if self.state_machine.state == Defense:
            if (self.face_dir == "r" and atk_pos > self.x) or (self.face_dir == "l" and atk_pos < self.x):
                damage /= 2
                self.speed[0] = knock_back / 2
            else:
                self.state_machine.handle_event(("DEFENSE_FAIL", 0))
        self.state_machine.handle_event(("HIT", 0))
        if self.state_machine.state == Hit:
            self.rigid_time += rigid * (
                    (MegaMen.maxHp / (self.hp + MegaMen.maxHp)) ** 0.5) * self.resist_coefficient ** self.rigid_time
            self.speed[1] += knock_up
            self.speed[0] = knock_back
        self.hp -= damage


class AtkBox:
    def __init__(self, megamen):
        self.box_info = None
        self.ATK_INFO = (0, 0, 0, 0)
        self.effect = None
        self.megamen = megamen
        self.x = None
        self.sound = load_wav("sound/atk_sound.wav")
        self.sound.set_volume(50)

    def get_bb(self):
        if self.box_info:
            if self.megamen.face_dir == "l":
                atkX, atkY = self.megamen.x - self.box_info[0], self.megamen.y + self.box_info[1]
            else:
                atkX, atkY = self.megamen.x + self.box_info[0], self.megamen.y + self.box_info[1]
            return atkX - self.box_info[2], atkY - self.box_info[3], atkX + self.box_info[2], atkY + self.box_info[3]

    def set_info(self, D, R, U, B):
        self.ATK_INFO = (D, R, U, B)

    def handle_collision(self, group, other):
        if other.control_method.isHit(group):
            if self.ATK_INFO[0] > 0:
                self.sound.play()
                other.hit(*self.ATK_INFO, atk_pos=self.x)
                self.megamen.ultimate_gage = min(self.megamen.ultimate_gage + self.ATK_INFO[0] / 10, 3)
                if self.effect == "ignition":
                    other.debuff = "burn"
                    other.debuff_time = 3
                self.reset()

    def reset(self):
        self.box_info = None
        self.ATK_INFO = (0, 0, 0, 0)
