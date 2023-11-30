from pico2d import load_image, get_canvas_width, get_canvas_height


class Ground:
    def __init__(self, y):
        self.y = y
        self.img = load_image("ground.png")

    def get_bb(self):
        return -10000, self.y, 10000, self.y

    def draw(self):
        self.img.clip_draw(0, 0, self.img.w, self.img.h, get_canvas_width() / 2, self.y / 2, get_canvas_width(), self.y)

    def update(self):
        pass

    def handle_collision(self, group, other):
        pass
