import pymunk.pygame_util
import pygame
from human import *
from Груша import Pear

alive = True
WHITE = (255, 255, 255)

pygame.init()
W = 1000
H = 600
screen = pygame.display.set_mode((W, H))
space.gravity = (0, 100)  # По горизонтали 0, по вертикали 500 в вымышленных единицах
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 16)
draw_options = pymunk.pygame_util.DrawOptions(screen)


def walls():
    floor_shape = pymunk.Segment(space.static_body, (0, 600), (1000, 600), 50)
    space.add(floor_shape)

    left_wall_shape = pymunk.Segment(space.static_body, (0, 0), (0, 600), 50)
    space.add(left_wall_shape)

    right_wall_shape = pymunk.Segment(space.static_body, (1000, 0), (1000, 600), 50)
    space.add(right_wall_shape)

    roof_shape = pymunk.Segment(space.static_body, (0, 0), (1000, 0), 50)
    space.add(roof_shape)

create_Human()
walls()
p1 = Pear(W//2, 'боксёрская груша.jpg')

while alive:
    for event in pygame.event.get():
        check_event_human(event)
        if event.type == pygame.QUIT:
            alive = False


    screen.fill(WHITE)
    screen.blit(p1.image, p1.rect)
    space.step(1 / 50)  # Независимый цикл пересчитывающий физику
    space.debug_draw(draw_options)
    pygame.display.update()

    clock.tick(30)

pygame.quit()