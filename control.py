from sdl2 import SDL_KEYDOWN, SDLK_d, SDLK_a


class Player1:
    @staticmethod
    def move_r_down(e):
        return e[0] == "INPUT" and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_d

    @staticmethod
    def move_l_down(e):
        return e[0] == "INPUT" and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_a
