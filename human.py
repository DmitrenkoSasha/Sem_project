import pygame
import pymunk
import pymunk.pygame_util
from pymunk.vec2d import Vec2d
from pygame.locals import *

pygame.init()
screen = pygame.display.set_mode((1000, 600))
space = pymunk.Space()
space.gravity = (0, 50)
clock = pygame.time.Clock()
scale = 2
font = pygame.font.SysFont("Arial", 16)
options = pymunk.pygame_util.DrawOptions(screen)
options.flags = pymunk.SpaceDebugDrawOptions.DRAW_SHAPES
collision_types = {
    "head": 1,
    "body": 2,
    "arm": 3,
    "leg": 4,
    "wall": 5
}

class Human:
    def __init__(self, space):
        self.space = space
        self.complect = []
        self.points = 0

    def create_ball(self, x, y, radius):
        body = pymunk.Body(1, 10)
        body.position = (x, y)
        shape = pymunk.Circle(body, radius)
        self.space.add(body, shape)  # Объединили душу и тело
        return shape

    def add_ball(self, pos, category, mask):
        body = pymunk.Body()
        body.position = Vec2d(*pos)
        shape = pymunk.Circle(body, 15*scale)
        shape.mass = 1
        shape.friction = 0.7
        shape.filter = pymunk.ShapeFilter(categories=category, mask=mask)
        shape.color = pygame.Color('red')
        shape.collision_type = collision_types["head"]
        self.space.add(body, shape)
        return body

    def add_lever(self, pos, x1, x2, category, mask):
        body = pymunk.Body()
        body.position = pos
        shape = pymunk.Segment(body, x1, x2, 6*scale)
        shape.mass = 1
        shape.friction = 50
        shape.color = pygame.Color('blue')
        shape.filter = pymunk.ShapeFilter(categories=category, mask=mask)
        shape.collision_type = collision_types["leg"]
        self.space.add(body, shape)
        return body

    def add_lever_2(self, pos, x1, x2, category, mask):
        body = pymunk.Body()
        body.position = pos
        shape = pymunk.Segment(body, x1, x2, 8*scale)
        shape.mass = 1
        shape.friction = 0.7
        shape.color = (142, 68, 173, 255)
        shape.color = pygame.Color('blue')
        shape.filter = pymunk.ShapeFilter(categories=category, mask=mask)
        shape.collision_type = collision_types["body"]
        self.space.add(body, shape)
        return body

    def create_Human(self, x, y):
        telo = self.add_lever_2((x, y), (0, 30 * scale), (0, -30 * scale), 2, 682)
        head = self.add_ball((x, y - 30 * scale), 1, 1021)
        c_head_body = pymunk.PivotJoint(head, telo, (x, y - 30 * scale))
        c_head_body.color = pygame.Color('white')
        self.space.add(c_head_body)

        right_leg_1 = self.add_lever((x, y), (0, 30 * scale), (20 * scale, 50 * scale), 256, 477)
        right_leg_2 = self.add_lever((x, y), (20 * scale, 50 * scale), (20 * scale, 80 * scale), 512, 767)
        c_right_leg = pymunk.PivotJoint(right_leg_1, right_leg_2, (x + 20 * scale, y + 50 * scale))
        c_right_leg.color = pygame.Color('red')
        self.space.add(c_right_leg)

        left_leg_1 = self.add_lever((x, y), (0, 30 * scale), (-20 * scale, 50 * scale), 64, 637)
        left_leg_2 = self.add_lever((x, y), (-20 * scale, 50 * scale), (-20 * scale, 80 * scale), 128, 959)
        c_left_leg = pymunk.PivotJoint(left_leg_1, left_leg_2, (x - 20 * scale, y + 50 * scale))
        self.space.add(c_left_leg)

        c_body_right_leg = pymunk.PivotJoint(right_leg_1, telo, (x, y + 30 * scale))
        c_body_left_leg = pymunk.PivotJoint(left_leg_1, telo, (x, y + 30 * scale))
        spring_legs = pymunk.DampedSpring(left_leg_2, right_leg_2, (-20 * scale, 70 * scale), (20 * scale, 70 * scale),
                                          40 * scale, 2000, 50)
        spring_legs_2 = pymunk.DampedSpring(left_leg_1, right_leg_1, (-20 * scale, 50 * scale),
                                            (20 * scale, 50 * scale), 50 * scale, 2000, 50)
        spring_body_right_leg = pymunk.DampedSpring(telo, right_leg_2, (0, 20 * scale), (20 * scale, 70 * scale),
                                                    70 * scale, 500, 0.3)
        spring_body_left_leg = pymunk.DampedSpring(telo, left_leg_2, (0, 20 * scale), (-20 * scale, 70 * scale),
                                                   70 * scale, 500, 0.3)
        self.space.add(c_body_right_leg)
        self.space.add(c_body_left_leg)
        self.space.add(spring_legs)
        self.space.add(spring_legs_2)
        self.space.add(spring_body_right_leg)
        self.space.add(spring_body_left_leg)

        right_arm_1 = self.add_lever((x, y), (0, -5 * scale), (15 * scale, -20 * scale), 16, 985)
        right_arm_2 = self.add_lever((x, y), (15 * scale, -20 * scale), (40 * scale, -45 * scale), 32, 991)
        c_right_arm = pymunk.PivotJoint(right_arm_1, right_arm_2, (x + 15 * scale, y - 20 * scale))
        self.space.add(c_right_arm)

        left_arm_1 = self.add_lever((x, y), (0, -5 * scale), (-15 * scale, -20 * scale), 4, 997)
        left_arm_2 = self.add_lever((x, y), (-15 * scale, -20 * scale), (-40 * scale, -45 * scale), 8, 1019)
        c_left_arm = pymunk.PivotJoint(left_arm_1, left_arm_2, (x - 15 * scale, y - 20 * scale))
        self.space.add(c_left_arm)

        c_body_right_arm = pymunk.PivotJoint(right_arm_1, telo, (x, y - 5 * scale))
        c_body_left_arm = pymunk.PivotJoint(left_arm_1, telo, (x, y - 5 * scale))
        spring_body_right_arm = pymunk.DampedSpring(telo, right_arm_1, (0, 20 * scale), (20 * scale, -20 * scale),
                                                    40 * scale, 200, 0.3)
        spring_body_left_arm = pymunk.DampedSpring(telo, left_arm_1, (0, 20 * scale), (-20 * scale, -20 * scale),
                                                   40 * scale, 200, 0.3)
        self.space.add(c_body_right_arm)
        self.space.add(c_body_left_arm)
        self.space.add(spring_body_right_arm)
        self.space.add(spring_body_left_arm)

        self.complect = ([head, telo, right_arm_1, left_arm_1,
                             right_leg_1, left_leg_1])

    def check_event_human_1(self):
        """Эта функция должна вызываться в главном цикле модуля тренажёрный зал или главного модуля"""
        if pygame.key.get_pressed()[K_RIGHT]:
            for part in self.complect:
                part.velocity += (30, 0)
        if pygame.key.get_pressed()[K_LEFT]:
            for part in self.complect:
                part.velocity += (-30, 0)
        if pygame.key.get_pressed()[K_UP]:
            for part in self.complect:
                part.velocity += (0, -30)
        if pygame.key.get_pressed()[K_DOWN]:
            for part in self.complect:
                part.velocity += (0, 30)


    def check_event_human_2(self):
        """Эта функция должна вызываться в главном цикле модуля тренажёрный зал или главного модуля"""
        if pygame.key.get_pressed()[K_d]:
            for part in self.complect:
                part.velocity += (30, 0)
        if pygame.key.get_pressed()[K_a]:
            for part in self.complect:
                part.velocity += (-30, 0)
        if pygame.key.get_pressed()[K_w]:
            for part in self.complect:
                part.velocity += (0, -30)
        if pygame.key.get_pressed()[K_s]:
            for part in self.complect:
                part.velocity += (0, 30)