import pygame
import pymunk
import math
from pymunk.vec2d import Vec2d


class Pear(pygame.sprite.Sprite):
    def __init__(self, space, x, y, filename, numroom, scale):
        """Боксёрская груша, пользователь будет ставить её представителей, куда ему захочется,
         и возможно, что будут разные картинки.
         filename: название файла-картинки груши
         x, y: положение точки подвеса груши в пространстве space
         numroom: номер комнаты, в которую груша будет добавляться
         scale: коэф. растяжения картинки и тела, меняющийся от потребностей комнаты
         """
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(filename).convert_alpha()  # Графическое представление спрайта
        self.space = space
        self.vs = [(-27 * scale, 115 * scale), (25 * scale, 115 * scale), (27 * scale, -85 * scale),
                   (-27 * scale, -84 * scale), (0 * scale, -95 * scale)]
        self.scale = scale
        self.x, self.y = x, y
        self.mass = 50
        self.destinationroom = numroom
        self.body = self.add_body_pear()
        self.shape = self.add_shape_pear()
        self.filter = pymunk.ShapeFilter(mask=pymunk.ShapeFilter.ALL_MASKS() ^ 0b1)

    def add_body_pear(self):
        """Добавляет тело груши и точку вращения. Вызывается внутри класса Pear"""

        moment = pymunk.moment_for_poly(self.mass, self.vs)
        body = pymunk.Body(self.mass, moment)
        body.position = (self.x, self.y)

        rotation_center_body = pymunk.Body(body_type=pymunk.Body.STATIC)

        # Располагается на 130 выше центра масс груши - чуть больше половины картинки
        rotation_center_body.position = body.position + (0, -140 * self.scale)
        rotation_center_joint = pymunk.PinJoint(body, rotation_center_body, (0, -140 * self.scale), (0, 0))

        if self.destinationroom == 1:
            rotation_motor_body = pymunk.Body(body_type=pymunk.Body.STATIC)
            rotation_motor_body.position = body.position + (0, -140)
            rotation_motor_joint = pymunk.SimpleMotor(body, rotation_center_body, 1)
            self.space.add(rotation_motor_joint)

        self.space.add(rotation_center_joint)
        self.space.add(body)

        return body

    def add_shape_pear(self):
        """Добавляет форму для груши. Вызывается внутри класса Pear"""
        shape = pymunk.Poly(self.body, self.vs)
        shape.friction = 1
        shape.color = (255, 255, 255, 255)  # Чтоб не было видно
        self.space.add(shape)

        return shape

    def rotate(self):
        """Вращение картинки и красной рамки так, чтобы они всегда накладывалась на тело
        :return: rotated_img - картинка, повёрнутая вокруг своего геом.центра
                           vc - вектор к геом.центру рисунка
                          coords_vs - координаты вершин красной рамки вокруг картинки"""
        # Вектор к точке поворота; Остаётся постоянным 650,200
        vec_rot = self.shape.body.position
        vec_rot = Vec2d(vec_rot.x, vec_rot.y)

        # Нужно повернуть на 180 градусов
        angle_degrees = -math.degrees(self.shape.body.angle)
        rotated_img = pygame.transform.rotate(self.image, angle_degrees)
        if self.destinationroom == 1:
            rotated_img = pygame.transform.scale(rotated_img, (round(rotated_img.get_rect().size[0] * self.scale),
                                                               round(rotated_img.get_rect().size[1] * self.scale)))

        # Координаты красной рамки вокруг картинки
        coords_vs = [
            vertice.rotated(self.shape.body.angle) + self.shape.body.position
            for vertice in self.shape.get_vertices()]

        coords_vs = [(round(one.x), round(one.y)) for one in coords_vs]
        coords_vs += [coords_vs[0]]

        #  Для смещения лев.верх. угла пов-ти рисунка
        offset_x = rotated_img.get_rect().size[0] / 2
        offset_y = rotated_img.get_rect().size[1] / 2
        offset = Vec2d(offset_x, offset_y)

        #  Вектор к центру картинки
        vc = vec_rot - Vec2d(*offset)

        return rotated_img, vc, coords_vs

    def update(self, *args):
        pass


class Ball(pygame.sprite.Sprite):

    def __init__(self, space, pos_x, pos_y):
        pygame.sprite.Sprite.__init__(self)
        self.space = space
        self.pos = (pos_x, pos_y)

    def add_ball(self, space):
        body = pymunk.Body()
        body.position = Vec2d(*self.pos)
        shape = pymunk.Circle(body, 50)
        shape.mass = 1
        shape.color = (255, 25, 255, 255)
        shape.friction = 0.7
        space.add(body, shape)


class Weight:
    def __init__(self):
        self.img = pygame.image.load('задний план\\гиря.png').convert_alpha()


if __name__ == 'main':
    print("This module is not for direct call!")
