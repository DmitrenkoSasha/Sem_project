import pygame
import pymunk
import math
from pymunk.vec2d import Vec2d


#space = pymunk.Space()
#space.gravity = (0.0, 900.0)

print(1)  # Проверка на то, что Тренажёрный зал выполняет всё, что написано в этом модуле

class Pear(pygame.sprite.Sprite):
    def __init__(self, space, x, filename):
        """Боксёрская груша, пользователь будет ставить её представителей, куда ему захочется,
         и возможно, что будут разные картинки.
         filename: название файла-картинки груши"""
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(filename).convert_alpha()  # Графическое представление спрайта
        self.rect = self.image.get_rect(center = (x, 200))  # Положение и размер спрайта
        self.space = space
        self.box_offset = 0, 0
        self.b1 = self.add_lever(space, (550, 100))
        #self.b2 = self.add_ball(space, (650, 0))
        #c: pymunk.Constraint = pymunk.PinJoint(self.b1, self.b2, (0, 60), (-20, 0))
        #space.add(pymunk.PivotJoint(self.b2, space.static_body, (650, 0) + Vec2d(
           # *self.box_offset)))  # Связывает точку вращения груши и шарик, к которому груша привешена
        #space.add(c)
        self.logo_img = pygame.image.load("груша.png")

    def add_ball(self, space, pos):
        body = pymunk.Body()
        body.position = Vec2d(*pos) + self.box_offset
        shape = pymunk.Circle(body, 20)
        shape.mass = 1
        shape.friction = 0.7
        space.add(body, shape)
        return body

    def add_lever(self, space, pos):
        mass = 100
        vs = [(-30, 270), (30, 270), (30, 0), (-30, 0)]

        moment = pymunk.moment_for_poly(mass, vs)
        body = pymunk.Body(mass, moment)
        body.position = pos + Vec2d(*self.box_offset)
        self.shape = pymunk.Poly(body, vs)
        self.shape.friction = 1
        rotation_center_body = pymunk.Body(body_type=pymunk.Body.STATIC)
        rotation_center_body.position = body.position
        rotation_center_joint = pymunk.PinJoint(body, rotation_center_body, (0, 0), (0, 0))

        space.add(rotation_center_joint)

        space.add(body, self.shape)
        #logos.append(shape)
        return body

    def work_with_logo(self):
        p = self.shape.body.position  # Остаётся постоянным 650,200
        p = Vec2d(p.x, p.y)

        # we need to rotate 180 degrees because of the y coordinate flip
        angle_degrees = -math.degrees(self.shape.body.angle)
        rotated_logo_img = pygame.transform.rotate(self.image, angle_degrees)

        # debug draw
        ps = [
            p.rotated(self.shape.body.angle) + self.shape.body.position
            for p in self.shape.get_vertices()]

        ps = [(round(p.x), round(p.y)) for p in ps]
        ps += [ps[0]]
        #pygame.draw.lines(screen, pygame.Color("red"), False, ps, 1)  В главом цикле тренажёрного зала

        offset_x = rotated_logo_img.get_rect().size[0] / 2
        offset_y = rotated_logo_img.get_rect().size[1] / 2
        offset = Vec2d(offset_x, offset_y)
        offset2 = (Vec2d(*ps[1] - self.shape.body.position) + Vec2d(*ps[3] - self.shape.body.position)) / 2
        p = p - Vec2d(*offset) + offset2
        return rotated_logo_img, p, ps
        #screen.blit(rotated_logo_img, (round(p.x), round(p.y)))    В главом цикле тренажёрного зала

    def update(self, *args):
        pass


    def check_event_pear(self, event):
        mouse_joint = None
        mouse_body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)

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
            self.b1.apply_impulse_at_local_point((2000, 0))
            if mouse_joint is not None:
                self.space.remove(mouse_joint)
                mouse_joint = None




mouse_joint = None
mouse_body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)


#pymunk.lib.cpBodyApplyForceAtWorldPoint(b1, [20, 20], [550, 100])


    #screen.blit(screen, circle(screen, (0,110,0), (b1.position[0]-270,b1.position[1]-0), 100))
'''
    mouse_pos = pygame.mouse.get_pos()


    mouse_body.position = mouse_pos

    space.step(1.0 / 60)

    space.debug_draw(draw_options)
    pygame.display.flip() # Обновляет весь экран

    clock.tick(60)
    pygame.display.set_caption(f"fps: {clock.get_fps()}")'''

if __name__ == 'main':
    print("This module is not for direct call!")
