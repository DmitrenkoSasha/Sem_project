# coding: utf-8
# license: GPLv3

from tkinter import *
from battle_zone import *
from gym import *
from functools import partial

def clicked_gym():
    main_gym()

def clicked_manual():
    show_manual()

def clicked(number_of_room):
    main_battle(number_of_room)

def show_menu_2():
    window.destroy()
    show_menu()

def show_rooms():
    global window
    window.destroy()
    window = Tk()
    window.title("Stickmen ahead")
    window.geometry('1000x700')
    btn = Button(window, text="Обычная комната!", command=partial(clicked, 0))
    btn.grid(column=0, row=0)
    btn = Button(window, text="Восемь стен!", command=partial(clicked, 1))
    btn.grid(column=0, row=1)
    btn = Button(window, text="Три этажа!", command=partial(clicked, 2))
    btn.grid(column=0, row=2)
    btn = Button(window, text="Случайные препятствия!", command=partial(clicked, 3))
    btn.grid(column=0, row=3)
    btn = Button(window, text="Поломка гравитации!", command=partial(clicked, 4))
    btn.grid(column=0, row=4)
    btn = Button(window, text="В меню", command=show_menu_2)
    btn.grid(column=0, row=5)
    window.mainloop()

def show_menu():
    global window
    window = Tk()
    window.title("Stickmen ahead")
    window.geometry('1000x700')
    alive = True
    btn = Button(window, text="Тренажёрный зал!", command=clicked_gym)
    btn.grid(column=0, row=0)
    btn = Button(window, text="Режим PvP!", command=show_rooms)
    btn.grid(column=0, row=1)
    btn = Button(window, text="Управление!", command=clicked_manual)
    btn.grid(column=0, row=2)
    btn = Button(window, text="Выход!", command=quit)
    btn.grid(column=0, row=3)
    window.mainloop()

def show_manual():
    global window
    window.destroy()
    window = Tk()
    window.title("Stickmen ahead")
    window.geometry('1000x700')
    lbl = Label(window, text="Игрок 1 - стрелки на клавиатуре")
    lbl.grid(column=0, row=0)
    lbl = Label(window, text="Игрок 2 - кнопки WASD")
    lbl.grid(column=0, row=2)
    btn = Button(window, text="В меню", command=show_menu_2)
    btn.grid(column=0, row=4)
    window.mainloop()

show_menu()

