from pico2d import open_canvas, delay, close_canvas, get_events, clear_canvas, update_canvas, load_image
from sdl2 import SDL_QUIT, SDL_KEYDOWN, SDLK_ESCAPE

import control
import game_framework
import mario
import game_world
import megamen
import megamen_projectile


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
            player1.state_machine.handle_events(event)
            player2.state_machine.handle_events(event)


def init():
    global player1, player2
    megamen_projectile.projectile = load_image('megamen.png')
    player1 = megamen.MegaMen(control.Player1)
    player2 = mario.Mario(control.Player2)
    player1.state_machine.start()
    game_world.add_obj(player1, 1)
    game_world.add_obj(player2, 1)
    # game_world.add_obj(megamen.MegaMen(), 1)

def finish():
    pass

def draw():
    clear_canvas()
    game_world.render()
    update_canvas()


def update():
    game_world.update()

