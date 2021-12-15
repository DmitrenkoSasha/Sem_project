import random

import pygame
import pymunk
import pymunk.autogeometry
import pymunk.pygame_util

W = 1000
H = 700


def lines_around_img(filename, width, height):
    """Приближает рисунок кривой
    filename: название картинки, которую нужно окружить ломанной
    width: необходимая ширина изображения, каким оно будет видно на экране
    height: необходимая высота изображения
    return: pymunk.autogeometry.PolylineSet object - массив координат
    """
    logo_img = pygame.image.load(filename).convert_alpha()
    logo_img = pygame.transform.scale(logo_img, (width, height))
    logo_bb = pymunk.BB(0, 0, logo_img.get_width(), logo_img.get_height())
    logo_img.lock()

    def sample_func(point):
        """Необходима для march_soft
        return: целое число, отвечающее, как близко расположена ломанная к картинке, отриц. знач. не имеют смысла"""
        try:
            p = pymunk.pygame_util.to_pygame(point, logo_img)
            color = logo_img.get_at(p)
            return color.a - 100
        except:
            return 0

    line_set = pymunk.autogeometry.march_soft(logo_bb, logo_img.get_width(), logo_img.get_height(), 99, sample_func)
    logo_img.unlock()
    return line_set


def create_floor(space, x, y):
    floor_body = pymunk.Body(body_type=pymunk.Body.STATIC)
    floor_body.position = x, y
    floor_shape = pymunk.Poly.create_box(floor_body, (W * 0.7, 10))
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
    left_wall = pymunk.Segment(space.static_body, (W * 0.7, H / 2), (W, H / 2), 50)
    space.add(left_wall)

class three_levels():
    def __init__(self, space):
        self.space = space
        self.img = pygame.image.load('мяч.png').convert_alpha()

    def run(self):
        """Функция, запускающаяся в battle_zone после создания комнаты"""
        common_walls(self.space)
        create_floor(self.space, W / 2, H / 4)  # TODO избавиться от глобальных W, H
        create_floor(self.space, W / 2, H / 2)
        create_floor(self.space, W / 2, 3 * H / 4)


class random_circle_room:
    def __init__(self, space):
        self.space = space
        self.amount = 20
        self.width = 40
        self.height = 40
        self.coord = []  # Список с координатами шариков, который используется while_rooms_events
        self.img = pygame.image.load('мяч.png').convert_alpha()

    def run(self):
        """Функция, запускающаяся в battle_zone после создания комнаты"""
        common_walls(self.space)

        line_set = lines_around_img('мяч.png', self.width, self.height)

        # Каждый круг описываем ломанной
        for i in range(1, self.amount, 1):
            # Положение одного круга
            x = random.randint(50, W - 100) # TODO избавиться от глобальных переменных
            y = random.randint(50, H - 100)
            self.coord.append((x, y))
            for line in line_set:

                # Returns a copy of a polyline simplified by using the Douglas-Peucker algorithm
                line = pymunk.autogeometry.simplify_curves(line, 0.7)

                for j in range(len(line) - 1):
                    shape = pymunk.Segment(self.space.static_body, line[j] + (x, y), line[j + 1] + (x, y), 1)
                    shape.friction = 0.5
                    shape.color = (255, 255, 255, 255)
                    self.space.add(shape)


def gravity_change(space):
    common_walls(space)

    space.gravity = (0, -200)

def while_rooms_events(screen, room):
    """Вызывается в while loop в battle_zone. Для каждой комнаты отображает нужную картинку"""

    if type(room) is random_circle_room:
        img = pygame.transform.scale(room.img, (room.width, room.height))
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
        return random_circle_room(space)

    if number_of_room == 3:
        return three_levels(space)

    if number_of_room == 4:
        gravity_change(space)
