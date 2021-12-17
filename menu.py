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

    @staticmethod
    def clicked_gym():
        """При нажатии на кнопку начинает исполнение модуля gym"""
        main_gym()

    @staticmethod
    def clicked(number_of_room):
        """ При нажатии на кнопку начинает исполнение модуля battle_zone
            Params:
                number_of_room: [int] - номер вызываемой комнаты
        """
        main_battle(number_of_room)

    def clicked_manual(self):
        """При нажатии на кнопку показывает manual"""
        self.show_manual()

    def clicked_rooms(self):
        """При нажатии на кнопку показывает rooms"""
        self.show_rooms()

    def create_menu_pattern(self):
        self.window = Tk()
        self.window.title("Stickmen ahead")
        self.window.geometry('1000x700')
        width = 1000
        height = 700
        img = Image.open(self.background)
        imag = img.resize((width, height), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(imag)
        return photo

    def show_menu_2(self):
        """При нажатии на кнопку показывает menu"""
        self.window.destroy()
        self.show_menu()

    def add_image(self, path, width, height):
        """ Позволяет добавить изображение на экран Tkinter
            Params:
                path: [str] - имя изображения
                width: [int] - ширина изображения в пикселях
                height: [int] - высота изображения в пикселях
        """
        img = Image.open(path)
        imag = img.resize((width, height), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(imag)
        self.images.append(photo)

    def show_rooms(self):
        """Показывает список комнат - rooms"""
        self.window.destroy()
        photo = self.create_menu_pattern()
        panel = Label(self.window, image=photo)
        panel.pack(side="top", fill="both", expand=0)
        width_1 = 280
        height_1 = round(width_1*0.7)
        self.images = []
        self.add_image(r'задний план\room_1.jpg', width_1, height_1)
        self.add_image(r'задний план\room_2.jpg', width_1, height_1)
        self.add_image(r'задний план\room_3.jpg', width_1, height_1)
        self.add_image(r'задний план\room_4.jpg', width_1, height_1)
        self.add_image(r'задний план\room_5.jpg', width_1, height_1)
        Label(width=40, height=2, bg='lightgreen', text="Выберите комнату",
              font=font.Font(size=15)).place(x=290, y=0)
        for i in range(0, 3, 1):
            Button(self.window, image=self.images[i], width=width_1, height=height_1,
                   command=partial(self.clicked, i)).place(x=80+(width_1+10)*i, y=40)
        for i in range(3, 5, 1):
            Button(self.window, image=self.images[i], width=width_1, height=height_1,
                   command=partial(self.clicked, i)).place(x=80+(width_1+10)*1, y=40+height_1*(i-2)+10)
        Button(self.window, text="В меню", bg='lightgreen', width=20, height=1,
               font=font.Font(size=15), command=partial(self.show_menu_2)).place(x=0, y=0)
        self.window.mainloop()

    def show_menu(self):
        """При нажатии на кнопку показывает menu - инициализирующий запуск"""
        photo = self.create_menu_pattern()
        panel = Label(self.window, image=photo)
        panel.pack(side="top", fill="both", expand=0)
        Label(width=20, height=3, bg='#f5fb53', text="Stickman ahead", font=font.Font(size=40)).place(x=200, y=0)
        Button(self.window, text="Тренажёрный зал", width=24, height=3, bg=self.color,
               font=font.Font(family='Helvetica', size=15), command=self.clicked_gym).place(x=370, y=200)
        Button(self.window, text="Режим PvP", width=24, height=3, bg=self.color,
               font=font.Font(family='Helvetica', size=15), command=self.clicked_rooms).place(x=370, y=300)
        Button(self.window, text="Управление", width=24, height=3, bg=self.color,
               font=font.Font(family='Helvetica', size=15), command=self.clicked_manual).place(x=370, y=400)
        Button(self.window, text="Выход", width=24, height=3, bg=self.color,
               font=font.Font(family='Helvetica', size=15), command=self.window.destroy).place(x=370, y=500)
        self.window.mainloop()

    def show_manual(self):
        """Показывает управление - manual"""
        self.window.destroy()
        photo = self.create_menu_pattern()
        panel = Label(self.window, image=photo)
        panel.pack(side="top", fill="both", expand=0)

        Label(self.window, bg='#f5fb53', font=font.Font(size=15),
              text="Ваша задача - уничтожить палочного противника раньше, чем он уничтожит вас").place(x=100, y=90)
        Label(self.window, bg='#f5fb53', font=font.Font(size=15),
              text="Жизни снимаются при попадании в голову и тело").place(x=100, y=120)
        Label(self.window, bg='#f5fb53', font=font.Font(size=15),
              text="Удачи!").place(x=100, y=150)
        Label(self.window, bg='#f5fb53', font=font.Font(size=15),
              text="Игрок 1 - стрелки на клавиатуре").place(x=20, y=250)
        Label(self.window, bg='#f5fb53', font=font.Font(size=15),
              text="Игрок 2 - кнопки WASD").place(x=700, y=250)
        Button(self.window, font=font.Font(size=15),
               text="В меню", command=self.show_menu_2).place(x=0, y=0)
        self.window.mainloop()


menu = Menu()
menu.show_menu()
