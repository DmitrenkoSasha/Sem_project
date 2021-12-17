from random import randint
import pygame
import pymunk
import pymunk.autogeometry
import pymunk.pygame_util
from equipment import Pear

W = 1000
H = 700


def lines_around_img(filename, width, height):
    """Приближает рисунок кривой
        Params:
            filename: [str] - название картинки, которую нужно окружить ломанной
            width: [float] - необходимая ширина изображения, каким оно будет видно на экране
            height: [float] - необходимая высота изображения
        return:
            [pymunk.autogeometry.PolylineSet] - массив координат
    """
    logo_img = pygame.image.load(filename).convert_alpha()
    logo_img = pygame.transform.scale(logo_img, (width, height))
    logo_bb = pymunk.BB(0, 0, logo_img.get_width(), logo_img.get_height())
    logo_img.lock()

    def sample_func(point):
        """ Необходима для march_soft
            Params:
                point: tuple[float, float] - координаты точки
            return:
                [int] целое число, отвечающее, как близко расположена ломанная к картинке, отриц. знач. не имеют смысла
        """
        try:
            p = pymunk.pygame_util.to_pygame(point, logo_img)
            color = logo_img.get_at(p)
            return color.a - 100
        except IndexError:
            return 0

    line_set = pymunk.autogeometry.march_soft(logo_bb, logo_img.get_width(), logo_img.get_height(), 99, sample_func)
    logo_img.unlock()
    return line_set


def create_square(space, x, y):
    square_body = pymunk.Body(body_type=pymunk.Body.STATIC)
    square_body.position = x, y
    square_shape = pymunk.Segment(square_body, (x, y), (x + 1, y + 1), 15)
    square_shape.elasticity = 10.0
    square_shape.friction = 0.1
    square_shape.friction = 1.0
    space.add(square_body, square_shape)


def common_walls(space):
    """
        Используется для прорисовки стен-границ всех комнат. Добавляет в space неподвижные прямоугольники - стены.
        Params:
            space: [pymunk.Space] - пространство pymunk, в которое будем добавлять объекты
    """
    floor_shape = pymunk.Segment(space.static_body, (0, H), (W, H), 30)
    space.add(floor_shape)

    left_wall_shape = pymunk.Segment(space.static_body, (0, 0), (0, H), 30)
    space.add(left_wall_shape)

    right_wall_shape = pymunk.Segment(space.static_body, (W, 0), (W, H), 30)
    space.add(right_wall_shape)

    roof_shape = pymunk.Segment(space.static_body, (0, 0), (W, 0), 30)
    space.add(roof_shape)


class TypicalWalls:
    """Обычная комната!"""

    def __init__(self, space):
        """ Конструктор комнаты
            Params:
                space: [pymunk.Space] - область создания
        """
        self.space = space
        self.event = pygame.USEREVENT + 1

    def run(self):
        """Запускает процесс создания комнаты. Вызывается в модуле battle_zone"""
        common_walls(self.space)
        small_balls = 100

        return small_balls


class FourExtraWalls:
    """Восемь стен!"""

    def __init__(self, space):
        """ Конструктор комнаты
            space: [pymunk.Space] - область создания
        """
        self.number = 1  # порядковый номер комнаты
        self.space = space
        self.things = []
        self.event = None

    def run(self):
        """Запускает процесс создания комнаты. Вызывается в модуле battle_zone"""
        common_walls(self.space)

        up_wall = pymunk.Segment(self.space.static_body, (W / 2, 0), (W / 2, H / 7), 50)
        self.space.add(up_wall)
        down_wall = pymunk.Segment(self.space.static_body, (W / 2, H * 6 / 7), (W / 2, H), 50)
        self.space.add(down_wall)
        right_wall = pymunk.Segment(self.space.static_body, (0, H / 2), (W * 0.3, H / 2), 50)
        self.space.add(right_wall)
        left_wall = pymunk.Segment(self.space.static_body, (W * 0.7, H / 2), (W, H / 2), 50)
        self.space.add(left_wall)

        p1 = Pear(self.space, W // 2, H // 2, 'задний план\\груша.png', self.number, 0.5)
        p2 = Pear(self.space, W // 2, 27 * H // 40, 'задний план\\груша.png', self.number, 0.5)

        self.things.append(p1)
        self.things.append(p2)

        return 0


class ThreeLevels:
    """Три этажа!"""

    def __init__(self, space):
        """pos_x: расстояние от левой стены до левого края платформы"""
        self.space = space
        self.img = pygame.image.load('задний план\\платформа.png').convert_alpha()
        self.width = round(W * 0.7)
        self.height = 50
        self.pos_x = W / 6
        self.event = None

    def run(self):
        """Запускает процесс создания комнаты. Вызывается в модуле battle_zone"""
        common_walls(self.space)
        line_set = lines_around_img('задний план\\платформа.png', self.width, self.height)

        for line in line_set:
            for i in range(3):  # три платформы
                for j in range(len(line) - 1):
                    shape = pymunk.Segment(self.space.static_body, line[j] +
                                           (self.pos_x, H / 4 + H / 4 * i),
                                           line[j + 1] + (self.pos_x, H / 4 + H / 4 * i), 1)
                    shape.friction = 0.5
                    shape.elasticity = 10.0
                    shape.color = (255, 255, 255, 255)
                    self.space.add(shape)

        return 0


class RandomCircleRoom:
    def __init__(self, space):
        self.space = space
        self.amount = 30
        self.balls_width = 40
        self.balls_height = 40
        self.stones_coord = []  # Список с координатами шариков, который используется while_rooms_events
        self.img1 = pygame.image.load('задний план\\камень коричневый.png').convert_alpha()
        self.img2 = pygame.image.load('задний план\\камень серый.png').convert_alpha()
        self.event = None

    def set_line(self, line, x, y):
        """Returns a copy of a polyline simplified by using the Douglas-Peucker algorithm"""
        line = pymunk.autogeometry.simplify_curves(line, 0.5)
        for j in range(len(line) - 1):
            shape = pymunk.Segment(self.space.static_body, line[j] + (x, y), line[j + 1] + (x, y), 1)
            shape.friction = 0.5
            shape.color = (25, 25, 25, 25)
            self.space.add(shape)

    def run(self):
        """Функция, запускающаяся в battle_zone после создания комнаты"""
        common_walls(self.space)

        line_set1 = lines_around_img('задний план\\камень коричневый.png', self.balls_width, self.balls_height)
        line_set2 = lines_around_img('задний план\\камень серый.png', self.balls_width, self.balls_height)

        #  Каждый круг описываем ломанной
        for i in range(1, self.amount, 1):
            #  Положение одного круга
            x = randint(50, W - 50)
            y = randint(50, H - 200)
            self.stones_coord.append((x, y))
            for line in line_set1:
                self.set_line(line, x, y)
            for line in line_set2:
                self.set_line(line, x, y)

        return 0


class ReverseGravity:
    """Поломка гравитации!"""

    def __init__(self, space):
        self.space = space
        self.event = pygame.USEREVENT + 2

    def run(self):
        """Функция, запускающаяся в battle_zone после создания комнаты"""
        common_walls(self.space)
        self.space.gravity = (0, -200)
        small_balls = 100

        return small_balls


def while_rooms_events(screen, room):
    """Вызывается в while loop в battle_zone. Для каждой комнаты отображает нужную картинку"""

    if type(room) is RandomCircleRoom:
        img1 = pygame.transform.scale(room.img1, (room.balls_width, room.balls_height))
        img2 = pygame.transform.scale(room.img2, (room.balls_width, room.balls_height))
        for i in range(room.amount - 1):
            if i % 2 == 0:
                (img_x, img_y) = room.stones_coord[i]
                screen.blit(img1, (img_x, img_y))
            else:
                (img_x, img_y) = room.stones_coord[i]
                screen.blit(img2, (img_x, img_y))

    elif type(room) is ThreeLevels:
        img = pygame.transform.scale(room.img, (room.width, room.height))
        screen.blit(img, (room.pos_x, H / 4))
        screen.blit(img, (room.pos_x, H / 2))
        screen.blit(img, (room.pos_x, 3 * H / 4))
    elif type(room) is FourExtraWalls:
        for one in room.things:
            if type(one) is Pear:
                rotated_img, vec_to_c, ps = one.rotate()
                screen.blit(rotated_img, (round(vec_to_c.x), round(vec_to_c.y)))


def create_room(space, number_of_room):
    """ Открывает нужную комнату
        Params:
            space: [pymunk.Space] - область создания
            number_of_room: [int] - порядковый номер комнаты
    return: представитель класса выбранной комнаты"""
    if number_of_room == 0:
        return TypicalWalls(space)

    if number_of_room == 1:
        return FourExtraWalls(space)

    if number_of_room == 2:
        return RandomCircleRoom(space)

    if number_of_room == 3:
        return ThreeLevels(space)

    if number_of_room == 4:
        return ReverseGravity(space)

if __name__ == 'main':
    print("This module is not for direct call!")