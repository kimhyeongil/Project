from pico2d import hide_cursor, hide_lattice, clear_canvas, update_canvas, get_events, load_image, get_canvas_width, \
    get_canvas_height
from sdl2 import SDL_KEYDOWN, SDL_QUIT, SDLK_ESCAPE, SDLK_a, SDLK_RIGHT, SDLK_d, SDLK_LEFT

import game_framework


def init():
    global menu, champions, player1, player2
    champions = list()
    player1 = 0
    player2 = 0
    champions.append(load_image("mario_portrait.png"))
    champions.append(load_image("megamen_portrait.png"))
    hide_cursor()
    hide_lattice()


def handle_events():
    global player1, player2

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                game_framework.quit()
            elif event.key == SDLK_d:
                player1 = (player1 + 1) % len(champions)
            elif event.key == SDLK_a:
                player1 -= 1
                if player1 < 0:
                    player1 = len(champions) - 1
            elif event.key == SDLK_RIGHT:
                player2 = (player2 + 1) % len(champions)
            elif event.key == SDLK_LEFT:
                player2 -= 1
                if player2 < 0:
                    player2 = len(champions) - 1


def update():
    pass


def draw():
    clear_canvas()
    champions[player1].clip_draw(0, 0, champions[player1].w, champions[player1].h, get_canvas_width() / 4,
                                 get_canvas_height() / 2, 200, 200)
    champions[player2].clip_draw(0, 0, champions[player2].w, champions[player2].h, get_canvas_width() / 2 + get_canvas_width() / 4,
                                 get_canvas_height() / 2, 200, 200)
    update_canvas()
