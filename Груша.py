import pygame
import pymunk
from pymunk.vec2d import Vec2d

#space = pymunk.Space()
#space.gravity = (0.0, 900.0)
'''import inspect
import math

from pygame.draw import circle
import pymunk
import pymunk.pygame_util
from pymunk.vec2d import Vec2d


pygame.init()
screen = pygame.display.set_mode((1200, 600))
clock = pygame.time.Clock()
font = pygame.font.Font(None, 24)

space = pymunk.Space()
space.gravity = (0.0, 900.0)
draw_options = pymunk.pygame_util.DrawOptions(screen)

# containers
box_size = 200
w = screen.get_width()
h = screen.get_height()
pear = pygame.image.load('боксёрская груша.jpg')
pear_rect = pear.get_rect(bottomright=(400, 300))
screen.blit(pear, pear_rect)

pygame.display.update()'''
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
        self.b2 = self.add_ball(space, (650, 0))
        c: pymunk.Constraint = pymunk.PinJoint(self.b1, self.b2, (0, 60), (-20, 0))
        space.add(pymunk.PivotJoint(self.b2, space.static_body, (650, 0) + Vec2d(
            *self.box_offset)))  # Связывает точку вращения груши и шарик, к которому груша привешена
        space.add(c)

    def add_ball(self, space, pos):
        body = pymunk.Body()
        body.position = Vec2d(*pos) + self.box_offset
        shape = pymunk.Circle(body, 20)
        shape.mass = 1
        shape.friction = 0.7
        space.add(body, shape)
        return body

    def add_lever(self, space, pos):
        body = pymunk.Body()
        body.position = pos + Vec2d(*self.box_offset) + (0, -20)
        shape = pymunk.Segment(body, (0, 60), (0, -60), 50)
        shape.mass = 1
        shape.friction = 0.7
        space.add(body, shape)
        return body

    def update(self, *args):
        pass

    def smth(self):
        '''b1 = self.add_lever(space, (550, 100))
        b2 = self.add_ball(space, (650, 0))
        c: pymunk.Constraint = pymunk.PinJoint(b1, b2, (0, 60), (-20, 0))
        space.add(pymunk.PivotJoint(b2, space.static_body, (650, 0) + Vec2d(*self.box_offset)))  # Связывает точку вращения груши и шарик, к которому груша привешена
        #txts[box_offset] = inspect.getdoc(c)
        space.add(c)'''

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
'''
def add_ball(space, pos, box_offset):
    body = pymunk.Body()
    body.position = Vec2d(*pos) + box_offset
    shape = pymunk.Circle(body, 20)
    shape.mass = 1
    shape.friction = 0.7
    space.add(body, shape)
    return body


def add_lever(space, pos, box_offset):
    body = pymunk.Body()
    body.position = pos + Vec2d(*box_offset) + (0, -20)
    shape = pymunk.Segment(body, (0, 60), (0, -60), 50)
    shape.mass = 1
    shape.friction = 0.7
    space.add(body, shape)
    return body


#txts = {}
'''



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
