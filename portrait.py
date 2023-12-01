class Portrait:
    def __init__(self, img, O):
        self.img = img
        self.img_info = (0,0,img.w, img.h)
        self.O = O

    def draw(self):
        self.img.clip_draw_to_origin(*self.img_info, self.O[0], self.O[1], 100, 100)

    def update(self):
        pass
