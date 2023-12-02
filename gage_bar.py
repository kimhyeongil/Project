from pico2d import load_image, load_font


class GageBar:
    bar_img = None
    font = None
    size = 150

    def __init__(self, O, dir):
        if GageBar.bar_img == None:
            GageBar.bar_img = load_image("gage_bar.png")
            GageBar.font = load_font("ENCR10B.TTF", 20)
        self.O = O
        self.gage = 0.99
        self.dir = dir
        self.barW = GageBar.bar_img.w
        self.barH = GageBar.bar_img.h

    def draw(self):
        GageBar.bar_img.clip_draw(0, 0, self.barW, self.barH,
                                  self.O[0] - ((self.gage - int(self.gage)) * GageBar.size // 2 * self.dir),
                                  self.O[1] - 12.5,
                                  ((self.gage - int(self.gage)) * GageBar.size // 2) * 2, 25)
        GageBar.bar_img.clip_draw(0, 0, self.barW, self.barH,
                                  self.O[0] + (25 * self.dir), self.O[1], 50, 50)
        if self.dir < 0:
            GageBar.font.draw(self.O[0] - 30, self.O[1], f"{int(self.gage)}", (255, 255, 255))
        else:
            GageBar.font.draw(self.O[0] + 20, self.O[1], f"{int(self.gage)}", (255, 255, 255))

    def update(self):
        pass
