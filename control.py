from sdl2 import SDL_KEYDOWN, SDLK_d, SDLK_a, SDL_KEYUP, SDLK_h


class Player1:
    @staticmethod
    def move_r_down(e):
        return e[0] == "INPUT" and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_d

    @staticmethod
    def move_l_down(e):
        return e[0] == "INPUT" and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_a

    @staticmethod
    def move_r_up(e):
        return e[0] == "INPUT" and e[1].type == SDL_KEYUP and e[1].key == SDLK_d

    @staticmethod
    def move_l_up(e):
        return e[0] == "INPUT" and e[1].type == SDL_KEYUP and e[1].key == SDLK_a

    @staticmethod
    def jump_down(e):
        return e[0] == "INPUT" and e[1].type == SDL_KEYUP and e[1].key == SDLK_h
