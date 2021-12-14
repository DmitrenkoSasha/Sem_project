from human import *
import pymunk.autogeometry

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
options = pymunk.pygame_util.DrawOptions(screen)
options.flags = pymunk.SpaceDebugDrawOptions.DRAW_SHAPES


def show_img_things(equipment):
    """Рисует картинки элементов из списка снарядов в зале
    equipment: список снарядов, которые будут видны в зале, и с которыми можно взаимодействовать"""
    for one in equipment:
        if type(one) is Pear:
            rotated_logo_img, p, ps = one.rotate()
            screen.blit(rotated_logo_img, (round(p.x), round(p.y)))
            #pygame.draw.lines(screen, pygame.Color("red"), False, ps, 1)



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

h1 = Human(space)
humans.append(h1)
h1.create_Human(100, 100)
walls()

items = pygame.sprite.Group()
p1 = Pear(space, W//3, H//2, 'груша.png')
things.append(p1)
# items.add(p1)


mouse_joint = None
mouse_body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)

while alive:
    screen.fill(WHITE)
    for event in pygame.event.get():

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

            if mouse_joint is not None:
                space.remove(mouse_joint)
                mouse_joint = None

            p = Vec2d(*event.pos)

            hit = space.point_query_nearest(p, 5, pymunk.ShapeFilter())
            if hit is not None and hit.shape.body.body_type == pymunk.Body.DYNAMIC:
                # Используем ближайшую точку на поверхности в заданном радиусе
                # если точка нажатия мышки за формой тела
                if hit.distance > 0:
                    nearest = hit.point
                else:
                    nearest = p
                mouse_joint = pymunk.PivotJoint(
                    mouse_body, hit.shape.body, (0, 0), hit.shape.body.world_to_local(nearest)
                )
                mouse_joint.max_force = 50000
                mouse_joint.error_bias = (1 - 0.15) ** 60
                space.add(mouse_joint)

        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            alive = False
        elif event.type == pygame.MOUSEBUTTONUP:
            if mouse_joint is not None:
                space.remove(mouse_joint)
                mouse_joint = None
        elif event.type == pygame.MOUSEMOTION:
            mouse_pos = pymunk.pygame_util.get_mouse_pos(screen)
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_BACKSPACE:
            t = active_thing  # Находим тело, на которое нажали мышкой
            if t is not None:
                space.remove(t.shape, t.body)
                things.remove(t)


    mouse_pos = pygame.mouse.get_pos()
    mouse_body.position = mouse_pos
    #items.draw(screen)
    space.debug_draw(options)
    show_img_things(things)

    pygame.display.update()  # Обновляет весь экран, если не передать аргумент

    space.step(1 / 50)  # Независимый цикл пересчитывающий физику
    clock.tick(30)

pygame.quit()
