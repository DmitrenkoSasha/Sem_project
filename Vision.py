# coding: utf-8
# license: GPLv3

from tkinter import *
from battle_zone import *
from gym import *
from functools import partial
from PIL import ImageTk, Image

background = r'background.png'

def clicked_gym():
    main_gym()

def clicked_manual():
    show_manual(background)

def clicked_rooms():
    show_rooms(background)

def clicked(number_of_room):
    main_battle(number_of_room)

def show_menu_2(background):
    window.destroy()
    show_menu(background)

def show_rooms(background):
    global window
    window.destroy()
    window = Tk()
    window.title("Stickmen ahead")
    window.geometry('1000x700')
    img = Image.open(background)
    width = 1000
    height = 700
    imag = img.resize((width, height), Image.ANTIALIAS)
    image = ImageTk.PhotoImage(imag)
    panel = Label(window, image=image)
    panel.pack(side="top", fill="both", expand="no")

    btn = Button(window, text="Обычная комната!", command=partial(clicked, 0)).place(x=250, y=120)
    btn = Button(window, text="Восемь стен!", command=partial(clicked, 1)).place(x=250, y=150)
    btn = Button(window, text="Три этажа!", command=partial(clicked, 2)).place(x=250, y=180)
    btn = Button(window, text="Случайные препятствия!", command=partial(clicked, 3)).place(x=250, y=210)
    btn = Button(window, text="Поломка гравитации!", command=partial(clicked, 4)).place(x=250, y=240)
    btn = Button(window, text="В меню", command=partial(show_menu_2, background)).place(x=250, y=270)
    window.mainloop()

def show_menu(background):
    global window
    window = Tk()
    window.title("Stickmen ahead")
    window.geometry('1000x700')
    img = Image.open(background)
    width = 1000
    height = 700
    imag = img.resize((width, height), Image.ANTIALIAS)
    image = ImageTk.PhotoImage(imag)
    panel = Label(window, image=image)
    panel.pack(side="top", fill="both", expand="no")
    font1 = pygame.font.SysFont('chalkduster.ttf', 72)
    btn = Button(window, text="Тренажёрный зал!", command=clicked_gym).place(x=250, y=100)
    btn = Button(window, text="Режим PvP!", command=clicked_rooms).place(x=250, y=200)
    btn = Button(window, text="Управление!", command=clicked_manual).place(x=250, y=300)
    btn = Button(window, text="Выход!", command=quit).place(x=250, y=400)
    window.mainloop()

def show_manual(background):
    global window
    window.destroy()
    window = Tk()
    window.title("Stickmen ahead")
    window.geometry('1000x700')
    img = Image.open(background)
    width = 1000
    height = 700
    imag = img.resize((width, height), Image.ANTIALIAS)
    image = ImageTk.PhotoImage(imag)
    panel = Label(window, image=image)
    panel.pack(side="top", fill="both", expand="no")

    lbl = Label(window, text="Игрок 1 - стрелки на клавиатуре").place(x=250, y=120)
    lbl = Label(window, text="Игрок 2 - кнопки WASD").place(x=250, y=140)
    btn = Button(window, text="В меню", command=partial(show_menu_2, background)).place(x=250, y=160)
    window.mainloop()

show_menu(background)

