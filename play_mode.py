from pico2d import get_events, clear_canvas, update_canvas, load_image
from sdl2 import SDL_QUIT, SDL_KEYDOWN, SDLK_ESCAPE

import player1_control
import player2_control
import game_framework
import play_sever
from mario import Mario
import game_world
from megamen import MegaMen
import megamen_projectile
from ground import Ground


def init():
    megamen_projectile.projectile = load_image('megamen.png')
    play_sever.player1 = MegaMen(player1_control)
    play_sever.player2 = Mario(player2_control)
    play_sever.ground = Ground(300)
    game_world.add_obj(play_sever.player1, 1)
    game_world.add_obj(play_sever.player2, 1)
    game_world.add_collision_pair("knuckle:ground", None, play_sever.ground)
    game_world.add_collision_pair("Player1:Player2", None, play_sever.player2)
    game_world.add_collision_pair("Player2:Player1", None, play_sever.player1)


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
            play_sever.player1.handle_event(event)
            play_sever.player2.handle_event(event)


def finish():
    pass


def draw():
    clear_canvas()
    game_world.render()
    update_canvas()


def update():
    game_world.update()
    game_world.handle_collisons()
