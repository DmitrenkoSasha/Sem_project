import pygame
from pymunk.pygame_util import *
from human import *
from typing import List
import random
alive = True
WHITE = (255, 255, 255)

pygame.init()
W = 1000
H = 700
screen = pygame.display.set_mode((W, H))
space = pymunk.Space()
space.gravity = (0, 100)  # По горизонтали 0, по вертикали 500 в вымышленных единицах
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 16)
draw_options = pymunk.pygame_util.DrawOptions(screen)

collision_types = {
    "head": 1,
    "body": 2,
    "arm": 3,
    "leg": 4,
    "wall": 5
}


def create_blood(space, center, radius):
    body = pymunk.Body(1, 10)
    body.position = center
    shape = pymunk.Circle(body, radius)
    shape.color = pygame.Color('red')
    space.add(body, shape)  # Объединили душу и тело
    v1 = random.randint(-200, 200)
    v2 = random.randint(-200, 200)
    body.velocity = (v1,v2)
    return shape

def draw_blood(arbiter, space, data):
    for c in arbiter.contact_point_set.points:
        r = max(3, abs(c.distance * 5))
        r = int(r)

        p = pymunk.pygame_util.to_pygame(c.point_a, data["surface"])
        pygame.draw.circle(data["surface"], pygame.Color("black"), p, r, 1)
        create_blood(space, p, 5)

handler = space.add_collision_handler(collision_types["head"], collision_types["leg"])
handler.data["surface"] = screen
handler.post_solve = draw_blood

def walls():
    floor_shape = pymunk.Segment(space.static_body, (0, H), (W, H), 50)
    space.add(floor_shape)

    left_wall_shape = pymunk.Segment(space.static_body, (0, 0), (0, H), 50)
    space.add(left_wall_shape)

    right_wall_shape = pymunk.Segment(space.static_body, (W, 0), (W, H), 50)
    space.add(right_wall_shape)

    roof_shape = pymunk.Segment(space.static_body, (0, 0), (W, 0), 50)
    space.add(roof_shape)

def check_event_human_1(self, event):
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

    if (event.type == pygame.KEYDOWN) and (event.key == pygame.K_r):
        self.create_ball()

def check_event_human_2(self, event):
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

def points():
    pass

h1 = Human(space)
h1.create_Human(700, 200)
h1.complect[0].color = pygame.Color('green')

h2 = Human(space)
h2.create_Human(300, 300)

walls()

while alive:
    h1.check_event_human_1()
    h2.check_event_human_2()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            alive = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            alive = False
    screen.fill(WHITE)
    space.step(1 / 50)  # Независимый цикл пересчитывающий физику
    space.debug_draw(draw_options)
    pygame.display.update()  # Обновляет весь экран, если не передать аргумент

    clock.tick(30)

pygame.quit()
