from pico2d import hide_cursor, hide_lattice, clear_canvas, update_canvas, get_events, load_image, get_canvas_width, \
    get_canvas_height, load_font
from sdl2 import SDL_KEYDOWN, SDL_QUIT, SDLK_ESCAPE, SDLK_a, SDLK_RIGHT, SDLK_d, SDLK_LEFT, SDLK_f, SDLK_COMMA, \
    SDLK_SPACE, SDLK_RETURN

import ending_server
import game_framework
import menu_mode


def init():
    global background, font1, font2
    background = load_image("ending_scene.png")
    font1 = load_font("ENCR10B.TTF", 70)
    font2 = load_font("ENCR10B.TTF")
    ending_server.winner.win()


def finish():
    global background
    background = None
    ending_server.reset()


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                game_framework.quit()
            elif event.key == SDLK_RETURN:
                game_framework.change_mode(menu_mode)


def update():
    ending_server.winner.update()


def draw():
    clear_canvas()
    background.clip_draw_to_origin(0, 0, background.w, background.h, 0, 0, get_canvas_width(), get_canvas_height())
    ending_server.winner.draw()
    font2.draw(get_canvas_width() - get_canvas_width() / 3, 100, "Press Enter to Restart Game", (255,255,255))
    font1.draw(get_canvas_width() / 5, get_canvas_height() - 100, f"{ending_server.winner_name} Win!", (255, 0, 0))
    update_canvas()
