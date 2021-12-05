import pygame
import pymunk
import pymunk.pygame_util
from pymunk.vec2d import Vec2d

pygame.init()
screen = pygame.display.set_mode((1000, 600))
space = pymunk.Space()
space.gravity = (0, 100)
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 16)
options = pymunk.pygame_util.DrawOptions(screen)
options.flags = pymunk.SpaceDebugDrawOptions.DRAW_SHAPES

def draw_collision(arbiter, space, data):
    for c in arbiter.contact_point_set.points:
        r = max(3, abs(c.distance * 5))
        r = int(r)

        p = pymunk.pygame_util.to_pygame(c.point_a, data["surface"])
        pygame.draw.circle(data["surface"], pygame.Color("black"), p, r, 1)
        

def create_ball(space):
    body = pymunk.Body(1, 10)
    body.position = (500, 300)
    radius = 25
    shape = pymunk.Circle(body, radius)
    space.add(body, shape)  # Объединили душу и тело
    return shape

def add_ball(space, pos, category, mask):
    body = pymunk.Body()
    body.position = Vec2d(*pos)
    shape = pymunk.Circle(body, 15)
    shape.mass = 1
    shape.friction = 0.7
    shape.filter = pymunk.ShapeFilter(categories = category, mask = mask)
    shape.color = pygame.Color('red')
    space.add(body, shape)
    return body

def add_lever(space, pos, x1, x2, category, mask):
    body = pymunk.Body()
    body.position = pos
    shape = pymunk.Segment(body, x1, x2, 6)
    shape.mass = 1
    shape.friction = 50
    shape.color = pygame.Color('blue')
    shape.filter = pymunk.ShapeFilter(categories = category, mask = mask)
    space.add(body, shape)
    return body

def add_lever_2(space, pos, x1, x2, category, mask):
    body = pymunk.Body()
    body.position = pos
    shape = pymunk.Segment(body, x1, x2, 8)
    shape.mass = 1
    shape.friction = 0.7
    shape.color = (142, 68, 173, 255)
    shape.color = pygame.Color('blue')
    shape.filter = pymunk.ShapeFilter(categories = category, mask = mask)
    space.add(body, shape)
    return body


def create_Human():
    global complect  # вынужденная приспособа
    telo = add_lever_2(space, (200, 200), (0, 30), (0, -30), 2, 682)
    head = add_ball(space, (200, 170), 1, 1021)
    c_head_body = pymunk.PivotJoint(head, telo, (200, 170))
    c_head_body.color = pygame.Color('white')
    space.add(c_head_body)

    right_leg_1 = add_lever(space, (200, 200), (0, 30), (20, 50), 256, 477)
    right_leg_2 = add_lever(space, (200, 200), (20, 50), (20, 80), 512, 767)
    c_right_leg = pymunk.PivotJoint(right_leg_1, right_leg_2, (220, 250))
    c_right_leg.color = pygame.Color('red')
    space.add(c_right_leg)

    left_leg_1 = add_lever(space, (200, 200), (0, 30), (-20, 50), 64, 637)
    left_leg_2 = add_lever(space, (200, 200), (-20, 50), (-20, 80), 128, 959)
    c_left_leg = pymunk.PivotJoint(left_leg_1, left_leg_2, (180, 250))
    space.add(c_left_leg)

    c_body_right_leg = pymunk.PivotJoint(right_leg_1, telo, (200, 230))
    c_body_left_leg = pymunk.PivotJoint(left_leg_1, telo, (200, 230))
    space.add(c_body_right_leg)
    space.add(c_body_left_leg)

    right_arm_1 = add_lever(space, (200, 200), (0, -5), (15, -20), 16, 985)
    right_arm_2 = add_lever(space, (200, 200), (15, -20), (40, -45), 32, 991)
    c_right_arm = pymunk.PivotJoint(right_arm_1, right_arm_2, (215, 180))
    space.add(c_right_arm)

    left_arm_1 = add_lever(space, (200, 200), (0, -5), (-15, -20), 4, 997)
    left_arm_2 = add_lever(space, (200, 200), (-15, -20), (-40, -45), 8, 1019)
    c_left_arm = pymunk.PivotJoint(left_arm_1, left_arm_2, (185, 180))
    space.add(c_left_arm)

    c_body_right_arm = pymunk.PivotJoint(right_arm_1, telo, (200, 195))
    c_body_left_arm = pymunk.PivotJoint(left_arm_1, telo, (200, 195))
    space.add(c_body_right_arm)
    space.add(c_body_left_arm)

    complect = [head, telo, right_arm_1, left_arm_1,
            right_leg_1, left_leg_1]

def check_event_human(event):
    """Эта функция должна вызываться в главном цикле модуля тренажёрный зал или главного модуля"""
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_RIGHT:
            for part in complect:
                part.velocity += (400, 0)
        if event.key == pygame.K_LEFT:
            for part in complect:
                part.velocity += (-400, 0)
        if event.key == pygame.K_UP:
            for part in complect:
                part.velocity += (0, -400)
        if event.key == pygame.K_DOWN:
            for part in complect:
                part.velocity += (0, 400)

        if event.key == pygame.K_r:
            create_ball(space)
        if event.key == pygame.K_h:
            create_Human()
    elif event.type == pygame.MOUSEMOTION:
        mouse_pos = pymunk.pygame_util.get_mouse_pos(screen)
def create_surface():
    floor_body = pymunk.Segment(space.static_body, (0, 600), (1000, 600), 50)
    floor_shape = pymunk.Segment(space.static_body, (0, 600), (1000, 600), 50)
    floor_shape.friction = 50
    space.add(floor_body, floor_shape)

    left_wall_body = pymunk.Segment(space.static_body, (0, 0), (0, 600), 50)
    left_wall_shape = pymunk.Segment(space.static_body, (0, 0), (0, 600), 50)
    space.add(left_wall_body, left_wall_shape)

    right_wall_body = pymunk.Segment(space.static_body, (1000, 0), (1000, 600), 50)
    right_wall_shape = pymunk.Segment(space.static_body, (1000, 0), (1000, 600), 50)
    space.add(right_wall_body, right_wall_shape)

    roof_body = pymunk.Segment(space.static_body, (0, 0), (1000, 0), 50)
    roof_shape = pymunk.Segment(space.static_body, (0, 0), (1000, 0), 50)
    space.add(roof_body, roof_shape)
    
def main():
    alive = True
    create_surface()
    while alive:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                alive = False
            check_event_human(event)
    
        screen.fill('WHITE')
        space.step(1 / 50)  # Независимый цикл пересчитывающий физику
        space.debug_draw(options)
        pygame.display.update()

        clock.tick(30)

    pygame.quit()
    
if __name__ == "__main__":
    main()

