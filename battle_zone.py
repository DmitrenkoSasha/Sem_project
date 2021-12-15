import pygame
from pymunk.pygame_util import *
from typing import List
import random
import pymunk
import pymunk.pygame_util
from pymunk.vec2d import Vec2d
from pygame.locals import *
from textures import *

def main_battle(number_of_room):
    alive = True
    WHITE = (255, 255, 255)

    pygame.init()
    W = 1000
    H = 700
    screen = pygame.display.set_mode((W, H))
    space = pymunk.Space()
    scale = 1.2
    space.gravity = (0, 100)  # По горизонтали 0, по вертикали 500 в вымышленных единицах
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 30)
    draw_options = pymunk.pygame_util.DrawOptions(screen)
    draw_options.flags = pymunk.SpaceDebugDrawOptions.DRAW_SHAPES
    balls = []
    handlers = []
    balls_to_remove = []
    head_list = []
    human_1_shapes = []
    human_2_shapes = []

    pygame.mixer.music.load('фон.wav')
    pygame.mixer.music.set_volume(0.1)
    pygame.mixer.music.play()
    sound2 = pygame.mixer.Sound('удар по груше.wav')


    collision_types = {
        "head_1": 1,
        "body_1": 2,
        "right_arm_1": 3,
        "right_hand_1": 4,
        "left_arm_1": 5,
        "left_hand_1": 6,
        "right_leg_1": 7,
        "right_feet_1": 8,
        "left_leg_1": 9,
        "left_feet_1": 10,

        "head_2": 11,
        "body_2": 12,
        "right_arm_2": 13,
        "right_hand_2": 14,
        "left_arm_2": 15,
        "left_hand_2": 16,
        "right_leg_2": 17,
        "right_feet_2": 18,
        "left_leg_2": 19,
        "left_feet_2": 20,
    }


    def add_ball(pos, category, mask, collision_type):
        body = pymunk.Body()
        body.position = Vec2d(*pos)
        shape = pymunk.Circle(body, 15 * scale)
        shape.mass = 1
        shape.friction = 0.7
        shape.filter = pymunk.ShapeFilter(categories=category, mask=mask)
        shape.color = pygame.Color('red')
        shape.collision_type = collision_types[collision_type]
        head_list.append(shape)
        space.add(body, shape)
        return body


    def add_lever(pos, x1, x2, category, mask, collision_type):
        body = pymunk.Body()
        body.position = pos
        shape = pymunk.Segment(body, x1, x2, 6 * scale)
        shape.mass = 1
        shape.friction = 50
        shape.color = pygame.Color('blue')
        shape.filter = pymunk.ShapeFilter(categories=category, mask=mask)
        shape.collision_type = collision_types[collision_type]
        space.add(body, shape)
        human_1_shapes.append(shape)
        return body

    def add_lever_2(pos, x1, x2, category, mask, collision_type):
        body = pymunk.Body()
        body.position = pos
        shape = pymunk.Segment(body, x1, x2, 8 * scale)
        shape.mass = 1
        shape.friction = 0.7
        shape.color = (142, 68, 173, 255)
        shape.color = pygame.Color('blue')
        shape.filter = pymunk.ShapeFilter(categories=category, mask=mask)
        shape.collision_type = collision_types[collision_type]
        human_2_shapes.append(shape)
        space.add(body, shape)
        return body

    def create_Human_1(x, y):
        global complect_1, points_1
        telo_1 = add_lever((x, y), (0, 30 * scale), (0, -30 * scale), 2, 682, 'body_1')
        head_1 = add_ball((x, y - 30 * scale), 1, 1021, 'head_1')
        c_head_body = pymunk.PivotJoint(head_1, telo_1, (x, y - 30 * scale))
        c_head_body.color = pygame.Color('white')
        space.add(c_head_body)

        right_leg_1 = add_lever((x, y), (0, 30 * scale), (20 * scale, 50 * scale), 256, 477, 'right_leg_1')
        right_feet_1 = add_lever((x, y), (20 * scale, 50 * scale), (20 * scale, 80 * scale), 512, 767, 'right_feet_1')
        c_right_leg = pymunk.PivotJoint(right_leg_1, right_feet_1, (x + 20 * scale, y + 50 * scale))
        c_right_leg.color = pygame.Color('red')
        space.add(c_right_leg)

        left_leg_1 = add_lever((x, y), (0, 30 * scale), (-20 * scale, 50 * scale), 64, 637, 'left_leg_1')
        left_feet_1 = add_lever((x, y), (-20 * scale, 50 * scale), (-20 * scale, 80 * scale), 128, 959, 'left_feet_1')
        c_left_leg = pymunk.PivotJoint(left_leg_1, left_feet_1, (x - 20 * scale, y + 50 * scale))
        space.add(c_left_leg)

        c_body_right_leg = pymunk.PivotJoint(right_leg_1, telo_1, (x, y + 30 * scale))
        c_body_left_leg = pymunk.PivotJoint(left_leg_1, telo_1, (x, y + 30 * scale))
        spring_legs = pymunk.DampedSpring(left_feet_1, right_feet_1, (-20 * scale, 70 * scale), (20 * scale, 70 * scale),
                                          40 * scale, 500, 50)
        spring_legs_2 = pymunk.DampedSpring(left_leg_1, right_leg_1, (-20 * scale, 50 * scale),
                                            (20 * scale, 50 * scale), 50 * scale, 500, 50)
        spring_body_right_leg = pymunk.DampedSpring(telo_1, right_feet_1, (0, 20 * scale), (20 * scale, 70 * scale),
                                                    70 * scale, 500, 0.3)
        spring_body_left_leg = pymunk.DampedSpring(telo_1, left_feet_1, (0, 20 * scale), (-20 * scale, 70 * scale),
                                                   70 * scale, 500, 0.3)
        space.add(c_body_right_leg)
        space.add(c_body_left_leg)
        space.add(spring_legs)
        space.add(spring_legs_2)
        space.add(spring_body_right_leg)
        space.add(spring_body_left_leg)

        right_arm_1 = add_lever((x, y), (0, -5 * scale), (15 * scale, -20 * scale), 16, 985, 'right_arm_1')
        right_hand_1 = add_lever((x, y), (15 * scale, -20 * scale), (40 * scale, -45 * scale), 32, 991, 'right_hand_1')
        c_right_arm = pymunk.PivotJoint(right_arm_1, right_hand_1, (x + 15 * scale, y - 20 * scale))
        space.add(c_right_arm)

        left_arm_1 = add_lever((x, y), (0, -5 * scale), (-15 * scale, -20 * scale), 4, 997, 'left_arm_1')
        left_hand_1 = add_lever((x, y), (-15 * scale, -20 * scale), (-40 * scale, -45 * scale), 8, 1019, 'left_hand_1')
        c_left_arm = pymunk.PivotJoint(left_arm_1, left_hand_1, (x - 15 * scale, y - 20 * scale))
        space.add(c_left_arm)

        c_body_right_arm = pymunk.PivotJoint(right_arm_1, telo_1, (x, y - 5 * scale))
        c_body_left_arm = pymunk.PivotJoint(left_arm_1, telo_1, (x, y - 5 * scale))
        spring_body_right_arm = pymunk.DampedSpring(telo_1, right_arm_1, (0, 20 * scale), (20 * scale, -20 * scale),
                                                    40 * scale, 200, 0.3)
        spring_body_left_arm = pymunk.DampedSpring(telo_1, left_arm_1, (0, 20 * scale), (-20 * scale, -20 * scale),
                                                   40 * scale, 200, 0.3)
        space.add(c_body_right_arm)
        space.add(c_body_left_arm)
        space.add(spring_body_right_arm)
        space.add(spring_body_left_arm)

        complect_1 = ([head_1, telo_1, right_arm_1, left_arm_1,
                          right_leg_1, left_leg_1])
        points_1 = 100

    def create_Human_2(x, y):
        global complect_2, points_2
        telo_2 = add_lever_2((x, y), (0, 30 * scale), (0, -30 * scale), 2, 682, 'body_2')
        head_2 = add_ball((x, y - 30 * scale), 1, 1021, 'head_2')
        c_head_body = pymunk.PivotJoint(head_2, telo_2, (x, y - 30 * scale))
        c_head_body.color = pygame.Color('white')
        space.add(c_head_body)

        right_leg_2 = add_lever_2((x, y), (0, 30 * scale), (20 * scale, 50 * scale), 256, 477, 'right_leg_2')
        right_feet_2 = add_lever_2((x, y), (20 * scale, 50 * scale), (20 * scale, 80 * scale), 512, 767, 'right_feet_2')
        c_right_leg = pymunk.PivotJoint(right_leg_2, right_feet_2, (x + 20 * scale, y + 50 * scale))
        c_right_leg.color = pygame.Color('red')
        space.add(c_right_leg)

        left_leg_2 = add_lever_2((x, y), (0, 30 * scale), (-20 * scale, 50 * scale), 64, 637, 'left_leg_2')
        left_feet_2 = add_lever_2((x, y), (-20 * scale, 50 * scale), (-20 * scale, 80 * scale), 128, 959, 'left_feet_2')
        c_left_leg = pymunk.PivotJoint(left_leg_2, left_feet_2, (x - 20 * scale, y + 50 * scale))
        space.add(c_left_leg)

        c_body_right_leg = pymunk.PivotJoint(right_leg_2, telo_2, (x, y + 30 * scale))
        c_body_left_leg = pymunk.PivotJoint(left_leg_2, telo_2, (x, y + 30 * scale))
        spring_legs = pymunk.DampedSpring(left_feet_2, right_feet_2, (-20 * scale, 70 * scale), (20 * scale, 70 * scale),
                                          40 * scale, 500, 50)
        spring_legs_2 = pymunk.DampedSpring(left_leg_2, right_leg_2, (-20 * scale, 50 * scale),
                                            (20 * scale, 50 * scale), 50 * scale, 500, 50)
        spring_body_right_leg = pymunk.DampedSpring(telo_2, right_feet_2, (0, 20 * scale), (20 * scale, 70 * scale),
                                                    70 * scale, 500, 0.3)
        spring_body_left_leg = pymunk.DampedSpring(telo_2, left_feet_2, (0, 20 * scale), (-20 * scale, 70 * scale),
                                                   70 * scale, 500, 0.3)
        space.add(c_body_right_leg)
        space.add(c_body_left_leg)
        space.add(spring_legs)
        space.add(spring_legs_2)
        space.add(spring_body_right_leg)
        space.add(spring_body_left_leg)

        right_arm_2 = add_lever_2((x, y), (0, -5 * scale), (15 * scale, -20 * scale), 16, 985, 'right_arm_2')
        right_hand_2 = add_lever_2((x, y), (15 * scale, -20 * scale), (40 * scale, -45 * scale), 32, 991, 'right_hand_2')
        c_right_arm = pymunk.PivotJoint(right_arm_2, right_hand_2, (x + 15 * scale, y - 20 * scale))
        space.add(c_right_arm)

        left_arm_2 = add_lever_2((x, y), (0, -5 * scale), (-15 * scale, -20 * scale), 4, 997, 'left_arm_2')
        left_hand_2 = add_lever_2((x, y), (-15 * scale, -20 * scale), (-40 * scale, -45 * scale), 8, 1019, 'left_hand_2')
        c_left_arm = pymunk.PivotJoint(left_arm_2, left_hand_2, (x - 15 * scale, y - 20 * scale))
        space.add(c_left_arm)

        c_body_right_arm = pymunk.PivotJoint(right_arm_2, telo_2, (x, y - 5 * scale))
        c_body_left_arm = pymunk.PivotJoint(left_arm_2, telo_2, (x, y - 5 * scale))
        spring_body_right_arm = pymunk.DampedSpring(telo_2, right_arm_2, (0, 20 * scale), (20 * scale, -20 * scale),
                                                    40 * scale, 200, 0.3)
        spring_body_left_arm = pymunk.DampedSpring(telo_2, left_arm_2, (0, 20 * scale), (-20 * scale, -20 * scale),
                                                   40 * scale, 200, 0.3)
        space.add(c_body_right_arm)
        space.add(c_body_left_arm)
        space.add(spring_body_right_arm)
        space.add(spring_body_left_arm)

        complect_2 = ([head_2, telo_2, right_arm_2, left_arm_2,
                          right_leg_2, left_leg_2])
        points_2 = 100

    def walls():
        floor_shape = pymunk.Segment(space.static_body, (0, H), (W, H), 50)
        space.add(floor_shape)

        left_wall_shape = pymunk.Segment(space.static_body, (0, 0), (0, H), 50)
        space.add(left_wall_shape)

        right_wall_shape = pymunk.Segment(space.static_body, (W, 0), (W, H), 50)
        space.add(right_wall_shape)

        roof_shape = pymunk.Segment(space.static_body, (0, 0), (W, 0), 50)
        space.add(roof_shape)

    def create_blood(space, center, radius):
        body = pymunk.Body(1000, 1000)
        body.position = center
        shape = pymunk.Circle(body, radius)
        shape.color = pygame.Color('red')
        shape.filter = pymunk.ShapeFilter(categories=1024 , mask=0)
        space.add(body, shape)  # Объединили душу и тело
        v1 = random.randint(-300, 300)
        v2 = random.randint(30, 300)
        body.velocity = (v1,v2)
        balls.append(shape)
        return shape

    def draw_blood(arbiter, space, data):
        global complect_1, complect_2
        for c in arbiter.contact_point_set.points:
            r = max(3, abs(c.distance * 5))
            r = int(r)

            p = pymunk.pygame_util.to_pygame(c.point_a, data["surface"])
            pygame.draw.circle(data["surface"], pygame.Color("black"), p, r, 1)
            for i in range(100):
                create_blood(space, p, 2)
            sound2.play()

            ### Draw stuff
            balls_to_remove = []
            for ball in balls:
                if ball.body.position.y > 700:
                    balls_to_remove.append(ball)
                p = tuple(map(int, ball.body.position))
                pygame.draw.circle(screen, pygame.Color("blue"), p, int(ball.radius), 2)

            for ball in balls_to_remove:
                space.remove(ball, ball.body)
                balls.remove(ball)
        return True

    def count_points(arbiter, space, data):
        global points_1, points_2
        part_1 = arbiter.shapes[0]
        part_2 = arbiter.shapes[1]
        #print(part_1)
        #print(part_2)
        if part_1 == head_list[0]:
            if part_2 == head_list[1]:
                points_1 -= 2
                points_2 -= 2
            if part_2 == human_2_shapes[0]:
                points_2 -= 1
            for i in range(1, 5, 1):
                if part_2 == human_2_shapes[i]:
                    points_2 -= 3
            for i in range(5, 9, 1):
                if part_2 == human_2_shapes[i]:
                    points_2 -= 2

        elif part_1 == head_list[1]:
            if part_2 == human_1_shapes[0]:
                points_1 -= 1
            for i in range(1, 5, 1):
                if part_2 == human_1_shapes[i]:
                    points_1 -= 3
            for i in range(5, 9, 1):
                if part_2 == human_1_shapes[i]:
                    points_1 -= 2

        elif part_1 == human_1_shapes[0]:
            for i in range(1, 5, 1):
                if part_2 == human_2_shapes[i]:
                    points_2 -= 2
            for i in range(5, 9, 1):
                if part_2 == human_2_shapes[i]:
                    points_2 -= 1

        elif part_1 == human_2_shapes[0]:
            for i in range(1, 5, 1):
                if part_2 == human_1_shapes[i]:
                    points_1 -= 2
            for i in range(5, 9, 1):
                if part_2 == human_1_shapes[i]:
                    points_1 -= 1

    def add_blood_handler(object_1, object_2):
        handler = space.add_collision_handler(collision_types[object_1], collision_types[object_2])
        handler.data["surface"] = screen
        handler.begin = draw_blood
        handler.separate = count_points
        handlers.append(handler)

    create_Human_1(300, 450)
    create_Human_2(700, 450)

    room = create_room(space, 3)  # сюда обращаться за нужной комнатой
    room.run()

    head_list[1].color = pygame.Color('green')

    add_blood_handler('head_1', "head_2")
    add_blood_handler('head_1', "right_hand_2")
    add_blood_handler('head_1', "right_feet_2")
    add_blood_handler('head_1', "left_hand_2")
    add_blood_handler('head_1', "left_feet_2")
    add_blood_handler('body_1', "right_hand_2")
    add_blood_handler('body_1', "left_hand_2")
    add_blood_handler('body_1', "right_feet_2")
    add_blood_handler('body_1', "left_feet_2")

    add_blood_handler('head_2', "right_hand_1")
    add_blood_handler('head_2', "right_feet_1")
    add_blood_handler('head_2', "left_hand_1")
    add_blood_handler('head_2', "left_feet_1")
    add_blood_handler('body_2', "right_hand_1")
    add_blood_handler('body_2', "left_hand_1")
    add_blood_handler('body_2', "right_feet_1")
    add_blood_handler('body_2', "left_feet_1")


    def make_text(points_1, points_2):
        text_1 = font.render('Жизни: '+str(points_1), True, 'red')
        text_2 = font.render('Жизни: '+str(points_2), True, 'green2')
        screen.blit(text_1, (20, 20))
        screen.blit(text_2, (800, 20))


    def check_event_human_1():
        """Эта функция должна вызываться в главном цикле модуля тренажёрный зал или главного модуля"""
        if pygame.key.get_pressed()[K_RIGHT]:
            for part in complect_1:
                part.velocity += (30, 0)
        if pygame.key.get_pressed()[K_LEFT]:
            for part in complect_1:
                part.velocity += (-30, 0)
        if pygame.key.get_pressed()[K_UP]:
            for part in complect_1:
                part.velocity += (0, -30)
        if pygame.key.get_pressed()[K_DOWN]:
            for part in complect_1:
                part.velocity += (0, 30)


    def check_event_human_2():
        """Эта функция должна вызываться в главном цикле модуля тренажёрный зал или главного модуля"""
        if pygame.key.get_pressed()[K_d]:
            for part in complect_2:
                part.velocity += (30, 0)
        if pygame.key.get_pressed()[K_a]:
            for part in complect_2:
                part.velocity += (-30, 0)
        if pygame.key.get_pressed()[K_w]:
            for part in complect_2:
                part.velocity += (0, -30)
        if pygame.key.get_pressed()[K_s]:
            for part in complect_2:
                part.velocity += (0, 30)

    while alive:
        check_event_human_1()
        check_event_human_2()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                alive = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                alive = False
        screen.fill(WHITE)
        while_rooms_events(screen, room)
        space.step(1 / 40)  # Независимый цикл пересчитывающий физику
        space.debug_draw(draw_options)
        make_text(points_1, points_2)

        pygame.display.update()  # Обновляет весь экран, если не передать аргумент

        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main_battle(0)