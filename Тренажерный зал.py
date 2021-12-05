import pygame
import pymunk.pygame_util
from human import *


alive = True
WHITE = (255, 255, 255)

pygame.init()
screen = pygame.display.set_mode((1000, 600))
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
'''ch = space.add_collision_handler(0, 0)
ch.data["surface"] = screen
ch.post_solve = draw_collision'''

while alive:
    for event in pygame.event.get():
        check_event_human(event)
        if event.type == pygame.QUIT:
            alive = False


    screen.fill(WHITE)
    space.step(1 / 50)  # Независимый цикл пересчитывающий физику
    space.debug_draw(draw_options)
    pygame.display.update()

    clock.tick(30)

pygame.quit()