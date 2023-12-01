from pico2d import load_image


class HPBar:
    remain_hp_img = None
    size = 250

    def __init__(self, O, maxHP, dir):
        if HPBar.remain_hp_img == None:
            HPBar.remain_hp_img = load_image("remain_hp.png")
        self.O = O
        self.HP = maxHP
        self.maxHP = maxHP
        self.dir = dir
        self.w = HPBar.remain_hp_img.w
        self.h = HPBar.remain_hp_img.h

    def draw(self):
        self.remain_hp_img.clip_draw(0, 0, self.w, self.h,
                                     self.O[0] - (self.HP / self.maxHP * HPBar.size * self.dir) // 2, self.O[1],
                                     (self.HP / self.maxHP * HPBar.size) // 2 * 2, 50)

    def update(self):
        pass
