from sdl2 import SDL_KEYDOWN, SDL_KEYUP, SDLK_RIGHT, SDLK_LEFT, SDLK_SLASH, SDLK_COMMA, SDLK_PERIOD, SDLK_UP, SDLK_k

import game_world

x = 600
start_face = "l"


def move_r_down(e):
    return e[0] == "INPUT" and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_RIGHT


def move_l_down(e):
    return e[0] == "INPUT" and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_LEFT


def move_r_up(e):
    return e[0] == "INPUT" and e[1].type == SDL_KEYUP and e[1].key == SDLK_RIGHT


def move_l_up(e):
    return e[0] == "INPUT" and e[1].type == SDL_KEYUP and e[1].key == SDLK_LEFT


def jump_down(e):
    return e[0] == "INPUT" and e[1].type == SDL_KEYUP and e[1].key == SDLK_SLASH


def atk1_down(e):
    return e[0] == "INPUT" and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_COMMA and not e[2]


def up_atk1_down(e):
    return e[0] == "INPUT" and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_COMMA and e[2]


def atk2_down(e):
    return e[0] == "INPUT" and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_PERIOD and not e[2]


def up_atk2_down(e):
    return e[0] == "INPUT" and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_PERIOD and e[2]


def atk2_up(e):
    return e[0] == "INPUT" and e[1].type == SDL_KEYUP and e[1].key == SDLK_PERIOD


def up_down(e):
    return e[0] == "INPUT" and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_UP


def up_up(e):
    return e[0] == "INPUT" and e[1].type == SDL_KEYUP and e[1].key == SDLK_UP


def ultimate_down(e):
    return e[0] == "INPUT" and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_k and not e[2]


def up_ultimate_down(e):
    return e[0] == "INPUT" and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_k and e[2]


def add_collision(o):
    game_world.add_collision_pair("Player1:Player2", None, o)
