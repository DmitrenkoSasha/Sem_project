from human import *
import pymunk.autogeometry

from pymunk.pygame_util import *
import pymunk.pygame_util
import random


from equipment import Pear, Ball


def main_gym():
    pygame.init()
    alive = True

    WHITE = (255, 255, 255)
    W = 1000
    H = 700
    FPS = 60

    bg = pygame.image.load(r'background.png')

    screen_gym = pygame.display.set_mode((W, H))
    space_gym = pymunk.Space()
    space_gym.gravity = (0, 900)  # По горизонтали 0, по вертикали 500 в вымышленных единицах
    space_gym.sleep_time_threshold = 0.3
    clock_gym = pygame.time.Clock()
    font_gym = pygame.font.SysFont("Arial", 16)
    options_gym = pymunk.pygame_util.DrawOptions(screen_gym)
    options_gym.flags = pymunk.SpaceDebugDrawOptions.DRAW_SHAPES
    pymunk.pygame_util.positive_y_is_up = False

    (img_x, img_y) = (100, 100)

    filename = 'мяч.png'

    def sample_func(point):
        try:
            position = pymunk.pygame_util.to_pygame(point, logo_img)
            color = logo_img.get_at(position)

            return color.a

        except:
            return 0

    # Generate geometry from pymunk logo image

    logo_img = pygame.image.load(filename).convert_alpha()
    logo_bb = pymunk.BB(0, 0, logo_img.get_width(), logo_img.get_height())

    logo_img.lock()
    line_set = pymunk.autogeometry.march_soft(logo_bb, logo_img.get_width(), logo_img.get_height(), 99, sample_func)
    logo_img.unlock()

    for line in line_set:

        # Returns a copy of a polyline simplified by using the Douglas-Peucker algorithm
        line = pymunk.autogeometry.simplify_curves(line, 0.7)

        for i in range(len(line) - 1):
            shape = pymunk.Segment(space_gym.static_body, line[i] + (img_x, img_y), line[i + 1] + (img_x, img_y), 1)
            shape.friction = 0.5
            shape.color = (255, 255, 255, 0)
            space_gym.add(shape)

    def show_img_things(equipment):
        """Рисует картинки элементов из списка снарядов в зале
        equipment: список снарядов, которые будут видны в зале, и с которыми можно взаимодействовать"""
        for one in equipment:
            if type(one) is Pear:
                rotated_logo_img, vec_to_c, ps = one.rotate()
                screen_gym.blit(rotated_logo_img, (round(vec_to_c.x), round(vec_to_c.y)))
                #  pygame.draw.lines(screen_gym, pygame.Color("red"), False, ps, 1)

    def walls():
        floor_shape = pymunk.Segment(space_gym.static_body, (0, H), (W, H), 30)
        space_gym.add(floor_shape)

        left_wall_shape = pymunk.Segment(space_gym.static_body, (0, 0), (0, H), 30)
        space_gym.add(left_wall_shape)

        right_wall_shape = pymunk.Segment(space_gym.static_body, (W, 0), (W, H), 30)
        space_gym.add(right_wall_shape)

        roof_shape = pymunk.Segment(space_gym.static_body, (0, 0), (W, 0), 30)
        space_gym.add(roof_shape)

    humans = []
    things = []
    active_thing = None

    h1 = Human(space_gym)
    humans.append(h1)
    h1.create_Human(400, 100, 0)
    walls()

    p1 = Pear(space_gym, 2 * W // 3, H // 2, 'груша.png', -1, 1)
    things.append(p1)

    mouse_joint = None
    mouse_body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)

    events = []
    events.append((5.0, Ball(space_gym, 300, 100).add_ball))
    events.append((10.0, Ball(space_gym, 300, 100).add_ball))
    events.sort(key=lambda z: z[0])
    total_time = 0

    smallball = pygame.USEREVENT + 1
    pygame.time.set_timer(smallball, 100)

    small_balls = 100

    while alive:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                alive = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                #  Встроенная ф-ция, чтобы переводить коорд. из формата pygame в pymunk
                p = from_pygame(event.pos, screen_gym)
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
                for x in range(10):
                    small_balls -= 1
                    mass = 3
                    radius = 8
                    moment = pymunk.moment_for_circle(mass, 0, radius)
                    b = pymunk.Body(mass, moment)
                    c = pymunk.Circle(b, radius)
                    c.friction = 1
                    b.position = random.randint(100, 400), 0

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

        space_gym.step(1 / FPS)  # Независимый цикл пересчитывающий физику
        screen_gym.fill(WHITE)
        screen_gym.blit(bg, (0, 0))
        space_gym.debug_draw(options_gym)
        show_img_things(things)
        screen_gym.blit(pygame.image.load('мяч.png').convert_alpha(), (img_x, img_y))

        pygame.display.flip()

        dt = clock_gym.tick(FPS)
        total_time += dt / 1000

    pygame.quit()
