from pico2d import get_events, clear_canvas, update_canvas, load_image, get_canvas_width, get_canvas_height
from sdl2 import SDL_QUIT, SDL_KEYDOWN, SDLK_ESCAPE

import player1_control
import player2_control
import game_framework
import play_server
from hp_bar import HPBar
from mario import Mario
import game_world
from background import FixedBackground as Background
from megamen import MegaMen
import megamen_projectile
from ground import Ground
from timer import Timer


def init():
    megamen_projectile.projectile = load_image('megamen.png')
    play_server.ground = Ground(100)
    game_world.add_obj(play_server.ground, 1)
    game_world.add_obj(Background(), 0)
    game_world.add_obj(Timer(99, (get_canvas_width() / 2, get_canvas_height() - 100)), 1)
    player1_control.portrait_pos = (0, get_canvas_height() - 100)
    player1_control.hp_bar_pos = (100, get_canvas_height() - 75)

    player2_control.portrait_pos = (get_canvas_width() - 100, get_canvas_height() - 100)
    player2_control.hp_bar_pos = (get_canvas_width() - 100, get_canvas_height() - 75)

    player2_control.x = get_canvas_width() - 100

    play_server.player1 = Mario(player1_control)
    play_server.player2 = MegaMen(player2_control)

    game_world.add_obj(play_server.player1, 2)
    game_world.add_obj(play_server.player2, 2)

    game_world.add_collision_pair("knuckle:ground", None, play_server.ground)
    game_world.add_collision_pair("Player1:Player2", None, play_server.player2)
    game_world.add_collision_pair("Player2:Player1", None, play_server.player1)


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
            play_server.player1.handle_event(event)
            play_server.player2.handle_event(event)


def finish():
    pass


def draw():
    clear_canvas()
    game_world.render()
    update_canvas()


def update():
    game_world.update()
    game_world.handle_collisons()
