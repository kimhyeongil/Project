from sdl2 import SDL_KEYDOWN, SDL_KEYUP, SDLK_RIGHT, SDLK_LEFT, SDLK_SLASH, SDLK_COMMA, SDLK_PERIOD

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
    return e[0] == "INPUT" and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_COMMA

def atk2_down(e):
    return e[0] == "INPUT" and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_PERIOD
