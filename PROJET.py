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
        self.displace = 0

    def install_in(self, canvas):
        lx = 400 + self.width / 2
        ly = 600 - self.height - 10
        self.id = canvas.create_rectangle(
            lx, ly, lx + self.width, ly + self.height, fill="white"
        )

    def move_in(self, canvas, direction):
        if direction == "left":
            if self.displace >= -400:
                self.displace -= 10
                canvas.move(self.id, -10, 0)
                canvas.update()
                time.sleep(0.01)
        if direction == "right":
            if self.displace <= 360:
                self.displace += 10
                canvas.move(self.id, 10, 0)
                canvas.update()
                time.sleep(0.01)

    def fire(self, canvas):
        Bullet(canvas, "up")


class Bullet(object):
    def __init__(self, canvas, direction):
        if direction == "up":
            self.cercle = canvas.create_oval(415, 555, 425, 565, fill="red")
            self.moveUp(canvas)

    def moveUp(self, canvas):
        # for i in range(10, 500):
        #     canvas.move(self.cercle, 0, i)
        #     x = canvas.coords(self.cercle)
        #     if x[1] < 0:
        #         canvas.delete(self.cercle)
        #         return
        i = 565
        while i > 0:
            canvas.move(self.cercle, 0, -10)
            canvas.update()
            time.sleep(0.1)
            i -= 10


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
        # self.defender.fire(self.canvas)
        self.frame.winfo_toplevel().bind("<Key>", self.keypress)

    def keypress(self, event):
        x = 0
        if event.keysym == "Left":
            self.defender.move_in(self.canvas, "left")
        if event.keysym == "Right":
            self.defender.move_in(self.canvas, "right")
        elif event.keysym == "space":
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
