import tkinter as tk

# from tkinter import *
import time


class Defender:
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
        bullet = Bullet("up")
        # bullet.moveUp(canvas)
        self.fired_bullets.append(bullet)
        print(len(self.fired_bullets))
        for bullet1 in self.fired_bullets:
            bullet1.moveUp()


class Bullet:
    def __init__(self, direction):
        if direction == "up":
            self.cercle = jeu.game.canvas.create_oval(415, 555, 425, 565, fill="red")
            # self.moveUp(canvas)

    def moveUp(self):
        i = 565
        while i > 0:
            jeu.game.canvas.move(self.cercle, 0, -10)
            jeu.game.canvas.update()
            time.sleep(0.1)
            i -= 10
        if i < 0:
            jeu.game.canvas.delete(self.cercle)
            return
        # canvas.after(50, moveUp)


#
# #*********************************
class Game:
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
        if event.keysym == "Left":
            self.defender.move_in(self.canvas, "left")
        if event.keysym == "Right":
            self.defender.move_in(self.canvas, "right")
        elif event.keysym == "space":
            self.defender.fire(self.canvas)

    def start_animation(self):
        self.start()


class SpaceInvaders:
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
        if self.game.defender.fired_bullets:
            self.root.after(0.1, self.game.defender.fired_bullets[0])
        self.root.mainloop()


jeu = SpaceInvaders()
jeu.play()
