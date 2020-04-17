import time
import math
import random


try:
    import tkinter as tk
except:
    import Tkinter as tk

from tkinter import messagebox


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
        self.fired_tir = []

    def install_in(self, canvas, dx, dy):
        """Valeurs de coordonnées de alien vont changer par rapport input dx, dy à classe Fleet."""
        self.id = canvas.create_image(dx + 30, dy, image=self.pim, tags="image")

    def move_in(self, canvas):
        """Déplacer un alien en 9 pas, selon direction(1 est de gauche à droite, -1 est en revanche)."""
        canvas.move(self.id, self.direction * 10, 0)
        if self.steps == 9:
            self.direction = -self.direction
            self.steps = 0
            canvas.move(self.id, 0, 20)
        self.steps += 1
        canvas.after(500, self.move_in, canvas)

    def fire(self, canvas):
        self.update()

        tir = Bullet(canvas.coords(self.id)[0], canvas.coords(self.id)[1], "alien")
        tir.install_in(canvas)
        tir.move_down(canvas)
        self.fired_tir.append(tir)

    def update(self):
        """Tester si le bullet n'est pas encore sur écran """
        for bullet in self.fired_tir:
            if bullet.tir_out_of_sight:
                self.fired_tir.remove(bullet)


class Fleet:
    def __init__(self):
        self.aliens_lines = 5
        self.aliens_columns = 10
        self.aliens_inner_gap = 20
        self.alien_x_delta = 5
        self.alien_y_delta = 15
        self.alien_array = []
        self.dx = 0
        self.dy = 50

    def install_in(self, canvas):
        """Créer la matrice des aliens, on ajouter les aliens au list des aliens."""
        for y in range(0, 5, 1):
            for x in range(0, 10, 1):
                self.alien_array.append(Alien(canvas, self.dx, self.dy))
                self.dx += 70
            self.dx = 0
            self.dy += 70
        self.move_in(canvas)
        self.tir_of_enemies(canvas)

    def move_in(self, canvas):
        """Parcourir la boucle for pour mouvement de la matrice."""
        for alien in self.alien_array:
            alien.move_in(canvas)

    def tir_of_enemies(self, canvas):
        alien_tir = self.alien_array[random.randint(0, len(self.alien_array)) - 1]
        alien_tir.fire(canvas)
        canvas.after(1000, self.tir_of_enemies, canvas)

    def manage_touched_aliens_by(self, canvas, defender):
        """Quand la matrice des aliens touche le défender, Défender va perdu."""
        for alien in self.alien_array:
            cord = canvas.coords(alien.id)
            if cord[1] > 510:
                canvas.delete(defender)

        canvas.after(100, self.manage_touched_aliens_by, canvas, defender)


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
        """Contrôler le maximum des bullets sur écran."""
        self.update()
        if len(self.fired_bullets) < 8:
            bullet = Bullet(canvas.coords(self.id)[0], 0, "shooter")
            bullet.install_in(canvas)
            bullet.move_in(canvas)
            self.fired_bullets.append(bullet)

    def update(self):
        """Tester si le bullet n'est pas encore sur écran >> recharger maximum 8 bullets."""
        for bullet in self.fired_bullets:
            if bullet.out_of_sight:
                self.fired_bullets.remove(bullet)


class Bullet:
    def __init__(self, x, y, role):
        self.x = x
        self.radius = 5
        self.color = "red"
        self.speed = 8
        self.id = None
        self.line = None
        self.out_of_sight = False
        self.tir_out_of_sight = False
        self.y = y
        self.role = role

    def install_in(self, canvas):
        if self.role == "shooter":
            self.id = canvas.create_oval(
                self.x + self.radius,
                555,
                self.x + self.radius + 10,
                565,
                fill=self.color,
            )
        else:
            self.line = canvas.create_line(
                self.x, self.y + 20, self.x, self.y, fill="red"
            )

    def move_in(self, canvas):
        """Déplacer le bullet et le supprimer quand  bullet touche bord haut."""
        canvas.move(self.id, 0, -10)
        canvas.update()
        cord = canvas.coords(self.id)

        if cord:
            if cord[3] < 10:
                canvas.delete(self.id)
                self.out_of_sight = True
                return
            canvas.after(100, self.move_in, canvas)

    def move_down(self, canvas):
        """Déplacer le tir et le supprimer quand  tir touche bord bas."""
        canvas.move(self.line, 0, +10)
        canvas.update()
        cord = canvas.coords(self.line)
        if cord:
            if cord[3] >= 570:
                canvas.delete(self.line)
                self.tir_out_of_sight = True
                return
            canvas.after(100, self.move_down, canvas)


# #*********************************
class Game:
    def __init__(self, frame):
        width = 800
        height = 600
        self.frame = frame
        self.canvas = tk.Canvas(self.frame, width=width, height=height, bg="black")
        self.canvas.pack(side="top", fill="both", expand=True)
        self.explosion_gif = tk.PhotoImage(file="explosion.gif")
        self.defender = Defender()
        self.fleet = Fleet()
        self.explosions = []
        self.colide()
        self.colide_tir()
        # Initialisation le numéro de score = 0
        self.score = 0
        # Initialisation le numéro de "live" = 0
        self.live = 0
        # Créer Label de Score
        self.displayscore = tk.Label(
            self.frame, font=("Minecraft", 15), text="Score : {0}".format(self.score)
        )
        self.displayscore.place(x=5, y=5)

        # Créer Label de Lives
        self.displaylive = tk.Label(
            self.frame, font=("Minecraft", 15), text="Lives : {0}/3".format(self.live)
        )
        self.displaylive.place(x=700, y=5)

    def start(self):
        self.defender.install_in(self.canvas)
        self.fleet.install_in(self.canvas)
        self.fleet.manage_touched_aliens_by(self.canvas, self.defender.id)
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

    def colide(self):
        """Envisager la distance entre bullet et aliens."""
        for bullet in self.defender.fired_bullets:
            for alien in self.fleet.alien_array:
                cord = self.canvas.coords(bullet.id)
                cord_alien = self.canvas.coords(alien.id)
                if cord and cord_alien:
                    distance = math.sqrt(
                        pow((cord[0] - cord_alien[0]), 2)
                        + pow((cord[1] - cord_alien[1]), 2)
                    )
                    if distance < 40:
                        self.defender.fired_bullets.remove(bullet)
                        self.canvas.delete(bullet.id)
                        self.explosion(cord_alien[0], cord_alien[1])
                        self.fleet.alien_array.remove(alien)
                        self.canvas.delete(alien.id)
                        self.update_point(
                            50
                        )  # quand bullet de défender touche alien, on gagne 50 points
        end = time.time()
        for value in self.explosions:
            explosion, start = value
            if end - start > 0.01:
                self.explosions.remove(value)
                self.canvas.delete(explosion)
        self.canvas.after(200, self.colide)

    def explosion(self, x, y):
        """Créer image d'explosions and l'ajouter au liste des explosions."""
        exp = self.canvas.create_image(x, y, image=self.explosion_gif, tags="image")
        start = time.time()
        self.explosions.append((exp, start))

    def colide_tir(self):
        """Envisager la distance entre tirs et défender."""
        for alien in self.fleet.alien_array:
            for tir in alien.fired_tir:
                cord = self.canvas.coords(tir.line)
                cord_defender = self.canvas.coords(self.defender.id)
                if cord and cord_defender:
                    distance = math.sqrt(
                        pow((cord[0] - cord_defender[0]), 2)
                        + pow((cord[1] - cord_defender[1]), 2)
                    )
                    if distance < 30:
                        alien.fired_tir.remove(tir)
                        self.canvas.delete(tir.line)
                        self.update_live(
                            1
                        )  # quand tir de alien touche défender, on va perdre 1 'live'
                        if self.live == 3:  # si défender est tué 3 fois, il va perdre.
                            self.canvas.delete(self.defender.id)
        self.canvas.after(200, self.colide_tir)

    def update_point(self, pts):
        """Méthode pour mettre à jour les points de défender"""
        self.score += pts
        self.displayscore.config(
            font=("Minecraft", 15), text="Score : {0}".format(self.score)
        )

    def update_live(self, pts):
        """Méthode pour mettre à jour les "lives" de défender"""
        self.live += pts
        self.displaylive.config(
            font=("Minecraft", 15), text="Lives : {0}/3".format(self.live)
        )


class SpaceInvaders:
    """ Main Game class."""

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
