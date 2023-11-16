world = [[] for _ in range(10)]
collision_pairs = {}
PIXEL_PER_METER = 100 / 2.5  # 100픽셀 당 1미터

g = 40
time_slice = 0.01
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
            erase_collision_object(o)
            del o
            return


def erase_collision_object(o):
    for pairs in collision_pairs.values():
        if o in pairs[0]:
            pairs[0].remove(o)
        if o in pairs[1]:
            pairs[1].remove(o)


def add_collision_pair(group, a, b):
    if group not in collision_pairs:
        print(f"add {group}")
        collision_pairs[group] = [[], []]
    if a:
        collision_pairs[group][0].append(a)
    if b:
        collision_pairs[group][1].append(b)


def collide(a, b):
    aboxes = a.get_bb()
    bboxes = b.get_bb()
    for abox in aboxes:
        for bbox in bboxes:
            al, ab, ar, at = abox
            bl, bb, br, bt = bbox
            if al <= br and ab <= bt and at >= bb and ar >= bl:
                return True
    return False


def handle_collisons():
    for group, pairs in collision_pairs.items():
        for a in pairs[0]:
            for b in pairs[1]:
                if collide(a, b):
                    a.handle_collision(group, b)
                    b.handle_collision(group, a)
