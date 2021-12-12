import math
import pygame
import pymunk
import pymunk.pygame_util
from pymunk.vec2d import Vec2d
from pygame.math import Vector2
from typing import List


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


pygame.display.update()

logo_img = pygame.image.load("груша.png")
logos: List[pymunk.Shape] = []

def add_ball(space, pos, box_offset):
    body = pymunk.Body()
    body.position = Vec2d(*pos) + box_offset
    shape = pymunk.Circle(body, 20)
    shape.mass = 1
    shape.friction = 0.7
    space.add(body, shape)
    return body

def add_lever(space, pos, box_offset):
    mass = 100
    vs = [(-30, 270), (30, 270), (30, 0), (-30, 0)]
    moment = pymunk.moment_for_poly(mass, vs)

    body = pymunk.Body(mass, moment)
    body.position = pos + Vec2d(*box_offset)
    shape = pymunk.Poly(body, vs)
    shape.friction = 1

    rotation_center_body = pymunk.Body(body_type=pymunk.Body.STATIC)
    rotation_center_body.position = body.position
    rotation_center_joint = pymunk.PinJoint(body, rotation_center_body, (0, 0), (0, 0))


    space.add(rotation_center_joint)

    space.add(body, shape)
    logos.append(shape)
    return body

'''def add_new(space):

    x = random.randint(20, 400)
    y = 500
    angle = math.pi
    # vs = [(-23, 26), (23, 26), (0, -26)]
    vs = [(30, -120), (-30, -120), (-30, 100), (30, 100)]
    mass = 10
    moment = pymunk.moment_for_poly(mass, vs)
    body = pymunk.Body(mass, moment)
    shape = pymunk.Poly(body, vs)
    shape.friction = 0.5
    body.position = x, y
    body.angle = angle

    space.add(body, shape)
    logos.append(shape)'''


box_offset = 0, 0
b1 = add_lever(space, (650, 200), box_offset)
#b2 = add_ball(space, (650, 30), box_offset)
#c: pymunk.Constraint = pymunk.PinJoint(b1, b2, (0, 0))  # Держит две точки на постоянном рассотянии

#space.add(pymunk.PivotJoint(b2, space.static_body, (650, 30) + Vec2d(*box_offset)))  # Связывает точку вращения груши и шарик, к которому груша привешена
#space.add(c)


mouse_joint = None
mouse_body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)


#pymunk.lib.cpBodyApplyForceAtWorldPoint(b1, [20, 20], [550, 100])

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if mouse_joint is not None:
                space.remove(mouse_joint)
                mouse_joint = None
            p = Vec2d(*event.pos)
            hit = space.point_query_nearest(p, 5, pymunk.ShapeFilter())
            if hit is not None and hit.shape.body.body_type == pymunk.Body.DYNAMIC:
                shape = hit.shape
                # Use the closest point on the surface if the click is outside
                # of the shape.
                if hit.distance > 0:
                    nearest = hit.point
                else:
                    nearest = p
                mouse_joint = pymunk.PivotJoint(
                    mouse_body, shape.body, (0, 0), shape.body.world_to_local(nearest)
                )
                mouse_joint.max_force = 50000
                mouse_joint.error_bias = (1 - 0.15) ** 60
                space.add(mouse_joint)

        elif event.type == pygame.MOUSEBUTTONUP:
            b1.apply_impulse_at_local_point((2000, 0))
            if mouse_joint is not None:
                space.remove(mouse_joint)
                mouse_joint = None

    screen.fill(pygame.Color("white"))

    '''# Rotate the image.
    self.image = pg.transform.rotozoom(self.orig_image, -self.angle, 1)
    # Rotate the offset vector.
    offset_rotated = self.offset.rotate(self.angle)
    # Create a new rect with the center of the sprite + the offset.
    self.rect = self.image.get_rect(center=self.pos + offset_rotated)'''

    for logo_shape in logos:


        p = logo_shape.body.position  # Остаётся постоянным 650,200
        p = Vec2d(p.x, p.y)


        # we need to rotate 180 degrees because of the y coordinate flip
        angle_degrees = -math.degrees(logo_shape.body.angle)
        rotated_logo_img = pygame.transform.rotate(logo_img, angle_degrees)

        # debug draw
        ps = [
            p.rotated(logo_shape.body.angle) + logo_shape.body.position
            for p in logo_shape.get_vertices()]

        ps = [(round(p.x), round(p.y)) for p in ps]
        ps += [ps[0]]
        pygame.draw.lines(screen, pygame.Color("red"), False, ps, 1)
        print(ps[1])

        offset_x = rotated_logo_img.get_rect().size[0]/2
        offset_y = rotated_logo_img.get_rect().size[1]/2
        offset = Vec2d(offset_x, offset_y)
        offset2 = (Vec2d(*ps[1] - logo_shape.body.position)+Vec2d(*ps[3] - logo_shape.body.position))/2
        p = p - Vec2d(*offset) + offset2
        screen.blit(rotated_logo_img, (round(p.x), round(p.y)))


    mouse_pos = pygame.mouse.get_pos()
    mouse_body.position = mouse_pos
    space.step(1.0 / 60)
    space.debug_draw(draw_options)
    pygame.display.flip()

    clock.tick(60)
    pygame.display.set_caption(f"fps: {clock.get_fps()}")