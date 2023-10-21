from pico2d import open_canvas, delay, close_canvas, get_events, clear_canvas, update_canvas
from sdl2 import SDL_QUIT, SDL_KEYDOWN, SDLK_ESCAPE

import mario
import game_world
import megamen
time_slice = 0.1


def handle_events():
    global running
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False


def create_world():
    global running
    open_canvas()
    running = True
    # game_world.add_obj(mario.Mario(), 1)
    game_world.add_obj(megamen.MegaMen(),1)
def render():
    clear_canvas()
    game_world.render()
    update_canvas()


def update():
    game_world.update()


create_world()
while running:
    handle_events()
    render()
    update()
    delay(time_slice)
close_canvas()
