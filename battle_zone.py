import pymunk.pygame_util
from textures import *
from human import *
from pygame import *


def main_battle(number_of_room):
    """ Запускает модуль battle_zone
            :param number_of_room [int] - номер вызываемой комнаты
    """
    alive = True
    end = False
    white = (255, 255, 255)

    pygame.init()

    screen = pygame.display.set_mode((W, H))

    bg1 = pygame.image.load(r'задний план\\background.png')
    bg2 = pygame.image.load(r'задний план\\фон2.jpg')

    bg5 = pygame.image.load(r'задний план\\фон4.jpg')

    bg7 = pygame.image.load(r'задний план\\фон7.png')
    bg8 = pygame.image.load(r'задний план\\фон8.png')

    bg10 = pygame.image.load(r'задний план\\фон10.jpg')
    bg12 = pygame.image.load(r'задний план\\фон12.jpg')
    bg14 = pygame.image.load(r'задний план\\фон14.jpg')

    bgss = [bg1, bg2, bg5, bg7, bg8, bg10, bg12, bg14]
    i = randint(0, 7)

    bg = bgss[i]
    bg = pygame.transform.scale(bg, (W, H))
    space = pymunk.Space()
    space.gravity = (0, 100)  #
    clock = pygame.time.Clock()
    great_font = pygame.font.SysFont("WeAreDIMDAM", 50)
    draw_options = pymunk.pygame_util.DrawOptions(screen)
    draw_options.flags = pymunk.SpaceDebugDrawOptions.DRAW_SHAPES
    balls = []

    pygame.mixer.music.load(r'sounds\\фон.wav')
    pygame.mixer.music.set_volume(0.1)
    pygame.mixer.music.play()
    sound2 = pygame.mixer.Sound(r'sounds\\удар по груше.wav')
    hart_img = pygame.image.load(r'задний план\\hart.png')
    hart_img = pygame.transform.scale(hart_img, (300, 90))

    def create_blood(spaces, center, radiuses):
        """Создаёт кровь в виде маленьких шариков
                :param spaces: [pymunk.Space] - область создания
                :param center: [float, float] - место удара
                :param radiuses: [float] - размер шариков
        """
        body = pymunk.Body(1000, 1000)
        body.position = center
        circle_shape = pymunk.Circle(body, radiuses)
        circle_shape.color = pygame.Color('red')
        circle_shape.filter = pymunk.ShapeFilter(categories=1024, mask=0)
        spaces.add(body, circle_shape)  # Объединили душу и тело
        v1 = randint(-300, 300)
        v2 = randint(30, 300)
        body.velocity = (v1, v2)
        balls.append(circle_shape)
        return circle_shape

    def draw_blood(arbiter, spaces, data):
        """ Отрисовывает кровь при столкновении
            :param arbiter: словарь для сталкивающихся тел
            :param pymunk.Space spaces: область создания
            :param dict data: данные о столкновении, генерируются автоматически

            :return: Булеан, обозначающий, необходимо ли обрабатывать столкновение
        """
        part_1 = arbiter.shapes[0]
        part_2 = arbiter.shapes[1]
        if ((part_1 in human_1.shapes) and (part_2 in human_2.shapes)) or (
                (part_2 in human_1.shapes) and (part_1 in human_2.shapes)):
            for point in arbiter.contact_point_set.points:
                r = max(3, abs(point.distance * 5))
                r = int(r)

                p = pymunk.pygame_util.to_pygame(point.point_a, data["surface"])
                pygame.draw.circle(data["surface"], pygame.Color("black"), p, r, 1)
                for n in range(50):
                    create_blood(spaces, p, 2)
                sound2.play()

                #  Draw stuff
                balls_to_remove = []
                for ball in balls:
                    if ball.body.position.y > 700:
                        balls_to_remove.append(ball)
                    pos = (ball.body.position.x, ball.body.position.y)
                    pygame.draw.circle(screen, pygame.Color("blue"), pos, int(ball.radius), 2)

                for ball in balls_to_remove:
                    spaces.remove(ball, ball.body)
                    balls.remove(ball)
        return True

    def count_points(arbiter, spaces, data):
        """ Подсчитывает очки после обработки столкновения
            :param arbiter: словарь для сталкивающихся тел
            :param pymunk.Space spaces: область создания
            :param dict data: данные о столкновении, генерируются автоматически
        """
        part_1 = arbiter.shapes[0]
        part_2 = arbiter.shapes[1]
        if (spaces == spaces) and (data == data):
            pass
        if part_1 == human_1.shapes[0]:
            if part_2 == human_2.shapes[0]:
                human_1.points -= 2
                human_2.points -= 2
            for n in range(2, 6, 1):
                if part_2 == human_2.shapes[n]:
                    human_1.points -= 2
            for n in range(6, 10, 1):
                if part_2 == human_2.shapes[n]:
                    human_1.points -= 3
        elif part_2 == human_1.shapes[0]:
            if part_1 == human_2.shapes[0]:
                human_1.points -= 2
                human_2.points -= 2
            for n in range(2, 6, 1):
                if part_1 == human_2.shapes[n]:
                    human_1.points -= 2
            for n in range(6, 10, 1):
                if part_1 == human_2.shapes[n]:
                    human_1.points -= 3  # head 1 blow
        elif part_1 == human_2.shapes[0]:
            if part_2 == human_1.shapes[0]:
                human_1.points -= 2
                human_2.points -= 2
            for n in range(2, 6, 1):
                if part_2 == human_1.shapes[n]:
                    human_2.points -= 2
            for n in range(6, 10, 1):
                if part_2 == human_1.shapes[n]:
                    human_2.points -= 3
        elif part_2 == human_2.shapes[0]:
            if part_1 == human_1.shapes[0]:
                human_1.points -= 2
                human_2.points -= 2
            for n in range(2, 6, 1):
                if part_1 == human_1.shapes[n]:
                    human_2.points -= 2
            for n in range(6, 10, 1):
                if part_1 == human_1.shapes[n]:
                    human_2.points -= 3  # head 2 blow

        if part_1 == human_1.shapes[1]:
            for n in range(2, 6, 1):
                if part_2 == human_2.shapes[n]:
                    human_1.points -= 1
            for n in range(6, 10, 1):
                if part_2 == human_2.shapes[n]:
                    human_1.points -= 2
        elif part_2 == human_1.shapes[1]:
            for n in range(2, 6, 1):
                if part_1 == human_2.shapes[n]:
                    human_1.points -= 1
            for n in range(6, 10, 1):
                if part_1 == human_2.shapes[n]:
                    human_1.points -= 2  # body 1 blow

        elif part_1 == human_2.shapes[1]:
            for n in range(2, 6, 1):
                if part_2 == human_1.shapes[n]:
                    human_2.points -= 1
            for n in range(6, 10, 1):
                if part_2 == human_1.shapes[n]:
                    human_2.points -= 2
        elif part_2 == human_2.shapes[1]:
            for n in range(2, 6, 1):
                if part_1 == human_1.shapes[n]:
                    human_2.points -= 1
            for n in range(6, 10, 1):
                if part_1 == human_1.shapes[n]:
                    human_2.points -= 2  # body 1 blow

    def add_blood_handler(object_1, object_2):
        """ Добавляет обработчик столкновений между объектами с заданными типами collision_types
                :param int object_1: первый объект (из collision_types)
                :param int object_2: второй объект (из collision_types)
        """
        handler = space.add_collision_handler(object_1, object_2)
        handler.data["surface"] = screen
        handler.begin = draw_blood
        handler.separate = count_points

    def announce_winner(number_of_human):
        """ Выводит на экран победителя
                :param int number_of_human: номер победившего игрока
        """
        announcement = great_font.render('Победил игрок номер ' + str(number_of_human) + '!', True, (255, 255, 255))
        screen.blit(announcement, (300, 350))

    human_1 = Human(space)
    human_1.create_human(100, 600)
    for shape in human_1.shapes:
        shape.color = pygame.Color('red')
    human_2 = Human(space)
    human_2.create_human(900, 600)
    for shape in human_2.shapes:
        shape.color = pygame.Color('blue')

    add_blood_handler(0, 0)
    add_blood_handler(0, 3)
    add_blood_handler(1, 3)

    def make_text(points_1, points_2):
        """ Выводит на экран текст с количеством жизней у людей
                :param int points_1: жизни первого человека
                :param int points_2: жизни второго человека
        """
        text_1 = great_font.render(str(points_1), True, (255, 0, 0))
        text_2 = great_font.render(str(points_2), True, (0, 0, 255))
        font_exit = pygame.font.SysFont("WeAreDIMDAM", 30)
        text_3 = font_exit.render('В меню', True, (0, 0, 0))
        screen.blit(text_1, (160, 0))
        screen.blit(text_2, (860, 0))
        screen.blit(text_3, (462, 680))

    room = create_room(space, number_of_room)  # сюда обращаться за нужной комнатой

    room.run()

    while alive:
        human_1.check_event_human(K_UP, K_LEFT, K_DOWN, K_RIGHT)
        human_2.check_event_human(K_w, K_a, K_s, K_d)
        for events in pygame.event.get():
            if events.type == pygame.QUIT:
                alive = False
            elif events.type == pygame.MOUSEBUTTONDOWN and (mouse.get_pos()[0] > 460) and (
                    mouse.get_pos()[0] < 540) and (mouse.get_pos()[1] > 680):
                alive = False
            elif events.type == pygame.KEYDOWN and events.key == pygame.K_ESCAPE:
                alive = False

        screen.fill(white)
        screen.blit(bg, (0, 0))
        space.debug_draw(draw_options)
        while_rooms_events(screen, room)

        space.step(1 / 40)  # Независимый цикл пересчитывающий физику

        screen.blit(hart_img, (0, -25))
        screen.blit(hart_img, (700, -25))
        pygame.draw.rect(screen, (128, 128, 128), (460, 670, 80, 30))
        if not end:
            if human_1.points <= 0:
                human_1.points = 0
                announce_winner(2)
                end = True
                pygame.display.update()
            if human_2.points <= 0:
                human_2.points = 0
                announce_winner(1)
                end = True
                pygame.display.update()

            make_text(human_1.points, human_2.points)

            pygame.display.update()  # Обновляет весь экран, если не передать аргумент

        clock.tick(30)

    pygame.quit()


if __name__ == "__main__":
    main_battle(0)
