from human import *
import pymunk.autogeometry

from pymunk.pygame_util import *
import pymunk.pygame_util
#from Окружение_картинки_ломанной import line_around_img

from Груша import Pear

def main_gym():
    alive = True
    WHITE = (255, 255, 255)

    pygame.init()
    W = 1000
    H = 700

    FPS = 60

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

    events = []
    events.append((10, h1.create_Human(500, 400)))
    events.append((100, h1.create_Human(500, 400)))
    events.sort(key=lambda x: x[0])
    total_time = 0

    mouse_joint = None
    mouse_body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)

    def sample_func(point):
        try:
            img = pygame.image.load("груша.png").convert_alpha()
            p = pymunk.pygame_util.to_pygame(point, img)
            color = img.get_at(p)

            return color.a
            #return color.hsla[2]
        except:
            return 0


    logo_img = pygame.image.load('груша.png').convert_alpha()
    logo_bb = pymunk.BB(0, 0, logo_img.get_width(), logo_img.get_height())

    logo_img.lock()
    #line_set = pymunk.autogeometry.march_soft(logo_bb, logo_img.get_width(), logo_img.get_height(), 10, sample_func)
    logo_img.unlock()

    r = 10


    '''for line in line_set:
    
        line = pymunk.autogeometry.simplify_curves(line, 0.7)  # Returns a copy of a polyline simplified by using the Douglas-Peucker algorithm
    
        max_x = 0
        min_x = 1000
        max_y = 0
        min_y = 1000
        for l in line:
            max_x = max(max_x, l.x)
            min_x = min(min_x, l.x)
            max_y = max(max_y, l.y)
            min_y = min(min_y, l.y)
        w, h = max_x - min_x, max_y - min_y
    
        # we skip the line which has less than 35 height, since its the "hole" in
        # the p in pymunk, and we dont need it.
        if h < 35:
            continue
    
        center = Vec2d(min_x + w / 2.0, min_y + h / 2.0)
    
        r += 30
        if r > 255:
            r = 0
    
    
        for i in range(len(line) - 1):
            shape = pymunk.Segment(space.static_body, line[i], line[i + 1], 1)
            shape.friction = 0.5
            shape.color = (255, 0, 0, 0)
            space.add(shape)'''


    while alive:

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

        if len(events) > 0 and total_time > events[0][0]:
            t, f = events.pop(0)

            f(space)

        space.step(1 / FPS)  # Независимый цикл пересчитывающий физику
        #items.draw(screen)
        screen.fill(WHITE)
        space.debug_draw(options)
        show_img_things(things)
        screen.blit(pygame.image.load('груша.png').convert_alpha(), (0, 0))


        pygame.display.flip()

        dt = clock.tick(FPS)
        total_time += dt / 1000.0

        #pygame.display.update()  # Обновляет весь экран, если не передать аргумент


        #clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main_gym()