# coding: utf-8
# license: GPLv3

from functools import partial
from tkinter import *

from PIL import ImageTk, Image

from battle_zone import *
from gym import *




class Menu:
    def __init__(self):
        self.window = Tk()
        self.background = r'background.png'

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

    def show_rooms(self):
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
        panel.pack(side="top", fill="both", expand="no")

        btn = Button(self.window, text="Обычная комната!", command=partial(self.clicked, 0)).place(x=250, y=120)
        btn = Button(self.window, text="Восемь стен!", command=partial(self.clicked, 1)).place(x=250, y=150)
        btn = Button(self.window, text="Случайные препятствия!", command=partial(self.clicked, 2)).place(x=250, y=180)
        btn = Button(self.window, text="Три этажа!", command=partial(self.clicked, 3)).place(x=250, y=210)
        btn = Button(self.window, text="Поломка гравитации!", command=partial(self.clicked, 4)).place(x=250, y=240)
        btn = Button(self.window, text="В меню", command=partial(self.show_menu_2)).place(x=250, y=270)
        self.window.mainloop()

    def show_menu(self):
        self.window.title("Stickmen ahead")
        self.window.geometry('1000x700')
        img = Image.open(self.background)
        width = 1000
        height = 700
        imag = img.resize((width, height), Image.ANTIALIAS)
        image = ImageTk.PhotoImage(imag)
        panel = Label(self.window, image=image)
        panel.pack(side="top", fill="both", expand="no")
        btn = Button(self.window, text="Тренажёрный зал!", command=self.clicked_gym).place(x=250, y=100)
        btn = Button(self.window, text="Режим PvP!", command=self.clicked_rooms).place(x=250, y=200)
        btn = Button(self.window, text="Управление!", command=self.clicked_manual).place(x=250, y=300)
        btn = Button(self.window, text="Выход!", command=quit).place(x=250, y=400)
        self.window.mainloop()

    def show_manual(self):
        self.window.destroy()
        self.window.title("Stickmen ahead")
        self.window.geometry('1000x700')
        img = Image.open(self.background)
        width = 1000
        height = 700
        imag = img.resize((width, height), Image.ANTIALIAS)
        image = ImageTk.PhotoImage(imag)
        panel = Label(self.window, image=image)
        panel.pack(side="top", fill="both", expand="no")

        lbl = Label(self.window, text="Игрок 1 - стрелки на клавиатуре").place(x=250, y=120)
        lbl = Label(self.window, text="Игрок 2 - кнопки WASD").place(x=250, y=140)
        btn = Button(self.window, text="В меню", command=partial(self.show_menu_2)).place(x=250, y=160)
        self.window.mainloop()

if __name__ == "__main__":
    menu = Menu()
    menu.show_menu()

