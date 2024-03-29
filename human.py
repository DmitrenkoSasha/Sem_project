import pygame
import pymunk
import pymunk.pygame_util


collision_types = (0, 1, 2, 3)


class Human:
    """Класс, отвечающий за создание палочных людей. Таковые создаются в модулях gym и battle_zone"""
    def __init__(self, space):
        """ Конструктор класса Human
            :param (pymunk.Space) space: область создания
        """
        self.space = space
        self.shapes = []
        self.complect = []
        self.points = 0
        self.scale = 1

    def add_lever(self, pos, x1, x2, width, category, mask, collision_type):
        """ Создаёт элемент человека
                :param (float, float) pos: позиция человека
                :param (float) x1: координаты первого края палки центра человека
                :param (float) x2: координаты второго края палки относительно центра человека
                :param float width: толщина палки
                :param int category: категория объекта, число в формате 2^n
                :param int mask: маска объекта, сумма чисел в формате 2^n, отвечает за столкновения
                :param int collision_type: тип столкновений для этого объекта из collision_types

                :return: присваивает переменной вид физического тела
        """
        body = pymunk.Body()
        body.position = pos
        shape = pymunk.Segment(body, x1, x2, width * self.scale)
        shape.mass = 1
        shape.friction = 50
        shape.color = pygame.Color('blue')
        shape.filter = pymunk.ShapeFilter(categories=category, mask=mask)
        shape.collision_type = collision_types[collision_type]
        self.shapes.append(shape)
        self.space.add(body, shape)
        return body

    def create_human(self, x, y, scale=1):
        """ Создаёт человека поэлементно, с добавлением суставов и пружин
            Args:
            :param float x: x-координата центра тела человека
            :param float y: y-координата центра тела человека
            :param int scale: параметр, отвечающий за размер человека
        """
        head = self.add_lever((x, y), (0, -30 * scale), (0, -32 * scale), 18, 1, 1021, 0)
        telo = self.add_lever((x, y), (0, 30 * scale), (0, -30 * scale), 6, 2, 682, 1)
        c_head_body = pymunk.PivotJoint(head, telo, (x, y - 30 * scale))
        self.space.add(c_head_body)

        right_arm = self.add_lever((x, y), (0, -5 * scale), (15 * scale, -20 * scale), 6, 16, 985, 2)
        right_hand = self.add_lever((x, y), (15 * scale, -20 * scale), (40 * scale, -45 * scale), 6, 32, 991, 3)
        c_right_arm = pymunk.PivotJoint(right_arm, right_hand, (x + 15 * scale, y - 20 * scale))
        self.space.add(c_right_arm)

        left_arm = self.add_lever((x, y), (0, -5 * scale), (-15 * scale, -20 * scale), 6, 4, 997, 2)
        left_hand = self.add_lever((x, y), (-15 * scale, -20 * scale), (-40 * scale, -45 * scale), 6, 8, 1019, 3)
        c_left_arm = pymunk.PivotJoint(left_arm, left_hand, (x - 15 * scale, y - 20 * scale))
        self.space.add(c_left_arm)

        c_body_right_arm = pymunk.PivotJoint(right_arm, telo, (x, y - 5 * scale))
        c_body_left_arm = pymunk.PivotJoint(left_arm, telo, (x, y - 5 * scale))
        spring_body_right_arm = pymunk.DampedSpring(telo, right_arm, (0, 20 * scale), (20 * scale, -20 * scale),
                                                    40 * scale, 200, 0.3)
        spring_body_left_arm = pymunk.DampedSpring(telo, left_arm, (0, 20 * scale), (-20 * scale, -20 * scale),
                                                   40 * scale, 200, 0.3)
        self.space.add(c_body_right_arm)
        self.space.add(c_body_left_arm)
        self.space.add(spring_body_right_arm)
        self.space.add(spring_body_left_arm)

        right_leg = self.add_lever((x, y), (0, 30 * scale), (20 * scale, 50 * scale), 6, 256, 477, 2)
        right_feet = self.add_lever((x, y), (20 * scale, 50 * scale), (20 * scale, 80 * scale), 6, 512, 767, 3)
        c_right_leg = pymunk.PivotJoint(right_leg, right_feet, (x + 20 * scale, y + 50 * scale))
        self.space.add(c_right_leg)

        left_leg = self.add_lever((x, y), (0, 30 * scale), (-20 * scale, 50 * scale), 6, 64, 637, 2)
        left_feet = self.add_lever((x, y), (-20 * scale, 50 * scale), (-20 * scale, 80 * scale), 6, 128, 959, 3)
        c_left_leg = pymunk.PivotJoint(left_leg, left_feet, (x - 20 * scale, y + 50 * scale))
        self.space.add(c_left_leg)

        c_body_right_leg = pymunk.PivotJoint(right_leg, telo, (x, y + 30 * scale))
        c_body_left_leg = pymunk.PivotJoint(left_leg, telo, (x, y + 30 * scale))
        spring_legs = pymunk.DampedSpring(left_feet, right_feet, (-20 * scale, 70 * scale), (20 * scale, 70 * scale),
                                          40 * scale, 500, 50)
        spring_legs_2 = pymunk.DampedSpring(left_leg, right_leg, (-20 * scale, 50 * scale),
                                            (20 * scale, 50 * scale), 50 * scale, 500, 50)
        spring_body_right_leg = pymunk.DampedSpring(telo, right_feet, (0, 20 * scale), (20 * scale, 70 * scale),
                                                    70 * scale, 500, 0.3)
        spring_body_left_leg = pymunk.DampedSpring(telo, left_feet, (0, 20 * scale), (-20 * scale, 70 * scale),
                                                   70 * scale, 500, 0.3)
        self.space.add(c_body_right_leg)
        self.space.add(c_body_left_leg)
        self.space.add(spring_legs)
        self.space.add(spring_legs_2)
        self.space.add(spring_body_right_leg)
        self.space.add(spring_body_left_leg)

        self.complect = ([head, telo, right_arm, left_arm,
                          right_leg, left_leg])
        self.points = 100

    def check_event_human(self, up, left, down, right):
        """ Отвечает за перемещение человека с помощью кнопок
            :param int up: - кнопка для движения вверх
            :param int left: - кнопка для движения влево
            :param int down: - кнопка для движения вниз
            :param int right: - кнопка для движения вправо
        """
        if pygame.key.get_pressed()[right]:
            for part in self.complect:
                part.velocity += (30, 0)
        if pygame.key.get_pressed()[left]:
            for part in self.complect:
                part.velocity += (-30, 0)
        if pygame.key.get_pressed()[up]:
            for part in self.complect:
                part.velocity += (0, -30)
        if pygame.key.get_pressed()[down]:
            for part in self.complect:
                part.velocity += (0, 30)
