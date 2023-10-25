world = [[] for _ in range(10)]

time_slice = 0.1
g = 100
ground = 300
def add_obj(o, depth):
    world[depth].append(o)


def render():
    for layer in world:
        for o in layer:
            o.draw()


def update():
    for layer in world:
        for o in layer:
            o.update()

def erase_obj(o):
    for layer in world:
        if o in layer:
            layer.remove(o)
            return