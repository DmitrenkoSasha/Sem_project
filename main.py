import pygame
import pymunk
from Vision import *

WHITE = (255, 255, 255)

alive = True
FPS = 30
width = 1000
height = 600

screen = pg.display.set_mode((1000, 600))
space = pymunk.Space()  # Вселенная, в которой паймунк умеет считать физику
space.gravity = (0, 500)  # По горизонтали 0, по вертикали 500 в вымышленных единицах

def create_apple(space):
     body = pymunk.Body(1, 100, body_type= pymunk.Body.DYNAMIC) # масса, инертность, тип
     body.position = (500, 300)
     shape = pymunk.Circle(body, 80)  # Чтобы могло сталкиваться с другими
     space.add(body, shape)  # Объединили душу и тело
     return shape

def draw_apples(apples):
    for apple in apples:
        #pos_x = int(apple.body.positon.x)
        #pos_y = int(apple.body.positon.y)
        pygame.draw.circle(screen, (0,0,0), apple.body.position, 80)
        print(1)

apples = []
apples.append(create_apple(space))

def main():
    """Главная функция главного модуля.
    Создаёт объекты графического дизайна библиотеки tkinter: окно, холст, фрейм с кнопками, кнопки.
    """
    global physical_time
    global displayed_time
    global time_step
    global time_speed
    global space
    global start_button
    global perform_execution
    global timer
    global alive
    global apples

    print('Modelling started!')
    physical_time = 0
    pg.init()

    #last_time = time.perf_counter()
    drawer = Drawer(screen)
    #menu, box, timer = init_ui(screen)
    #write_to_stats()

    pygame.display.update()
    clock = pygame.time.Clock()
    while alive:
        clock.tick(FPS)
        #handle_events(pg.event.get(), menu)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                alive = False

        draw_apples(apples)
        space.step(1 / 50)  # Независимый цикл пересчитывающий физику
        #drawer.update(objects, box)
        screen.fill(WHITE)
        pygame.display.update()


if __name__ == "__main__":
    main()