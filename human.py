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
scale = 1
font = pygame.font.SysFont("Arial", 16)
options = pymunk.pygame_util.DrawOptions(screen)
options.flags = pymunk.SpaceDebugDrawOptions.DRAW_SHAPES
collision_types = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21]

''' "head_1": 0,
    "body_1": 1,
    "right_arm_1": 2,
    "right_hand_1": 3,
    "left_arm_1": 4,
    "left_hand_1": 5,
    "right_leg_1": 6,
    "right_feet_1": 7,
    "left_leg_1": 8,
    "left_feet_1": 9,

    "head_2": 10,
    "body_2": 11,
    "right_arm_2": 12,
    "right_hand_2": 13,
    "left_arm_2": 14,
    "left_hand_2": 15,
    "right_leg_2": 16,
    "right_feet_2": 17,
    "left_leg_2": 18,
    "left_feet_2": 19'''

class Human:
    def __init__(self, space):
        self.space = space
        self.shapes = []
        self.points = 0

    def add_lever(self, pos, x1, x2, category, mask, collision_type):
        body = pymunk.Body()
        body.position = pos
        shape = pymunk.Segment(body, x1, x2, 6*scale)
        shape.mass = 1
        shape.friction = 50
        shape.color = pygame.Color('blue')
        shape.filter = pymunk.ShapeFilter(categories=category, mask=mask)
        shape.collision_type = collision_types[collision_type]
        self.shapes.append(shape)
        self.space.add(body, shape)
        return body

    def add_head(self, pos, x1, x2, category, mask, collision_type):
        body = pymunk.Body()
        body.position = pos
        shape = pymunk.Segment(body, x1, x2, 18*scale)
        shape.mass = 1
        shape.friction = 50
        shape.color = pygame.Color('blue')
        shape.filter = pymunk.ShapeFilter(categories=category, mask=mask)
        shape.collision_type = collision_types[collision_type]
        self.shapes.append(shape)
        self.space.add(body, shape)
        return body

    def create_Human(self, x, y, i):
        head = self.add_head((x, y), (0, -30 * scale), (0, -32 * scale), 1, 1021, i)
        telo = self.add_lever((x, y), (0, 30 * scale), (0, -30 * scale), 2, 682, i+1)
        c_head_body = pymunk.PivotJoint(head, telo, (x, y - 30 * scale))
        self.space.add(c_head_body)

        right_leg = self.add_lever((x, y), (0, 30 * scale), (20 * scale, 50 * scale), 256, 477, i+6)
        right_feet = self.add_lever((x, y), (20 * scale, 50 * scale), (20 * scale, 80 * scale), 512, 767, i+7)
        c_right_leg = pymunk.PivotJoint(right_leg, right_feet, (x + 20 * scale, y + 50 * scale))
        self.space.add(c_right_leg)

        left_leg = self.add_lever((x, y), (0, 30 * scale), (-20 * scale, 50 * scale), 64, 637, i+8)
        left_feet = self.add_lever((x, y), (-20 * scale, 50 * scale), (-20 * scale, 80 * scale), 128, 959, i+9)
        c_left_leg = pymunk.PivotJoint(left_leg, left_feet, (x - 20 * scale, y + 50 * scale))
        self.space.add(c_left_leg)

        c_body_right_leg = pymunk.PivotJoint(right_leg, telo, (x, y + 30 * scale))
        c_body_left_leg = pymunk.PivotJoint(left_leg, telo, (x, y + 30 * scale))
        spring_legs = pymunk.DampedSpring(left_feet, right_feet, (-20 * scale, 70 * scale), (20 * scale, 70 * scale),
                                          40 * scale, 500, 50)
        spring_legs_2 = pymunk.DampedSpring(left_leg, right_leg, (-20 * scale, 50 * scale),
                                            (20 * scale, 50 * scale), 50 * scale, 500, 50)
        spring_body_right_leg = pymunk.DampedSpring(telo, right_feet, (0, 20 * scale), (20 * scale, 70 * scale),
                                                    70 * scale, 500, 0.3)
        spring_body_left_leg = pymunk.DampedSpring(telo, left_feet, (0, 20 * scale), (-20 * scale, 70 * scale),
                                                   70 * scale, 500, 0.3)
        self.space.add(c_body_right_leg)
        self.space.add(c_body_left_leg)
        self.space.add(spring_legs)
        self.space.add(spring_legs_2)
        self.space.add(spring_body_right_leg)
        self.space.add(spring_body_left_leg)

        right_arm = self.add_lever((x, y), (0, -5 * scale), (15 * scale, -20 * scale), 16, 985, i+2)
        right_hand = self.add_lever((x, y), (15 * scale, -20 * scale), (40 * scale, -45 * scale), 32, 991, i+3)
        c_right_arm = pymunk.PivotJoint(right_arm, right_hand, (x + 15 * scale, y - 20 * scale))
        self.space.add(c_right_arm)

        left_arm = self.add_lever((x, y), (0, -5 * scale), (-15 * scale, -20 * scale), 4, 997, i+4)
        left_hand = self.add_lever((x, y), (-15 * scale, -20 * scale), (-40 * scale, -45 * scale), 8, 1019, i+5)
        c_left_arm = pymunk.PivotJoint(left_arm, left_hand, (x - 15 * scale, y - 20 * scale))
        self.space.add(c_left_arm)

        c_body_right_arm = pymunk.PivotJoint(right_arm, telo, (x, y - 5 * scale))
        c_body_left_arm = pymunk.PivotJoint(left_arm, telo, (x, y - 5 * scale))
        spring_body_right_arm = pymunk.DampedSpring(telo, right_arm, (0, 20 * scale), (20 * scale, -20 * scale),
                                                    40 * scale, 200, 0.3)
        spring_body_left_arm = pymunk.DampedSpring(telo, left_arm, (0, 20 * scale), (-20 * scale, -20 * scale),
                                                   40 * scale, 200, 0.3)
        self.space.add(c_body_right_arm)
        self.space.add(c_body_left_arm)
        self.space.add(spring_body_right_arm)
        self.space.add(spring_body_left_arm)

        self.complect = ([head, telo, right_arm, left_arm,
                          right_leg, left_leg])
        self.points = 100

    def check_event_human(self, up, left, down, right):
        """Эта функция должна вызываться в главном цикле модуля тренажёрный зал или главного модуля"""
        if pygame.key.get_pressed()[right]:
            for part in self.complect:
                part.velocity += (30, 0)
        if pygame.key.get_pressed()[left]:
            for part in self.complect:
                part.velocity += (-30, 0)
        if pygame.key.get_pressed()[up]:
            for part in self.complect:
                part.velocity += (0, -30)
        if pygame.key.get_pressed()[down]:
            for part in self.complect:
                part.velocity += (0, 30)
