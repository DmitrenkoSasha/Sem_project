import pygame
import pymunk
import pymunk.pygame_util
from pymunk.vec2d import Vec2d

screen = pygame.display.set_mode((1000, 600))
space = pymunk.Space()


def draw_collision(arbiter, data):
    for c in arbiter.contact_point_set.points:
        r = max(3, abs(c.distance * 5))
        r = int(r)

        p = pymunk.pygame_util.to_pygame(c.point_a, data["surface"])
        pygame.draw.circle(data["surface"], pygame.Color("black"), p, r, 1)
        

def create_ball(space):
    body = pymunk.Body(1, 10)
    body.position = (500, 300)
    radius = 25
    shape = pymunk.Circle(body, radius, (0,0))
    space.add(body, shape)  # Объединили душу и тело
    return shape

def add_ball(space, pos):
    body = pymunk.Body()
    body.position = Vec2d(*pos)
    shape = pymunk.Circle(body, 15)
    shape.mass = 1
    shape.friction = 0.7
    shape.filter = pymunk.ShapeFilter(group=1)
    shape.color = (142, 68, 173, 255)
    space.add(body, shape)
    return body

def add_lever(space, pos, x1, x2):
    body = pymunk.Body()
    body.position = pos
    shape = pymunk.Segment(body, x1, x2, 4)
    shape.mass = 1
    shape.friction = 0.7
    shape.color = (142, 68, 173, 255)
    shape.filter = pymunk.ShapeFilter(group=1)
    space.add(body, shape)
    return body


def create_Human():
    global telo, head  # вынужденная приспособа
    telo = add_lever(space, (200, 200), (0, 30), (0, -30))
    head = add_ball(space, (200, 180))
    c_head_body = pymunk.PivotJoint(head, telo, (200, 180))
    space.add(c_head_body)

    right_leg_1 = add_lever(space, (200, 200), (0, 30), (30, 60))
    right_leg_2 = add_lever(space, (200, 200), (30, 60), (30, 90))
    c_right_leg = pymunk.PivotJoint(right_leg_1, right_leg_2, (230, 260))
    space.add(c_right_leg)

    left_leg_1 = add_lever(space, (200, 200), (0, 30), (-30, 60))
    left_leg_2 = add_lever(space, (200, 200), (-30, 60), (-30, 90))
    c_left_leg = pymunk.PivotJoint(left_leg_1, left_leg_2, (170, 260))
    space.add(c_left_leg)

    c_body_right_leg = pymunk.PivotJoint(right_leg_1, telo, (200, 230))
    c_body_left_leg = pymunk.PivotJoint(left_leg_1, telo, (200, 230))
    space.add(c_body_right_leg)
    space.add(c_body_left_leg)

    right_arm_1 = add_lever(space, (200, 200), (0, -5), (30, -30))
    right_arm_2 = add_lever(space, (200, 200), (30, -30), (50, -30))
    c_right_arm = pymunk.PivotJoint(right_arm_1, right_arm_2, (230, 170))
    space.add(c_right_arm)

    left_arm_1 = add_lever(space, (200, 200), (0, -5), (-30, -30))
    left_arm_2 = add_lever(space, (200, 200), (-30, -30), (-50, -30))
    c_left_arm = pymunk.PivotJoint(left_arm_1, left_arm_2, (170, 170))
    space.add(c_left_arm)

    c_body_right_arm = pymunk.PivotJoint(right_arm_1, telo, (200, 195))
    c_body_left_arm = pymunk.PivotJoint(left_arm_1, telo, (200, 195))
    space.add(c_body_right_arm)
    space.add(c_body_left_arm)


    player_body = pymunk.Body(20, 200)
    player_body.position = 300, 100
    player_shape = pymunk.Segment(player_body, (-50, 0), (50, 0), 8)
    player_shape.color = pygame.Color("red")
    player_shape.elasticity = 50.0
    player_shape.collision_type = 2
    space.add(player_body, player_shape)

def check_event_human(event):
    """Эта функция должна вызываться в главном цикле модуля тренажёрный зал или главного модуля"""
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_RIGHT:
            print(1)
            telo.velocity += (400, 0)
            head.velocity += (400, 0)
        if event.key == pygame.K_LEFT:
            print(2)
            telo.velocity += (-400, 0)
            head.velocity += (-400, 0)
        if event.key == pygame.K_UP:
            telo.velocity += (0, -400)
            head.velocity += (0, -400)
        if event.key == pygame.K_DOWN:
            telo.velocity += (0, 400)
            head.velocity += (0, 400)

        if event.key == pygame.K_r:
            create_ball(space)



