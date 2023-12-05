from pico2d import load_font

import game_framework


class Timer:
    def __init__(self, limit, pos):
        self.limit = limit
        self.font = load_font("ENCR10B.TTF", 50)
        self.pos = pos

    def draw(self):
        self.font.draw(self.pos[0] - 25, self.pos[1] + 50, f"{int(self.limit)}")

    def update(self):
        self.limit -= game_framework.frame_time
