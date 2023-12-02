from pico2d import hide_cursor, hide_lattice, clear_canvas, update_canvas, get_events, load_image, get_canvas_width, \
    get_canvas_height
from sdl2 import SDL_KEYDOWN, SDL_QUIT, SDLK_ESCAPE, SDLK_a, SDLK_RIGHT, SDLK_d, SDLK_LEFT, SDLK_f, SDLK_COMMA

import game_framework
import play_mode
import play_server
import player1_control
from mario import Mario
from megamen import MegaMen


def init():
    global menu, champions_portrait, player1, player2, champions
    champions_portrait = list()
    champions = dict()
    player1 = 0
    player2 = 0
    champions_portrait.append(load_image("mario_portrait.png"))
    champions_portrait.append(load_image("megamen_portrait.png"))
    champions[0] = Mario
    champions[1] = MegaMen
    hide_cursor()
    hide_lattice()


def finish():
    global menu, champions_portrait, player1, player2, champions
    menu = None
    champions_portrait = None
    champions = None


def handle_events():
    global player1, player2

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                game_framework.quit()
            elif event.key == SDLK_f:
                if play_server.player1 == None:
                    play_server.player1 = champions[player1]
            elif event.key == SDLK_COMMA:
                if play_server.player2 == None:
                    play_server.player2 = champions[player2]
            if play_server.player1 == None:
                if event.key == SDLK_d:
                    player1 = (player1 + 1) % len(champions_portrait)
                elif event.key == SDLK_a:
                    player1 -= 1
                    if player1 < 0:
                        player1 = len(champions_portrait) - 1
            if play_server.player2 == None:
                if event.key == SDLK_RIGHT:
                    player2 = (player2 + 1) % len(champions_portrait)
                elif event.key == SDLK_LEFT:
                    player2 -= 1
                    if player2 < 0:
                        player2 = len(champions_portrait) - 1


def update():
    if play_server.player1 and play_server.player2:
        game_framework.change_mode(play_mode)


def draw():
    clear_canvas()
    champions_portrait[player1].clip_draw(0, 0, champions_portrait[player1].w, champions_portrait[player1].h,
                                          get_canvas_width() / 4, get_canvas_height() / 2, 200, 200)
    champions_portrait[player2].clip_draw(0, 0, champions_portrait[player2].w, champions_portrait[player2].h,
                                          get_canvas_width() / 2 + get_canvas_width() / 4, get_canvas_height() / 2, 200,
                                          200)
    update_canvas()
