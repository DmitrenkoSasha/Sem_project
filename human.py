import pygame
import pymunk
import pymunk.pygame_util
from pymunk.vec2d import Vec2d

WHITE = (255, 255, 255)
alive = True

pygame.init()
screen = pygame.display.set_mode((1000, 600))
space = pymunk.Space()  # Вселенная, в которой паймунк умеет считать физику
space.gravity = (0, 100)  # По горизонтали 0, по вертикали 500 в вымышленных единицах
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 16)
draw_options = pymunk.pygame_util.DrawOptions(screen)

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
    shape = pymunk.Circle(body, radius, (0,0))
    space.add(body, shape)  # Объединили душу и тело
    return shape

def add_ball(space, pos):
    body = pymunk.Body()
    body.position = Vec2d(*pos)
    shape = pymunk.Circle(body, 15)
    shape.mass = 1
    shape.friction = 0.7
    shape.filter = pymunk.ShapeFilter(group=1)
    shape.color = (142, 68, 173, 255)
    space.add(body, shape)
    return body

def add_lever(space, pos, x1, x2):
    body = pymunk.Body()
    body.position = pos
    shape = pymunk.Segment(body, x1, x2, 4)
    shape.mass = 1
    shape.friction = 0.7
    shape.color = (142, 68, 173, 255)
    shape.filter = pymunk.ShapeFilter(group=1)
    space.add(body, shape)
    return body


telo = add_lever(space, (200, 200), (0, 30), (0, -30))
head = add_ball(space, (200, 180))
c_head_body = pymunk.PivotJoint(head, telo, (200, 180))
space.add(c_head_body)

right_leg_1 = add_lever(space, (200, 200), (0, 30), (30, 60))
right_leg_2 = add_lever(space, (200, 200), (30, 60), (30, 90))
c_right_leg = pymunk.PivotJoint(right_leg_1, right_leg_2, (230, 260))
space.add(c_right_leg)

left_leg_1 = add_lever(space, (200, 200), (0, 30), (-30, 60))
left_leg_2 = add_lever(space, (200, 200), (-30, 60), (-30, 90))
c_left_leg = pymunk.PivotJoint(left_leg_1, left_leg_2, (170, 260))
space.add(c_left_leg)

c_body_right_leg = pymunk.PivotJoint(right_leg_1, telo, (200, 230))
c_body_left_leg = pymunk.PivotJoint(left_leg_1, telo, (200, 230))
space.add(c_body_right_leg)
space.add(c_body_left_leg)

right_arm_1 = add_lever(space, (200, 200), (0, -5), (30, -30))
right_arm_2 = add_lever(space, (200, 200), (30, -30), (50, -30))
c_right_arm = pymunk.PivotJoint(right_arm_1, right_arm_2, (230, 170))
space.add(c_right_arm)

left_arm_1 = add_lever(space, (200, 200), (0, -5), (-30, -30))
left_arm_2 = add_lever(space, (200, 200), (-30, -30), (-50, -30))
c_left_arm = pymunk.PivotJoint(left_arm_1, left_arm_2, (170, 170))
space.add(c_left_arm)

c_body_right_arm = pymunk.PivotJoint(right_arm_1, telo, (200, 195))
c_body_left_arm = pymunk.PivotJoint(left_arm_1, telo, (200, 195))
space.add(c_body_right_arm)
space.add(c_body_left_arm)


player_body = pymunk.Body(20, 200)
player_body.position = 300, 100
player_shape = pymunk.Segment(player_body, (-50, 0), (50, 0), 8)
player_shape.color = pygame.Color("red")
player_shape.elasticity = 50.0
player_shape.collision_type = 2
space.add(player_body, player_shape)


floor_body = pymunk.Segment(space.static_body, (0, 600), (1000, 600), 50)
floor_shape = pymunk.Segment(space.static_body, (0, 600), (1000, 600), 50)
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

ch = space.add_collision_handler(0, 0)
ch.data["surface"] = screen
ch.post_solve = draw_collision
    
balls = []
balls.append(create_ball(space))

pygame.display.update()
clock = pygame.time.Clock()

while alive:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            alive = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                telo.velocity += (400, 0)
                head.velocity += (400, 0)
            if event.key == pygame.K_LEFT:
                telo.velocity += (-400, 0)
                head.velocity += (-400, 0)
            if event.key == pygame.K_UP:
                telo.velocity += (0, -400)
                head.velocity += (0, -400)
            if event.key == pygame.K_DOWN:
                telo.velocity += (0, 400)
                head.velocity += (0, 400)
                
            if event.key == pygame.K_r:
                create_ball(space)

    screen.fill(WHITE)
    space.step(1 / 50)  # Независимый цикл пересчитывающий физику
    space.debug_draw(draw_options)
    pygame.display.update()

    clock.tick(30)

pygame.quit()
