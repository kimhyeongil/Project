from pico2d import get_events, clear_canvas, update_canvas, load_image, get_canvas_width, get_canvas_height
from sdl2 import SDL_QUIT, SDL_KEYDOWN, SDLK_ESCAPE

import ending_mode
import ending_server
import player1_control
import player2_control
import game_framework
import play_server
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
    play_server.timer = Timer(100, (get_canvas_width() / 2, get_canvas_height() - 100))
    game_world.add_obj(play_server.timer, 1)
    player1_control.portrait_pos = (0, get_canvas_height() - 100)
    player1_control.hp_bar_pos = (100, get_canvas_height() - 75)
    player1_control.gage_pos = (50, 25)

    player2_control.portrait_pos = (get_canvas_width() - 100, get_canvas_height() - 100)
    player2_control.hp_bar_pos = (get_canvas_width() - 100, get_canvas_height() - 75)
    player2_control.gage_pos = (get_canvas_width() - 50, 25)
    player2_control.x = get_canvas_width() - 100

    play_server.player1 = play_server.player1(player1_control)
    play_server.player2 = play_server.player2(player2_control)

    game_world.add_obj(play_server.player1, 3)
    game_world.add_obj(play_server.player2, 3)

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
    game_world.reset()
    play_server.reset()


def draw():
    clear_canvas()
    game_world.render()
    update_canvas()


def update():
    game_world.update()
    if play_server.player1.hp <= 0:
        ending_server.winner = play_server.player2
        ending_server.winner_name = "Player2"
        game_framework.change_mode(ending_mode)
    elif play_server.player2.hp <= 0:
        ending_server.winner = play_server.player1
        ending_server.winner_name = "Player1"
        game_framework.change_mode(ending_mode)
    elif int(play_server.timer.limit) <= 0:
        if play_server.player1.hp > play_server.player2.hp:
            ending_server.winner = play_server.player1
            ending_server.winner_name = "Player1"
        else:
            ending_server.winner = play_server.player2
            ending_server.winner_name = "Player2"
        game_framework.change_mode(ending_mode)

    game_world.handle_collisons()
