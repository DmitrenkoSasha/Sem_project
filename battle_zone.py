import pygame
from pymunk.pygame_util import *
from typing import List
import random
import pymunk
import pymunk.pygame_util
from pymunk.vec2d import Vec2d
from pygame.locals import *
from pymunk.vec2d import Vec2d

from textures import *
from human import *


def main_battle(number_of_room):
    """ Запускает модуль battle_zone

        Params:
            number_of_room [int] - номер вызываемой комнаты
    """
    alive = True
    white = (255, 255, 255)

    pygame.init()

    screen = pygame.display.set_mode((W, H))
    bg = pygame.image.load(r'background.png')
    space = pymunk.Space()
    scale = 1.2
    space.gravity = (0, 100)  #
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("WeAreDIMDAM", 50)
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
    hart_img = pygame.image.load('hart.png')
    hart_img = pygame.transform.scale(hart_img, (300, 90))

    def create_blood(space, center, radius):
        """ Создаёт кровь в виде маленьких шариков

                Params:
                    space: [pymunk.Space] - область создания
                    center: [float, float] - место удара
                    radius: [float] - размер шариков
        """
        body = pymunk.Body(1000, 1000)
        body.position = center
        shape = pymunk.Circle(body, radius)
        shape.color = pygame.Color('red')
        shape.filter = pymunk.ShapeFilter(categories=1024, mask=0)
        space.add(body, shape)  # Объединили душу и тело
        v1 = random.randint(-300, 300)
        v2 = random.randint(30, 300)
        body.velocity = (v1, v2)
        balls.append(shape)
        return shape

    def draw_blood(arbiter, space, data):
        """ Отрисовывает кровь при столкновении

            Params:
                arbiter: [dict] - словарь для сталкивающихся тел
                space: [pymunk.Space] - область создания
                data: [dict] - данные о столкновении, генерируются автоматически
            Returns:
                collision: [bool] - Булеан, обозначающий, необходимо ли обрабатывать столкновение
        """
        for c in arbiter.contact_point_set.points:
            r = max(3, abs(c.distance * 5))
            r = int(r)

            p = pymunk.pygame_util.to_pygame(c.point_a, data["surface"])
            pygame.draw.circle(data["surface"], pygame.Color("black"), p, r, 1)
            for i in range(100):
                create_blood(space, p, 2)
            sound2.play()

            #  Draw stuff
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
        """ Подсчитывает очки после обработки столкновения
            Params:
                arbiter: [dict] - словарь для сталкивающихся тел
                space: [pymunk.Space] - область создания
                data: [dict] - данные о столкновении, генерируются автоматически
        """
        part_1 = arbiter.shapes[0]
        part_2 = arbiter.shapes[1]
        #print(part_1)
        #print(part_2)
        if part_1 == human_1.shapes[0]:
            if part_2 == human_2.shapes[0]:
                human_1.points -= 2
                human_2.points -= 2
            if part_2 == human_2.shapes[1]:
                human_1.points -= 1
            for i in range(2, 6, 1):
                if part_2 == human_2.shapes[i]:
                    human_1.points -= 3
            for i in range(6, 10, 1):
                if part_2 == human_2.shapes[i]:
                    human_1.points -= 2

        elif part_1 == human_2.shapes[0]:
            if part_2 == human_1.shapes[0]:
                human_1.points -= 2
                human_2.points -= 2
            if part_2 == human_1.shapes[1]:
                human_2.points -= 1
            for i in range(2, 6, 1):
                if part_2 == human_1.shapes[i]:
                    human_2.points -= 3
            for i in range(6, 10, 1):
                if part_2 == human_1.shapes[i]:
                    human_2.points -= 2

        elif part_1 == human_1.shapes[1]:
            for i in range(2, 6, 1):
                if part_2 == human_1.shapes[i]:
                    human_1.points -= 2
            for i in range(6, 10, 1):
                if part_2 == human_1.shapes[i]:
                    human_1.points -= 1

        elif part_1 == human_2.shapes[1]:
            for i in range(2, 6, 1):
                if part_2 == human_2.shapes[i]:
                    human_2.points -= 2
            for i in range(6, 10, 1):
                if part_2 == human_2.shapes[i]:
                    human_2.points -= 1

    def add_blood_handler(object_1, object_2):
        """ Добавляет обработчик столкновений между объектами с заданными типами collision_types
            Params:
                object_1: [int] - первый объект (из collision_types)
                object_2: [int] - второй объект (из collision_types)
        """
        handler = space.add_collision_handler(collision_types[object_1], collision_types[object_2])
        handler.data["surface"] = screen
        handler.begin = draw_blood
        handler.separate = count_points
        handlers.append(handler)

    human_1 = Human(space)
    human_1.create_Human(300, 450, 0)
    for shape in human_1.shapes:
        shape.color = pygame.Color('red')
    for shape in human_1_shapes:
        print(shape.collision_type)
    human_2 = Human(space)
    human_2.create_Human(700, 450, 10)
    for shape in human_2.shapes:
        shape.color = pygame.Color('green2')
    for shape in human_1_shapes:
        print(shape.collision_type)
    room = create_room(space, 2)  # сюда обращаться за нужной комнатой
    room.run()

    add_blood_handler(0, 13)
    add_blood_handler(0, 15)
    add_blood_handler(0, 17)
    add_blood_handler(0, 19)
    add_blood_handler(1, 13)
    add_blood_handler(1, 15)
    add_blood_handler(1, 17)
    add_blood_handler(1, 19)

    add_blood_handler(10, 3)
    add_blood_handler(10, 5)
    add_blood_handler(10, 7)
    add_blood_handler(10, 9)
    add_blood_handler(11, 3)
    add_blood_handler(11, 5)
    add_blood_handler(11, 7)
    add_blood_handler(11, 9)

    def make_text(points_1, points_2):
        """ Выводит на экран текст с количеством жизней у людей
            Params:
                points_1: [int] - жизни первого человека
                points_2: [int] - жизни второго человека
        """
        text_1 = font.render(str(points_1), True, 'red')
        text_2 = font.render(str(points_2), True, 'green2')
        screen.blit(text_1, (160, 5))
        screen.blit(text_2, (860, 5))

    while alive:
        human_1.check_event_human(K_UP, K_LEFT, K_DOWN, K_RIGHT)
        human_2.check_event_human(K_w, K_a, K_s, K_d)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                alive = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                alive = False
        screen.fill(white)
        screen.blit(bg, (0, 0))
        while_rooms_events(screen, room)

        space.step(1 / 40)  # Независимый цикл пересчитывающий физику
        space.debug_draw(draw_options)
        screen.blit(hart_img, (0, -25))
        screen.blit(hart_img, (700, -25))
        make_text(human_1.points, human_2.points)

        pygame.display.update()  # Обновляет весь экран, если не передать аргумент

        clock.tick(30)

    pygame.quit()


if __name__ == "__main__":
    main_battle(0)
