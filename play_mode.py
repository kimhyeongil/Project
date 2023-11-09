from pico2d import open_canvas, delay, close_canvas, get_events, clear_canvas, update_canvas, load_image
from sdl2 import SDL_QUIT, SDL_KEYDOWN, SDLK_ESCAPE

import player1_control
import player2_control
import game_framework
from mario import Mario
import game_world
from megamen import MegaMen
import megamen_projectile
from ground import Ground


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
            player1.handle_event(event)
            player2.handle_event(event)


def init():
    global player1, player2
    megamen_projectile.projectile = load_image('megamen.png')
    player1 = MegaMen(player1_control)
    player2 = Mario(player2_control)
    ground = Ground(299)
    game_world.add_obj(player1, 1)
    game_world.add_obj(player2, 1)
    game_world.add_collision_pair("character:ground", player1, ground)
    game_world.add_collision_pair("character:ground", player2, ground)
    # game_world.add_obj(megamen.MegaMen(), 1)


def finish():
    pass


def draw():
    clear_canvas()
    game_world.render()
    update_canvas()


def update():
    game_world.update()
    game_world.handle_collisons()
