import pygame  # sprites, transform, images
import pymunk
from math import degrees
from pymunk.vec2d import Vec2d


class Pear(pygame.sprite.Sprite):
    def __init__(self, space, x, y, filename, numroom, scale):
        """Боксёрская груша, пользователь будет ставить её представителей, куда ему захочется,
         и возможно, что будут разные картинки.
            :param str filename: название файла-картинки груши
            :param float x: положение точки подвеса груши в пространстве space
            :param float y: положение точки подвеса груши в пространстве space
            :param int numroom: номер комнаты, в которую груша будет добавляться
            :param float scale: коэф. растяжения картинки и тела, меняющийся от потребностей комнаты
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
        angle_degrees = -degrees(self.shape.body.angle)
        rotated_img = pygame.transform.rotate(self.image, angle_degrees)
        if self.destinationroom == 1:  # Если вызывается в комнате с 8 стенами
            rotated_img = pygame.transform.scale(rotated_img, (round(rotated_img.get_rect().size[0] * self.scale),
                                                               round(rotated_img.get_rect().size[1] * self.scale)))

        # Координаты красной рамки вокруг body.shape
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


class Ball(pygame.sprite.Sprite):
    """Падающие розовые мячики"""
    def __init__(self, space, pos_x, pos_y):
        """Конструктор класса Ball
            :param pymunk.Space space: пространство для создания
            :param float pos_x: положение центра по оси x
            :param float pos_y: положение центра по оси y
        """
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


if __name__ == 'main':
    print("This module is not for direct call!")
