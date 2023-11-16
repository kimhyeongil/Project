class Ground:
    def __init__(self, y):
        self.y = y

    def get_bb(self):
        return -10000, self.y, 10000, self.y

    def handle_collision(self, group, other):
        pass
