from pico2d import open_canvas, delay, close_canvas, get_events, clear_canvas, update_canvas
from sdl2 import SDL_QUIT, SDL_KEYDOWN, SDLK_ESCAPE

import control
import mario
import game_world
import megamen



def handle_events():
    global running
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False
        else:
            player1.state_machine.handle_events(event)


def create_world():
    global running
    global player1
    open_canvas()
    running = True
    player1 = mario.Mario(control.Player1)
    game_world.add_obj(player1, 1)
    # game_world.add_obj(megamen.MegaMen(), 1)


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
    delay(game_world.time_slice)
close_canvas()
