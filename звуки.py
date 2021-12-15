import pygame as pg
import sys

pg.init()
sc = pg.display.set_mode((400, 300))

pg.mixer.music.load('.wav')
pg.mixer.music.play()

sound1 = pg.mixer.Sound('бросить карандаш.wav')
sound2 = pg.mixer.Sound('удар по груше.wav')

while 1:
    for i in pg.event.get():
        if i.type == pg.QUIT:
            sys.exit()

        elif i.type == pg.KEYUP:
            if i.key == pg.K_1:
                pg.mixer.music.pause()
                # pygame.mixer.music.stop()
            elif i.key == pg.K_2:
                pg.mixer.music.unpause()
                # pygame.mixer.music.play()
                pg.mixer.music.set_volume(0.5)
            elif i.key == pg.K_3:
                pg.mixer.music.unpause()
                # pygame.mixer.music.play()
                pg.mixer.music.set_volume(1)

        elif i.type == pg.MOUSEBUTTONUP:
            if i.button == 1:
                sound1.play()
            elif i.button == 3:
                sound2.play()

    pg.time.delay(20)