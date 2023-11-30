from pico2d import *


class FixedBackground:

    def __init__(self):
        self.image = load_image('Background.png')
        self.cw = get_canvas_width()
        self.ch = get_canvas_height()
        self.w = self.image.w
        self.h = self.image.h

    def draw(self):
        self.image.clip_draw_to_origin(0, 0, self.w, self.h, 0, 0, self.cw, self.ch)

    def update(self):
        pass

    def handle_event(self, event):
        pass
