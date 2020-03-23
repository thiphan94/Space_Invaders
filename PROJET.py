import tkinter as tk
from tkinter import *
import time
import threading
import random
from tkinter import messagebox


class Defender(object):
    def __init__(self):
        self.width = 20
        self.height = 20
        self.move_delta = 20
        self.id = None
        self.max_fired_bullets = 8
        self.fired_bullets = []

    def install_in(self, canvas):
        lx = 400 + self.width / 2
        ly = 600 - self.height - 10
        self.id = canvas.create_rectangle(
            lx, ly, lx + self.width, ly + self.height, fill="white"
        )

    def move_in(self, canvas, dx):
        canvas.move(self.id, dx, 0)

    def fire(self, canvas):
        Bullet(canvas, "up")


class Bullet(object):
    def __init__(self, canvas, direction):
        if direction == "up":
            self.line = canvas.create_oval(415, 565, 425, 570, fill="red")
        # 			self.moveUp()
        # else:
        #     self.line = canvas.create_line(self.x, y + 20, self.x, y, fill="red")


# 			self.moveDown()


#
# #*********************************
class Game(object):
    def __init__(self, frame):
        width = 800
        height = 600
        self.frame = frame
        self.canvas = tk.Canvas(self.frame, width=width, height=height, bg="black")
        self.canvas.pack(side="top", fill="both", expand=True)
        self.defender = Defender()

    def start(self):
        self.defender.install_in(self.canvas)
        self.defender.fire(self.canvas)
        self.frame.winfo_toplevel().bind("<Key>", self.keypress)

    def keypress(self, event):
        x = 0
        if event.keysym == "Left":
            x = -30
            self.defender.move_in(self.canvas, x)
        if event.keysym == "Right":
            x = 30
            self.defender.move_in(self.canvas, x)
        elif event.keysym == "Return":
            self.defender.fire(self.canvas)

    def start_animation(self):
        self.start()


class SpaceInvaders(object):
    """ Main Game class """

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Space Invaders")
        width = 800
        height = 600
        self.frame = tk.Frame(self.root, width=width, height=height, bg="green")
        self.frame.pack()
        self.game = Game(self.frame)

    def play(self):
        self.game.start_animation()
        self.root.mainloop()


jeu = SpaceInvaders()
jeu.play()
