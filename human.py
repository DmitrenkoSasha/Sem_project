import pygame
import pymunk
import pymunk.pygame_util
from pymunk.vec2d import Vec2d

class Human():
    def __init__(self, space):
        self.space = space


    '''def draw_collision(arbiter, data):
        for c in arbiter.contact_point_set.points:
            r = max(3, abs(c.distance * 5))
            r = int(r)

            p = pymunk.pygame_util.to_pygame(c.point_a, data["surface"])
            pygame.draw.circle(data["surface"], pygame.Color("black"), p, r, 1)'''


    def create_ball(self):
        body = pymunk.Body(1, 10)
        body.position = (500, 300)
        radius = 25
        shape = pymunk.Circle(body, radius)
        self.space.add(body, shape)  # Объединили душу и тело
        return shape

    def add_ball(self, pos, category, mask):
        body = pymunk.Body()
        body.position = Vec2d(*pos)
        shape = pymunk.Circle(body, 15)
        shape.mass = 1
        shape.friction = 0.7
        shape.filter = pymunk.ShapeFilter(categories = category, mask = mask)
        shape.color = pygame.Color('red')
        self.space.add(body, shape)
        return body

    def add_lever(self, pos, x1, x2, category, mask):
        body = pymunk.Body()
        body.position = pos
        shape = pymunk.Segment(body, x1, x2, 6)
        shape.mass = 1
        shape.friction = 50
        shape.color = pygame.Color('blue')
        shape.filter = pymunk.ShapeFilter(categories=category, mask=mask)
        self.space.add(body, shape)
        return body

    def add_lever_2(self, pos, x1, x2, category, mask):
        body = pymunk.Body()
        body.position = pos
        shape = pymunk.Segment(body, x1, x2, 8)
        shape.mass = 1
        shape.friction = 0.7
        shape.color = (142, 68, 173, 255)
        shape.color = pygame.Color('blue')
        shape.filter = pymunk.ShapeFilter(categories=category, mask=mask)
        self.space.add(body, shape)
        return body


    def create_Human(self):
        global complect  # вынужденная приспособа
        telo = self.add_lever_2((200, 200), (0, 30), (0, -30), 2, 682)
        head = self.add_ball((200, 170), 1, 1021)
        c_head_body = pymunk.PivotJoint(head, telo, (200, 170))
        c_head_body.color = pygame.Color('white')
        self.space.add(c_head_body)

        right_leg_1 = self.add_lever((200, 200), (0, 30), (20, 50), 256, 477)
        right_leg_2 = self.add_lever((200, 200), (20, 50), (20, 80), 512, 767)
        c_right_leg = pymunk.PivotJoint(right_leg_1, right_leg_2, (220, 250))
        c_right_leg.color = pygame.Color('red')
        self.space.add(c_right_leg)

        left_leg_1 = self.add_lever((200, 200), (0, 30), (-20, 50), 64, 637)
        left_leg_2 = self.add_lever((200, 200), (-20, 50), (-20, 80), 128, 959)
        c_left_leg = pymunk.PivotJoint(left_leg_1, left_leg_2, (180, 250))
        self.space.add(c_left_leg)

        c_body_right_leg = pymunk.PivotJoint(right_leg_1, telo, (200, 230))
        c_body_left_leg = pymunk.PivotJoint(left_leg_1, telo, (200, 230))
        self.space.add(c_body_right_leg)
        self.space.add(c_body_left_leg)

        right_arm_1 = self.add_lever((200, 200), (0, -5), (15, -20), 16, 985)
        right_arm_2 = self.add_lever((200, 200), (15, -20), (40, -45), 32, 991)
        c_right_arm = pymunk.PivotJoint(right_arm_1, right_arm_2, (215, 180))
        self.space.add(c_right_arm)

        left_arm_1 = self.add_lever((200, 200), (0, -5), (-15, -20), 4, 997)
        left_arm_2 = self.add_lever((200, 200), (-15, -20), (-40, -45), 8, 1019)
        c_left_arm = pymunk.PivotJoint(left_arm_1, left_arm_2, (185, 180))
        self.space.add(c_left_arm)

        c_body_right_arm = pymunk.PivotJoint(right_arm_1, telo, (200, 195))
        c_body_left_arm = pymunk.PivotJoint(left_arm_1, telo, (200, 195))
        self.space.add(c_body_right_arm)
        self.space.add(c_body_left_arm)

        complect = [head, telo, right_arm_1, left_arm_1,
                    right_leg_1, left_leg_1]

    def check_event_human(self, event):
        """Эта функция должна вызываться в главном цикле модуля тренажёрный зал или главного модуля"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                for part in complect:
                    part.velocity += (400, 0)
            if event.key == pygame.K_LEFT:
                for part in complect:
                    part.velocity += (-400, 0)
            if event.key == pygame.K_UP:
                for part in complect:
                    part.velocity += (0, -400)
            if event.key == pygame.K_DOWN:
                for part in complect:
                    part.velocity += (0, 400)
            if event.key == pygame.K_r:
                self.create_ball()
            if event.key == pygame.K_h:
                self.create_Human()


