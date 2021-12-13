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
        #self.vs = [(-30, 275), (30, 275), (30, 105), (-30, 105)]
        self.body = self.add_lever(space, (x, y))
        #self.shape = pymunk.Poly(self.body, self.vs)

    def add_lever(self, space, pos):
        mass = 100
        vs = [(-28, 265), (28, 265), (28, 63), (-28, 64), (0, 55), (0, 270)]
        moment = pymunk.moment_for_poly(mass, vs)
        body = pymunk.Body(mass, moment)
        self.shape = pymunk.Poly(body, vs)
        body.position = pos

        self.shape.friction = 1
        rotation_center_body = pymunk.Body(body_type=pymunk.Body.STATIC)
        rotation_center_body.position = body.position
        rotation_center_joint = pymunk.PinJoint(body, rotation_center_body, (0, 0), (0, 0))

        space.add(rotation_center_joint)

        space.add(body, self.shape)
        return body

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
            vrtcs.rotated(self.shape.body.angle) + self.shape.body.position
            for vrtcs in self.shape.get_vertices()]

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
        offset2 = (Vec2d(*vec0 - self.shape.body.position) + Vec2d(*vec2 - self.shape.body.position)) / 2

        #  Вектор к центру картинки
        p = vec_rot - Vec2d(*offset) + offset2

        return rotated_img, p, ps


    def update(self, *args):
        pass


    def check_event_pear(self, event, mouse_joint, mouse_body):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if mouse_joint is not None:
                self.space.remove(mouse_joint)
                mouse_joint = None

            p = Vec2d(*event.pos)
            hit = self.space.point_query_nearest(p, 5, pymunk.ShapeFilter())
            if hit is not None and hit.shape.body.body_type == pymunk.Body.DYNAMIC:
                shape = hit.shape
                # Use the closest point on the surface if the click is outside
                # of the shape.
                if hit.distance > 0:
                    nearest = hit.point
                else:
                    nearest = p
                mouse_joint = pymunk.PivotJoint(
                    mouse_body, shape.body, (0, 0), shape.body.world_to_local(nearest))
                mouse_joint.max_force = 50000
                mouse_joint.error_bias = (1 - 0.15) ** 60
                self.space.add(mouse_joint)

        elif event.type == pygame.MOUSEBUTTONUP:
            self.body.apply_impulse_at_local_point((2000, 0))
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
