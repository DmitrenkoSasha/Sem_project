import pygame
import pymunk
import math
from pymunk.vec2d import Vec2d


class Pear(pygame.sprite.Sprite):
    def __init__(self, space, x, y, filename):
        """Боксёрская груша, пользователь будет ставить её представителей, куда ему захочется,
         и возможно, что будут разные картинки.
         filename: название файла-картинки груши
         x, y: положение точки подвеса груши в пространстве space"""
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(filename).convert_alpha()  # Графическое представление спрайта
        #self.rect = self.image.get_rect(center=(x, 200))  # Положение и размер спрайта
        self.space = space
        #self.vs = [(-28, 265), (28, 265), (28, 63), (-28, 63), (0, 50), (0, 270)]
        self.vs = [(-28, 120), (28, 120), (28, -90), (-28, -90), (0, -100)]
        self.x, self.y = x, y
        self.mass = 100
        self.body = self.add_body_pear()
        self.shape = self.add_shape_pear()
        # self.filter = pymunk.ShapeFilter(categories=0b1)
        self.filter = pymunk.ShapeFilter(mask=pymunk.ShapeFilter.ALL_MASKS() ^ 0b1)

        self.bb = pymunk.BB(0, 0, self.image.get_width(), self.image.get_height())


    def add_body_pear(self):
        """Добавляет тело груши и точку вращения. Вызывается внутри класса Pear"""
        moment = pymunk.moment_for_poly(self.mass, self.vs)
        body = pymunk.Body(self.mass, moment)
        body.position = (self.x, self.y)
        rotation_center_body = pymunk.Body(body_type=pymunk.Body.STATIC)
        #rotation_center_body.position = body.position
        rotation_center_body.position = body.position + (0, -130)
        rotation_center_joint = pymunk.PinJoint(body, rotation_center_body, (0, -130), (0, 0))
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
                           p - вектор к геом.центру рисунка
                          ps - координаты вершин красной рамки вокруг картинки"""
        # Вектор к точке поворота; Остаётся постоянным 650,200
        vec_rot = self.shape.body.position
        vec_rot = Vec2d(vec_rot.x, vec_rot.y)

        # Нужно повернуть на 180 градусов
        angle_degrees = -math.degrees(self.shape.body.angle)
        rotated_img = pygame.transform.rotate(self.image, angle_degrees)

        # Координаты красной рамки вокруг картинки
        ps = [
            vertice.rotated(self.shape.body.angle) + self.shape.body.position
            for vertice in self.shape.get_vertices()]

        ps = [(round(p.x), round(p.y)) for p in ps]
        ps += [ps[0]]


        #  Для смещения лев.верх. угла пов-ти рисунка
        offset_x = rotated_img.get_rect().size[0] / 2
        offset_y = rotated_img.get_rect().size[1] / 2
        offset = Vec2d(offset_x, offset_y)

        #  Ищу полусумму двух векторов vec0, vec2 к диагонально противоположным точкам
        vec0 = Vec2d(-30, 0).rotated(self.shape.body.angle) + self.shape.body.position
        vec2 = Vec2d(30, 300).rotated(self.shape.body.angle) + self.shape.body.position
        #  Расположение центра рисунка
        #offset2 = (Vec2d(*vec0 - self.shape.body.position) + Vec2d(*vec2 - self.shape.body.position)) / 2

        #  Вектор к центру картинки
        p = vec_rot - Vec2d(*offset) #+ offset2

        return rotated_img, p, ps


    def update(self, *args):
        pass


    def check_event_pear(self, event, mouse_joint, mouse_body):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if mouse_joint is not None:
                self.space.remove(mouse_joint)
                mouse_joint = None

            p = Vec2d(*event.pos)
            print(p)
            hit = self.space.point_query_nearest(p, 5, self.filter)
            print(hit)
            if hit is not None and hit.shape.body.body_type == pymunk.Body.DYNAMIC:
                # Use the closest point on the surface if the click is outside
                # of the shape.
                if hit.distance > 0:
                    nearest = hit.point
                else:
                    nearest = p
                print(mouse_body)
                # (0, 0) отвечает за положение фиолетовой точки mouse_joint относит. положения курсора
                mouse_joint = pymunk.PivotJoint(mouse_body, hit.shape.body, (0, 0),
                                                hit.shape.body.world_to_local(nearest))
                mouse_joint.max_force = 50000
                mouse_joint.error_bias = (1 - 0.15) ** 60  # Определяет максимальное кол-во ошибок за один шаг
                self.space.add(mouse_joint)
                print(mouse_joint)

        elif event.type == pygame.MOUSEBUTTONUP:
            if mouse_joint is not None:
                self.space.remove(mouse_joint)
                mouse_joint = None

        return mouse_joint


class Ball(pygame.sprite.Sprite):

    def add_ball(self, space, pos):
        body = pymunk.Body()
        body.position = Vec2d(*pos)
        shape = pymunk.Circle(body, 20)
        shape.mass = 1
        shape.friction = 0.7
        space.add(body, shape)
        return


if __name__ == 'main':
    print("This module is not for direct call!")
