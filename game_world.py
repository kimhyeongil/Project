world = [[] for _ in range(10)]


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
