from human import *
from pymunk.pygame_util import *

from Груша import Pear


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


def show_img_things(equipment):
    """Рисует картинки элементов из списка снарядов в зале
    equipment: список снарядов, которые будут видны в зале, и с которыми можно взаимодействовать"""
    for one in equipment:
        if type(one) is Pear:
            rotated_logo_img, p, ps = one.rotate()
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
things = []
active_shape = None
active_thing = None

h1 = Human(space, screen)
humans.append(h1)
h1.create_Human()
walls()

items = pygame.sprite.Group()
p1 = Pear(space, W//3, H//4, 'груша.png')
things.append(p1)
items.add(p1)


mouse_joint = None
mouse_body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)

while alive:

    for event in pygame.event.get():

        mouse_joint = p1.check_event_pear(event, mouse_joint, mouse_body)
        h1.check_event_human(event)

        if event.type == pygame.QUIT:
            alive = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            p = from_pygame(event.pos, screen)  # Встроенная ф-ция, чтобы переводить коорд. из формата pygame в pymunk
            active_shape = None
            active_thing = None
            for thing in things:
                if type(thing.shape) is pymunk.shapes.Poly:
                    dist = thing.shape.point_query(p)[2]  # Встроенная функция
                    if dist < 0:
                        active_thing = thing

        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            alive = False
        elif event.type == pygame.MOUSEMOTION:
            mouse_pos = pymunk.pygame_util.get_mouse_pos(screen)
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_BACKSPACE:
            t = active_thing  # Находим тело, на которое нажали мышкой
            if t is not None:
                space.remove(t.shape, t.body)
                things.remove(t)

    screen.fill(WHITE)

    #items.draw(screen)
    space.debug_draw(draw_options)
    show_img_things(things)

    pygame.display.update()  # Обновляет весь экран, если не передать аргумент

    space.step(1 / 50)  # Независимый цикл пересчитывающий физику
    clock.tick(30)

pygame.quit()
