from sdl2 import SDL_KEYDOWN, SDLK_d, SDLK_a, SDL_KEYUP, SDLK_h, SDLK_f, SDLK_g, SDLK_s, SDLK_w, SDLK_r

x = 200
start_face = "r"


def move_r_down(e):
    return e[0] == "INPUT" and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_d


def move_l_down(e):
    return e[0] == "INPUT" and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_a


def move_r_up(e):
    return e[0] == "INPUT" and e[1].type == SDL_KEYUP and e[1].key == SDLK_d


def move_l_up(e):
    return e[0] == "INPUT" and e[1].type == SDL_KEYUP and e[1].key == SDLK_a


def jump_down(e):
    return e[0] == "INPUT" and e[1].type == SDL_KEYUP and e[1].key == SDLK_h


def atk1_down(e):
    return e[0] == "INPUT" and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_f and not e[2]


def up_atk1_down(e):
    return e[0] == "INPUT" and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_f and e[2]


def atk2_down(e):
    return e[0] == "INPUT" and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_g and not e[2]


def up_atk2_down(e):
    return e[0] == "INPUT" and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_g and e[2]


def atk2_up(e):
    return e[0] == "INPUT" and e[1].type == SDL_KEYUP and e[1].key == SDLK_g


def up_down(e):
    return e[0] == "INPUT" and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_w


def up_up(e):
    return e[0] == "INPUT" and e[1].type == SDL_KEYUP and e[1].key == SDLK_w


def ultimate_down(e):
    return e[0] == "INPUT" and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_r and not e[2]


def up_ultimate_down(e):
    return e[0] == "INPUT" and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_r and e[2]
