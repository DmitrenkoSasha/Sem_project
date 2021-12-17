# coding: utf-8
# license: GPLv3
from battle_zone import *
from gym import *

from functools import partial
from tkinter import *
import tkinter.font as font
from PIL import ImageTk, Image




class Menu:
    def __init__(self):
        self.background = r'задний план\menu_bg.png'
        self.color = 'lightgreen'
        self.images = []

    def random_bg(self):
        """Из множества собственных фонов случайным образом выбирает один
        :return: background - используется в show_manual(), show_room(), кнопках"""
        pass

    def clicked_gym(self):
        main_gym()

    def clicked_manual(self):
        self.show_manual()

    def clicked_rooms(self):
        self.show_rooms()

    def clicked(self, number_of_room):
        main_battle(number_of_room)

    def show_menu_2(self):
        self.window.destroy()
        self.show_menu()

    def add_image(self, path, width, height):
        img = Image.open(path)
        imag = img.resize((width, height), Image.ANTIALIAS)
        image = ImageTk.PhotoImage(imag)
        self.images.append(image)

    def show_rooms(self):
        self.window.destroy()
        self.window = Tk()
        self.window.title("Stickmen ahead")
        self.window.geometry('1000x700')
        width = 1000
        height = 700
        img = Image.open(self.background)
        imag = img.resize((width, height), Image.ANTIALIAS)
        image = ImageTk.PhotoImage(imag)
        width_1 = 280
        height_1 = round(width_1*0.7)
        self.images = []
        self.add_image(r'задний план\room_1.jpg', width_1, height_1)
        self.add_image(r'задний план\room_2.jpg', width_1, height_1)
        self.add_image(r'задний план\room_2.jpg', width_1, height_1)
        self.add_image(r'задний план\room_4.jpg', width_1, height_1)
        self.add_image(r'задний план\room_5.jpg', width_1, height_1)

        panel = Label(self.window, image=image)
        panel.pack(side="top", fill="both", expand=0)
        l = Label(width=40, height=2, bg='lightgreen', text="Выберите комнату", font=font.Font(family='Helvetica', size=15)).place(x=290, y=0)
        btn = Button(self.window, image=self.images[0], width=width_1, height=height_1, command=partial(self.clicked, 0)).place(x=80, y=40)
        btn = Button(self.window, image=self.images[1], width=width_1, height=height_1, command=partial(self.clicked, 1)).place(x=80+(width_1+10)*1, y=40)
        btn = Button(self.window, image=self.images[2], width=width_1, height=height_1, command=partial(self.clicked, 2)).place(x=80+(width_1+10)*2, y=40)
        btn = Button(self.window, image=self.images[3], width=width_1, height=height_1, command=partial(self.clicked, 3)).place(x=80+(width_1+10)*1, y=40+height_1+10)
        btn = Button(self.window, image=self.images[4], width=width_1, height=height_1, command=partial(self.clicked, 4)).place(x=80+(width_1+10)*1, y=40+height_1*2+20)
        btn = Button(self.window, text="В меню", bg='lightgreen', font=font.Font(family='Helvetica', size=15), width = 20, height = 1, command=partial(self.show_menu_2)).place(x=0, y=0)
        self.window.mainloop()

    def show_menu(self):
        self.window = Tk()
        self.window.title("Stickmen ahead")
        self.window.geometry('1000x700')
        img = Image.open(self.background)
        width = 1000
        height = 700
        imag = img.resize((width, height), Image.ANTIALIAS)
        image = ImageTk.PhotoImage(imag)
        panel = Label(self.window, image=image)
        panel.pack(side="top", fill="both", expand=0)
        l = Label(width=20, height=3, bg='#f5fb53', text="Stickman ahead", font=font.Font(family='Helvetica', size=40)).place(x=200, y=0)
        btn = Button(self.window, text="Тренажёрный зал", width = 24, height = 3, bg=self.color, font=font.Font(family='Helvetica', size=15), command=self.clicked_gym).place(x=370, y=200)
        btn = Button(self.window, text="Режим PvP", width = 24, height = 3, bg=self.color, font=font.Font(family='Helvetica', size=15), command=self.clicked_rooms).place(x=370, y=300)
        btn = Button(self.window, text="Управление", width = 24, height = 3, bg=self.color, font=font.Font(family='Helvetica', size=15), command=self.clicked_manual).place(x=370, y=400)
        btn = Button(self.window, text="Выход", width = 24, height = 3, bg=self.color, font=font.Font(family='Helvetica', size=15), command=self.window.destroy).place(x=370, y=500)
        self.window.mainloop()

    def show_manual(self):
        self.window.destroy()
        self.window = Tk()
        self.window.title("Stickmen ahead")
        self.window.geometry('1000x700')
        img = Image.open(self.background)
        width = 1000
        height = 700
        imag = img.resize((width, height), Image.ANTIALIAS)
        image = ImageTk.PhotoImage(imag)
        panel = Label(self.window, image=image)
        panel.pack(side="top", fill="both", expand=0)

        lbl = Label(self.window, bg='#f5fb53', font=font.Font(family='Helvetica', size=15), text="Ваша задача - уничтожить палочного противника раньше, чем он уничтожит вас").place(x=100, y=90)
        lbl = Label(self.window, bg='#f5fb53', font=font.Font(family='Helvetica', size=15),
                    text="Жизни снимаются при попадании в голову и тело").place(x=100, y=120)
        lbl = Label(self.window, bg='#f5fb53', font=font.Font(family='Helvetica', size=15),
                    text="Удачи!").place(x=100, y=150)
        lbl = Label(self.window, bg='#f5fb53', font=font.Font(family='Helvetica', size=15), text="Игрок 1 - стрелки на клавиатуре").place(x=20, y=250)
        lbl = Label(self.window, bg='#f5fb53', font=font.Font(family='Helvetica', size=15), text="Игрок 2 - кнопки WASD").place(x=700, y=250)
        btn = Button(self.window, font=font.Font(family='Helvetica', size=15), text="В меню", command=self.show_menu_2).place(x=0, y=0)
        self.window.mainloop()

menu = Menu()
menu.show_menu()

