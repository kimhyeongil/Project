from pico2d import *
import game_framework
import instruction_mode

import select_mode


def init():
    global title
    title = load_image("title.png")


def finish():
    global title
    title = None


def pause():
    pass


def resume():
    pass


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                game_framework.quit()
            elif event.key == SDLK_RETURN:
                game_framework.change_mode(select_mode)
            elif event.key == SDLK_SPACE:
                game_framework.push_mode(instruction_mode)


def update():
    pass


def draw():
    clear_canvas()
    title.clip_draw_to_origin(0, 0, title.w, title.h, 0, 0, get_canvas_width(), get_canvas_height())
    update_canvas()
