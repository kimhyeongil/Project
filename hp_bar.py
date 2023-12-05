from pico2d import load_image


class HPBar:
    remain_hp_img = None
    hp_back_img = None
    size = 250

    def __init__(self, O, maxHP, dir):
        if HPBar.remain_hp_img == None:
            HPBar.remain_hp_img = load_image("remain_hp.png")
            HPBar.hp_back_img = load_image("hp_back.png")
        self.O = O
        self.HP = maxHP
        self.maxHP = maxHP
        self.dir = dir
        self.w = HPBar.remain_hp_img.w
        self.h = HPBar.remain_hp_img.h

    def draw(self):
        if self.dir < 0:
            HPBar.hp_back_img.clip_draw_to_origin(0, 0, self.w, self.h, *self.O, HPBar.size, 50)
            HPBar.remain_hp_img.clip_draw_to_origin(0, 0, self.w, self.h,
                                                    *self.O, (self.HP / self.maxHP * HPBar.size), 50)
        else:
            HPBar.hp_back_img.clip_draw_to_origin(0, 0, self.w, self.h, self.O[0] - HPBar.size, self.O[1], HPBar.size,
                                                  50)
            HPBar.remain_hp_img.clip_draw_to_origin(0, 0, self.w, self.h,
                                                    self.O[0] - int(self.HP / self.maxHP * HPBar.size), self.O[1],
                                                    int(self.HP / self.maxHP * HPBar.size), 50)

    def update(self):
        pass
