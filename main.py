import pygame
from Vision import *

WHITE = (255, 255, 255)

alive = True
FPS = 30

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

    print('Modelling started!')
    physical_time = 0

    pg.init()

    width = 1000
    height = 900
    screen = pg.display.set_mode((width, height))
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

        #drawer.update(objects, box)
        pygame.display.update()
        screen.fill(WHITE)

if __name__ == "__main__":
    main()