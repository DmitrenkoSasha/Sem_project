import inspect
import math
import pygame
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
    shape = pymunk.Segment(body, (0, 60), (0, -60), 5)
    shape.mass = 1
    shape.friction = 0.7
    space.add(body, shape)
    return body


txts = {}

box_offset = 0, 0
b1 = add_lever(space, (550, 100), box_offset)
b2 = add_ball(space, (650, 0), box_offset)
c: pymunk.Constraint = pymunk.PinJoint(b1, b2, (0, 60), (-20, 0))
space.add(pymunk.PivotJoint(b2, space.static_body, (650, 0) + Vec2d(*box_offset)))
txts[box_offset] = inspect.getdoc(c)
space.add(c)



# TODO add one or two advanced constraints examples, such as a car or rope

mouse_joint = None
mouse_body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)



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
            if mouse_joint is not None:
                space.remove(mouse_joint)
                mouse_joint = None

    screen.fill(pygame.Color("white"))

    #screen.blit(screen, circle(screen, (0,110,0), (b1.position[0]-270,b1.position[1]-0), 100))

    mouse_pos = pygame.mouse.get_pos()


    mouse_body.position = mouse_pos

    space.step(1.0 / 60)

    space.debug_draw(draw_options)
    pygame.display.flip()

    clock.tick(60)
    pygame.display.set_caption(f"fps: {clock.get_fps()}")
