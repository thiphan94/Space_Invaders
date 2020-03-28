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

    # def update(self):
    #     for bullet in self.fired_bullets:
    #         bullet.moveUp()
    #     jeu.game.after(1, self.update)

    def fire(self, canvas):
        # bullet = Bullet("up")
        # # bullet.moveUp(canvas)
        # self.fired_bullets.append(bullet)
        # print(len(self.fired_bullets))
        # self.update()
        if self.max_fired_bullets > 0:
            self.max_fired_bullets -= 1
            bullet = Bullet(str(time.time()))
            bullet.install_in(canvas)
            bullet.move_in(canvas)


class Bullet:
    def __init__(self, shooter):
        self.radius = 5
        self.color = "red"
        self.speed = 8
        self.id = None
        self.shooter = shooter

    def install_in(self, canvas):
        self.id = canvas.create_oval(415, 555, 425, 565, fill=self.color)
        # self.id = canvas.create_oval(400, 500, fill=self.color)

    def move_in(self, canvas):
        canvas.move(self.id, 0, -10)
        canvas.update()
        # time.sleep(0.1)
        #
        # canvas.delete(self.id)
        print(self.shooter)
        canvas.after(100, self.move_in, canvas)


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
        # self.bullet.install_in(self.canvas)
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

    def move_bullets(self):
        pass

    # def move_aliens_fleet(self):


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
        self.root.mainloop()


jeu = SpaceInvaders()
jeu.play()
