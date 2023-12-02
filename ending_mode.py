from pico2d import hide_cursor, hide_lattice, clear_canvas, update_canvas, get_events, load_image, get_canvas_width, \
    get_canvas_height, load_font
from sdl2 import SDL_KEYDOWN, SDL_QUIT, SDLK_ESCAPE, SDLK_a, SDLK_RIGHT, SDLK_d, SDLK_LEFT, SDLK_f, SDLK_COMMA, \
    SDLK_SPACE, SDLK_RETURN

import game_framework
import menu_mode


def init():
    global background
    background = load_image("ending_scene.png")


def finish():
    global background
    background = None


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                game_framework.quit()
            elif event.key == SDLK_RETURN:
                game_framework.change_mode(menu_mode)


def update():
    pass


def draw():
    clear_canvas()
    background.clip_draw_to_origin(0, 0, background.w, background.h, 0, 0, get_canvas_width(), get_canvas_height())
    update_canvas()
