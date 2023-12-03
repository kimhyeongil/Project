from pico2d import *
import game_framework


def init():
    global instruction
    instruction = load_image('instruction.png')
    hide_lattice()


def finish():
    global instruction
    instruction = None


def pause():
    pass


def resume():
    pass


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.pop_mode()


def update():
    pass


def draw():
    clear_canvas()
    instruction.clip_draw_to_origin(0, 0, instruction.w, instruction.h, 0, 0, get_canvas_width(), get_canvas_height())
    update_canvas()
