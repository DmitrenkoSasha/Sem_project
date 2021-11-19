# coding: utf-8
# license: GPLv3

import pygame as pg

class Drawer:
    def __init__(self, screen):
        self.screen = screen

    def update(self, figures, ui):
        self.screen.fill('white')
        for figure in figures:
            figure.draw(self.screen)

        ui.blit()
        ui.update()
        pg.display.update()

class DrawableObject:
    def __init__(self, obj):
        self.obj = obj
        self.R = obj.R  # радиус тела в пикселях
        self.color = obj.color
        self.x = obj.x
        self.y = obj.y
        self.type = obj.type
        self.m = obj.m
        self.Vx = obj.Vx
        self.Vy = obj.Vy
        self.v = (obj.Vx ** 2 + obj.Vy ** 2) ** (0.5)

    def draw(self, surface):
        pass
        #pg.draw.circle(surface, self.color, (scale_x(self.x), scale_y(self.y)), self.R)
        #pg.draw.circle(surface, 'black', (scale_x(self.x), scale_y(self.y)), self.R, 2)