import pymunk
import random
import pygame
W = 1000
H = 700

def create_floor(space, x, y):
    floor_body = pymunk.Body(body_type=pymunk.Body.STATIC)
    floor_body.position = x, y
    floor_shape = pymunk.Poly.create_box(floor_body, (W*0.7, 10))
    floor_shape.elasticity = 10.0
    floor_shape.friction = 1.0
    space.add(floor_body, floor_shape)

def create_square(space, x, y):
    square_body = pymunk.Body(body_type=pymunk.Body.STATIC)
    square_body.position = x, y
    square_shape = pymunk.Segment(square_body, (x, y), (x+1, y+1), 15)
    square_shape.elasticity = 10.0
    square_shape.friction = 0.1
    square_shape.friction = 1.0
    space.add(square_body, square_shape)

def common_walls(space):
    floor_shape = pymunk.Segment(space.static_body, (0, H), (W, H), 50)
    space.add(floor_shape)

    left_wall_shape = pymunk.Segment(space.static_body, (0, 0), (0, H), 50)
    space.add(left_wall_shape)

    right_wall_shape = pymunk.Segment(space.static_body, (W, 0), (W, H), 50)
    space.add(right_wall_shape)

    roof_shape = pymunk.Segment(space.static_body, (0, 0), (W, 0), 50)
    space.add(roof_shape)

def four_extra_walls(space):
    common_walls(space)

    up_wall = pymunk.Segment(space.static_body, (W/2, 0), (W/2, H*2/7), 50)
    space.add(up_wall)
    down_wall = pymunk.Segment(space.static_body, (W/2, H*5/7), (W/2, H), 50)
    space.add(down_wall)
    right_wall = pymunk.Segment(space.static_body, (0, H/2), (W*0.3, H/2), 50)
    space.add(right_wall)
    left_wall = pymunk.Segment(space.static_body, (W*0.7, H/2), (W, H/2), 50)
    space.add(left_wall)

def three_levels(space):
    common_walls(space)

    create_floor(space, W/2, H/4)
    create_floor(space, W/2, H/2)
    create_floor(space, W/2, 3*H/4)

def random_circles(space):
    common_walls(space)

    for i in range (1, 22, 1):
        x = random.randint(100, W-100)
        y = random.randint(100, H-100)
        create_square(space, x/2, y/2)

def gravity_change(space):
    common_walls(space)

    space.gravity = (0, -200)

def create_room(space, number_of_room):
    if number_of_room == 0:
        common_walls(space)
    if number_of_room == 1:
        four_extra_walls(space)
    if number_of_room == 2:
        three_levels(space)
    if number_of_room == 3:
        random_circles(space)
    if number_of_room == 4:
        gravity_change(space)