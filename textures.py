import pymunk
import random
import pygame
import pymunk.autogeometry
import pymunk.pygame_util
W = 1000
H = 700

def create_floor(space, x, y):
    floor_body = pymunk.Body(body_type=pymunk.Body.STATIC)
    floor_body.position = x, y
    floor_shape = pymunk.Poly.create_box(floor_body, (W*0.7, 10))
    floor_shape.elasticity = 10.0
    floor_shape.friction = 1.0
    space.add(floor_body, floor_shape)

def create_square(space, x, y):
    square_body = pymunk.Body(body_type=pymunk.Body.STATIC)
    square_body.position = x, y
    square_shape = pymunk.Segment(square_body, (x, y), (x+1, y+1), 15)
    square_shape.elasticity = 10.0
    square_shape.friction = 0.1
    square_shape.friction = 1.0
    space.add(square_body, square_shape)

def common_walls(space):
    floor_shape = pymunk.Segment(space.static_body, (0, H), (W, H), 50)
    space.add(floor_shape)

    left_wall_shape = pymunk.Segment(space.static_body, (0, 0), (0, H), 50)
    space.add(left_wall_shape)

    right_wall_shape = pymunk.Segment(space.static_body, (W, 0), (W, H), 50)
    space.add(right_wall_shape)

    roof_shape = pymunk.Segment(space.static_body, (0, 0), (W, 0), 50)
    space.add(roof_shape)

def four_extra_walls(space):
    common_walls(space)

    up_wall = pymunk.Segment(space.static_body, (W/2, 0), (W/2, H*2/7), 50)
    space.add(up_wall)
    down_wall = pymunk.Segment(space.static_body, (W/2, H*5/7), (W/2, H), 50)
    space.add(down_wall)
    right_wall = pymunk.Segment(space.static_body, (0, H/2), (W*0.3, H/2), 50)
    space.add(right_wall)
    left_wall = pymunk.Segment(space.static_body, (W*0.7, H/2), (W, H/2), 50)
    space.add(left_wall)

def three_levels(space):
    common_walls(space)

    create_floor(space, W/2, H/4)
    create_floor(space, W/2, H/2)
    create_floor(space, W/2, 3*H/4)

class random_circle_room():
    def __init__(self, space):
        self.space = space
        self.amount = 20
        self.size = (40, 40)
        self.coord = []  # Список с координатами шариков, который используется while_rooms_events

    def lines_around_img(self, filename, w, h):
        logo_img = pygame.image.load(filename).convert_alpha()
        logo_img = pygame.transform.scale(logo_img, (w, h))
        logo_bb = pymunk.BB(0, 0, logo_img.get_width(), logo_img.get_height())
        logo_img.lock()

        def sample_func(point):
            try:
                p = pymunk.pygame_util.to_pygame(point, logo_img)
                color = logo_img.get_at(p)

                return color.a

            except:
                return 0

        line_set = pymunk.autogeometry.march_soft(logo_bb, logo_img.get_width(), logo_img.get_height(), 99, sample_func)
        logo_img.unlock()

        return line_set

    def run(self):
        common_walls(self.space)

        line_set = self.lines_around_img('мяч.png', 50, 50)
        #coords = []  # Список с координатами шариков, который используется while_rooms_events
        for i in range(1, self.amount, 1):
            x = random.randint(100, W-100)
            y = random.randint(100, H-100)
            self.coord.append((x, y))
            for line in line_set:

                # Returns a copy of a polyline simplified by using the Douglas-Peucker algorithm
                line = pymunk.autogeometry.simplify_curves(line, 0.7)

                for i in range(len(line) - 1):
                    shape = pymunk.Segment(self.space.static_body, line[i] + (x, y), line[i + 1] + (x, y), 1)
                    shape.friction = 0.5
                    shape.color = (255, 0, 0, 0)
                    self.space.add(shape)
            #create_square(space, x/2, y/2)


def gravity_change(space):
    common_walls(space)

    space.gravity = (0, -200)

def while_rooms_events(screen, room):
    """Вызывается в while loop в battle_zone"""

    if type(room) is random_circle_room:
        img = pygame.image.load('мяч.png').convert_alpha()
        img = pygame.transform.scale(img, (50, 50))
        for i in range(room.amount-1):
            (img_x, img_y) = room.coord[i]
            screen.blit(img, (img_x, img_y))

def create_room(space, number_of_room):
    """Открывает нужную комнату"""
    if number_of_room == 0:
        common_walls(space)
    if number_of_room == 1:
        four_extra_walls(space)
    if number_of_room == 2:
        three_levels(space)
    if number_of_room == 3:
        return random_circle_room(space)
        #random_circles(space)
    if number_of_room == 4:
        gravity_change(space)