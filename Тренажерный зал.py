from pymunk.pygame_util import *


from human import *
from Груша import Pear
from typing import List

alive = True
WHITE = (255, 255, 255)

pygame.init()
W = 1000
H = 700
screen = pygame.display.set_mode((W, H))
space = pymunk.Space()
space.gravity = (0, 900)  # По горизонтали 0, по вертикали 500 в вымышленных единицах
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 16)
draw_options = pymunk.pygame_util.DrawOptions(screen)

logos: List[pymunk.Shape] = []


def work_with_items(items):
    for item in items:
        if type(item) is Pear:
            rotated_logo_img, p, ps = item.rotate()
            screen.blit(rotated_logo_img, (round(p.x), round(p.y)))
            pygame.draw.lines(screen, pygame.Color("red"), False, ps, 1)


def walls():
    floor_shape = pymunk.Segment(space.static_body, (0, H), (W, H), 50)
    space.add(floor_shape)

    left_wall_shape = pymunk.Segment(space.static_body, (0, 0), (0, H), 50)
    space.add(left_wall_shape)

    right_wall_shape = pymunk.Segment(space.static_body, (W, 0), (W, H), 50)
    space.add(right_wall_shape)

    roof_shape = pymunk.Segment(space.static_body, (0, 0), (W, 0), 50)
    space.add(roof_shape)

humans = []
active_shape = None

h1 = Human(space)
humans.append(h1)
h1.create_Human()
walls()

items = pygame.sprite.Group()
p1 = Pear(space, W//3, H//2, 'боксёрская груша.jpg')
items.add(p1)
logos.append(p1.shape)


mouse_joint = None
mouse_body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)

while alive:

    for event in pygame.event.get():

        mouse_joint = p1.check_event_pear(event, mouse_joint, mouse_body)
        h1.check_event_human(event)


        if event.type == pygame.QUIT:
            alive = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            p = from_pygame(event.pos, screen)
            active_shape = None
            for s in space.shapes:
                if type(s) is pymunk.shapes.Poly:
                    dist = s.point_query(p)[2]
                    if dist < 0:
                        active_shape = s

        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            alive = False
        elif event.type == pygame.MOUSEMOTION:
            mouse_pos = pymunk.pygame_util.get_mouse_pos(screen)
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_BACKSPACE:
            s = active_shape
            if s != None:
                space.remove(s, s.body)
                active_shape = None

    screen.fill(WHITE)
    work_with_items(items)
    # items.draw(screen)
    space.step(1 / 50)  # Независимый цикл пересчитывающий физику
    space.debug_draw(draw_options)
    pygame.display.update()  # Обновляет весь экран, если не передать аргумент

    clock.tick(30)

pygame.quit()
