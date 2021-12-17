
import pymunk.autogeometry
from pymunk.vec2d import Vec2d
from pymunk.pygame_util import *
import pymunk.pygame_util
import random

from human import *
from equipment import Pear, Ball
from textures import common_walls


def main_gym():
    pygame.init()
    alive = True

    white = (255, 255, 255)
    w = 1000
    h = 700
    fps = 60

    bg = pygame.image.load(r'задний план\background.png')

    screen_gym = pygame.display.set_mode((w, h))
    space_gym = pymunk.Space()
    space_gym.gravity = (0, 100)  # По горизонтали 0, по вертикали 500 в вымышленных единицах
    space_gym.sleep_time_threshold = 0.3
    clock_gym = pygame.time.Clock()
    options_gym = pymunk.pygame_util.DrawOptions(screen_gym)
    options_gym.flags = pymunk.SpaceDebugDrawOptions.DRAW_SHAPES
    pymunk.pygame_util.positive_y_is_up = False

    def show_img_things(equipment):
        """Рисует картинки элементов из списка снарядов в зале
        equipment: список снарядов, которые будут видны в зале, и с которыми можно взаимодействовать"""
        for one in equipment:
            if type(one) is Pear:
                rotated_logo_img, vec_to_c, ps = one.rotate()
                screen_gym.blit(rotated_logo_img, (round(vec_to_c.x), round(vec_to_c.y)))
                #  pygame.draw.lines(screen_gym, pygame.Color("red"), False, ps, 1)

    def make_exit_button(screen):
        pygame.draw.rect(screen, (128, 128, 128), (460, 670, 80, 30))
        font_exit = pygame.font.SysFont("WeAreDIMDAM", 30)
        text_exit = font_exit.render('В меню', True, (0, 0, 0))
        screen.blit(text_exit, (462, 680))

    humans = []
    things = []
    active_thing = None
    h1 = Human(space_gym)
    humans.append(h1)
    h1.create_human(400, 100, 1)
    common_walls(space_gym)
    p1 = Pear(space_gym, 2 * w // 3, h // 2, r'задний план\груша.png', -1, 1)
    things.append(p1)

    mouse_joint = None
    mouse_body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)

    events = [(5.0, Ball(space_gym, 300, 100).add_ball), (10.0, Ball(space_gym, 300, 100).add_ball)]
    events.sort(key=lambda z: z[0])
    total_time = 0

    smallball = pygame.USEREVENT + 1
    pygame.time.set_timer(smallball, 100)

    small_balls = 100

    while alive:

        for event in pygame.event.get():
            h1.check_event_human(pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d)

            if event.type == pygame.QUIT:
                alive = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                #  Встроенная ф-ция, чтобы переводить коорд. из формата pygame в pymunk
                p = from_pygame(event.pos, screen_gym)
                if (pygame.mouse.get_pos()[0] > 460) and (pygame.mouse.get_pos()[0] < 540)\
                        and (pygame.mouse.get_pos()[1] > 680):
                    alive = False
                active_thing = None
                for thing in things:
                    if type(thing.shape) is pymunk.shapes.Poly:
                        dist = thing.shape.point_query(p)[2]  # Встроенная функция
                        if dist < 0:
                            active_thing = thing
                if mouse_joint is not None:
                    space_gym.remove(mouse_joint)
                    mouse_joint = None

                p = Vec2d(*event.pos)

                hit = space_gym.point_query_nearest(p, 5, pymunk.ShapeFilter())
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
                    space_gym.add(mouse_joint)

            elif event.type == smallball:
                if small_balls <= 0:
                    pygame.time.set_timer(smallball, 0)
                for x in range(4):
                    small_balls -= 1
                    mass = 3
                    radius = 8
                    moment = pymunk.moment_for_circle(mass, 0, radius)
                    b = pymunk.Body(mass, moment)
                    c = pymunk.Circle(b, radius)
                    c.friction = 1
                    b.position = random.randint(100, 800), 0

                    space_gym.add(b, c)

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                alive = False
            elif event.type == pygame.MOUSEBUTTONUP:
                if mouse_joint is not None:
                    space_gym.remove(mouse_joint)
                    mouse_joint = None
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_BACKSPACE:
                t = active_thing  # Находим тело, на которое нажали мышкой
                if t is not None:
                    space_gym.remove(t.shape, t.body)
                    things.remove(t)

        mouse_pos = pygame.mouse.get_pos()
        mouse_body.position = mouse_pos
        if len(events) > 0 and total_time > events[0][0]:
            t, f = events.pop(0)

            f(space_gym)

        space_gym.step(1 / fps)  # Независимый цикл пересчитывающий физику
        screen_gym.fill(white)
        screen_gym.blit(bg, (0, 0))
        space_gym.debug_draw(options_gym)
        show_img_things(things)

        make_exit_button(screen_gym)

        pygame.display.flip()

        dt = clock_gym.tick(fps)
        total_time += dt / 1000

    pygame.quit()


if __name__ == "__main__":
    print("This module is not for a straight call!")
