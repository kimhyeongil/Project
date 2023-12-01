from pico2d import load_image


class HPBar:
    remain_hp_img = None
    size = 250
    def __init__(self, O):
        if HPBar.remain_hp_img == None:
            HPBar.remain_hp_img = load_image("remain_hp.png")
        self.O = O

    def draw(self):
        HPBar.remain_hp_img.clip_draw_to_origin(0, 0, HPBar.remain_hp_img.w, HPBar.remain_hp_img.h, *self.O, HPBar.size, 50)

    def update(self):
        pass
