import tkinter as tk
import time
import math


class Alien:
    def __init__(self, canvas, dx, dy):
        self.id = None
        self.alive = True
        self.pim = tk.PhotoImage(file="alien.gif")
        self.steps = 0
        self.direction = 1
        self.dx = dx
        self.dy = dy
        self.install_in(canvas, dx, dy)

    def touched_by(self, canvas, projectile):
        pass

    def install_in(self, canvas, dx, dy):

        self.id = canvas.create_image(
            self.dx + 50, self.dy, image=self.pim, tags="image"
        )
        # self.move_in(canvas)

    def move_in(self, canvas):
        # canvas.move(self.id, self.direction * 10, 0)

        if self.steps == 24:
            self.direction = -self.direction
            self.steps = 0
            # canvas.move(self.id, 0, 20)
        self.steps += 1
        canvas.after(200, self.move_in, canvas)


class Fleet:
    def __init__(self):
        self.aliens_lines = 5
        self.aliens_columns = 10
        self.aliens_inner_gap = 20
        self.alien_x_delta = 5
        self.alien_y_delta = 15
        # fleet_size =
        self.aliens_lines * self.aliens_columns
        # self.aliens_fleet = [None] * fleet_size
        self.alien_array = []
        self.dx = 0
        self.dy = 50

    def install_in(self, canvas):
        for y in range(0, 5, 1):
            for x in range(0, 10, 1):
                self.alien_array.append(Alien(canvas, self.dx, self.dy))
                self.dx += 50
            self.dx = 0
            self.dy += 50
        self.move_in(canvas)

    def move_in(self, canvas):
        for alien in self.alien_array:
            alien.move_in(canvas)
        #     if canvas.coords(alien)[1] > 10:
        #         canvas.delete(self.alien_array)
        # canvas.after(100, self.move_in, canvas)

    def manage_touched_aliens_by(self, canvas, defender):
        pass


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
        self.update()

        if len(self.fired_bullets) < 8:
            bullet = Bullet(canvas.coords(self.id)[0], 0, "shooter")
            bullet.install_in(canvas)
            bullet.move_in(canvas)
            self.fired_bullets.append(bullet)

    def update(self):
        for bullet in self.fired_bullets:
            if bullet.out_of_sight == True:
                self.fired_bullets.remove(bullet)
                # pass


class Bullet:
    def __init__(self, x, y, shooter):
        self.x = x
        self.radius = 5
        self.color = "red"
        self.speed = 8
        self.id = None
        self.shooter = shooter
        self.out_of_sight = False
        self.y = y

    def install_in(self, canvas):
        self.id = canvas.create_oval(
            self.x + self.radius, 555, self.x + self.radius + 10, 565, fill=self.color
        )

    def move_in(self, canvas):
        canvas.move(self.id, 0, -10)
        canvas.update()
        cord = canvas.coords(self.id)

        if cord:
            if cord[3] < 10:
                canvas.delete(self.id)
                self.out_of_sight = True
                return
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
        self.fleet = Fleet()
        self.colide()

    def start(self):
        self.defender.install_in(self.canvas)
        self.fleet.install_in(self.canvas)
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

    def colide(self):
        for alien in self.fleet.alien_array:
            for bullet in self.defender.fired_bullets:
                cord = self.canvas.coords(bullet.id)
                if cord:
                    print(cord)
                    print(len(self.defender.fired_bullets))
                    print(cord[1])
                    distance = math.sqrt(
                        pow((cord[0] - alien.dx), 2) + pow((cord[1] - alien.dy), 2)
                    )
                    # print(cord[1])
                    print("d", distance)
                    if distance < 40:
                        self.defender.fired_bullets.remove(bullet)
                        self.canvas.delete(bullet.id)

        self.canvas.after(200, self.colide)


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
