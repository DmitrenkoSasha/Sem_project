import pygame
import pymunk

WHITE = (255, 255, 255)
alive = True

pygame.init()
screen = pygame.display.set_mode((1000, 600))
space = pymunk.Space()  # Вселенная, в которой паймунк умеет считать физику
space.gravity = (0, 100)  # По горизонтали 0, по вертикали 500 в вымышленных единицах

def create_apple(space):
     body = pymunk.Body(1, 100, body_type= pymunk.Body.DYNAMIC) # масса, инертность, тип
     body.position = 500, 300
     shape = pymunk.Circle(body, 80)  # Чтобы могло сталкиваться с другими
     space.add(body, shape)  # Объединили душу и тело
     return shape

def draw_apples(apples):
    for apple in apples:
        pos_x = int(apple.body.position.x)
        pos_y = int(apple.body.position.y)
        pygame.draw.circle(screen, (0,0,0), (pos_x, pos_y), 80)
        print(1)

apples = []
apples.append(create_apple(space))

pygame.display.update()
clock = pygame.time.Clock()

while alive:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            alive = False
            print(apples)


    screen.fill(WHITE)
    draw_apples(apples)
    space.step(1 / 50)  # Независимый цикл пересчитывающий физику
    pygame.display.update()

    clock.tick(30)