"""Space Invaders Game."""

import time
import math
import random
import json
import operator

try:
    import tkinter as tk
except ImportError:
    import Tkinter as tk


class Alien:
    """Class pour créer un alien."""

    def __init__(self, canvas, dx, dy, nb):
        """Image d'alien et les attributes pour déplacer un alien."""
        self.id = None
        self.pim = tk.PhotoImage(file="alien.gif")
        self.pim2 = tk.PhotoImage(file="alien2.gif")
        self.steps = 0
        self.direction = 1
        self.dx = dx
        self.dy = dy
        self.nb = nb
        self.install_in(canvas, dx, dy, nb)

    def install_in(self, canvas, dx, dy, nb):
        """Valeurs de coordonnées de alien vont changer par rapport input dx, dy à classe Fleet."""
        if nb > 19:
            self.id = canvas.create_image(dx + 30, dy, image=self.pim, tags="image")
        else:
            self.id = canvas.create_image(dx + 30, dy, image=self.pim2, tags="image")

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
        """Méthode pour tirer un tir d'alien."""
        coord = canvas.coords(self.id)
        if coord:
            tir = Bullet(coord[0], coord[1], "alien")
            tir.install_in(canvas)
            tir.move_in(canvas, "alien")
            return tir
        return None


class Fleet:
    """Class pour créer une matrice des aliens."""

    def __init__(self):
        """Mettre des attributes pour déplacer la matrice."""
        self.aliens_lines = 5
        self.aliens_columns = 10
        self.alien_array = []
        self.dx = 0
        self.dy = 50
        self.fired_tir = []
        self.nb = 0

    def install_in(self, canvas):
        """Créer la matrice des aliens, on ajouter les aliens au list des aliens."""
        for _ in range(self.aliens_lines):
            for _ in range(self.aliens_columns):
                self.alien_array.append(Alien(canvas, self.dx, self.dy, self.nb))
                self.dx += 70
                self.nb += 1
            self.dx = 0
            self.dy += 70
        self.move_in(canvas)
        if self.alien_array:
            self.tir_of_enemies(canvas)

    def move_in(self, canvas):
        """Parcourir la boucle for pour mouvement de la matrice."""
        for alien in self.alien_array:
            alien.move_in(canvas)

    def tir_of_enemies(self, canvas):
        """Choissir random un alien dans matrice pour tirer."""
        self.update()
        if self.alien_array:
            alien_tir = self.alien_array[random.randint(0, len(self.alien_array)) - 1]
            tir = alien_tir.fire(canvas)
            if tir:
                self.fired_tir.append(tir)
        canvas.after(1000, self.tir_of_enemies, canvas)

    def update(self):
        """Tester si le tir n'est pas encore sur écran."""
        for tir in self.fired_tir:
            if tir.out_of_sight:
                self.fired_tir.remove(tir)


class Defender:
    """Class pour définir un défender."""

    def __init__(self):
        """Méthode pour définir des attributes."""
        self.width = 20
        self.height = 20
        self.id = None
        self.max_fired_bullets = 8
        self.fired_bullets = []
        self.displace = 0
        self.left = False
        self.right = False

    def install_in(self, canvas):
        """Création de défender."""
        lx = 400 + self.width / 2
        ly = 600 - self.height - 10
        self.id = canvas.create_rectangle(
            lx, ly, lx + self.width, ly + self.height, fill="white"
        )

    def move_in(self, canvas):
        """Mouvement de défender."""
        if self.left:
            if self.displace >= -400:
                self.displace -= 10
                canvas.move(self.id, -10, 0)
                canvas.update()
                time.sleep(0.01)
        if self.right:
            if self.displace <= 360:
                self.displace += 10
                canvas.move(self.id, 10, 0)
                canvas.update()
                time.sleep(0.01)

        canvas.after(100, self.move_in, canvas)

    def fire(self, canvas):
        """Contrôler le maximum des bullets sur écran."""
        self.update()
        coord = canvas.coords(self.id)
        if len(self.fired_bullets) < self.max_fired_bullets and coord:
            bullet = Bullet(canvas.coords(self.id)[0], 0, "shooter")
            bullet.install_in(canvas)
            bullet.move_in(canvas, "defender")
            self.fired_bullets.append(bullet)

    def update(self):
        """Tester si le bullet n'est pas encore sur écran >> recharger maximum 8 bullets."""
        for bullet in self.fired_bullets:
            if bullet.out_of_sight:
                self.fired_bullets.remove(bullet)


class Bullet:
    """Class pour créer bullet de défender et tirs des aliens."""

    def __init__(self, x, y, role):
        """Des attributes pour créer des bullets et des tirs."""
        self.x = x
        self.radius = 5
        self.color = "red"
        self.speed = 10
        self.id = None
        self.out_of_sight = False
        self.y = y
        self.role = role

    def install_in(self, canvas):
        """Création des bullets et des tirs."""
        if self.role == "shooter":
            self.id = canvas.create_oval(
                self.x + self.radius,
                555,
                self.x + self.radius + 10,
                565,
                fill=self.color,
            )
        elif self.role == "alien":
            self.id = canvas.create_line(
                self.x, self.y + 20, self.x, self.y, fill=self.color
            )

    def move_in(self, canvas, command):
        """Déplacer le bullet et le tir et le supprimer quand ils ne sont pas sur écran."""
        if command == "defender":
            canvas.move(self.id, 0, -self.speed)
        elif command == "alien":
            canvas.move(self.id, 0, +self.speed)
        canvas.update()
        coord = canvas.coords(self.id)
        if coord:
            if coord[3] < 10 or coord[3] >= 570:
                canvas.delete(self.id)
                self.out_of_sight = True
                return
            canvas.after(100, self.move_in, canvas, command)


class Bunker:
    """Class pour créer un bunker de défender."""

    def __init__(self, canvas, dx, dy):
        """création un bunker."""
        self.dx = dx
        self.dy = dy
        self.id = None
        self.install_in(canvas, dx, dy)

    def install_in(self, canvas, dx, dy):
        """Créer id d'un bunker."""
        self.id = canvas.create_rectangle(
            dx, dy, dx + 20, dy + 20, outline="purple", fill="grey",
        )


class Bunkers:
    """Class pour créer les bunkers de défender."""

    cpt = 0  # compteur de nombre de petit bunker dans bunkers dans game, initialisation = 0
    cpt_row = 0

    def __init__(self):
        """création liste des bunkers au début."""
        self.compteur = Bunkers.cpt
        self.dx = 70
        self.dy = 490
        self.bunkers_array = []

    def install_in(self, canvas):
        """Créer la matrice des aliens, on ajouter les aliens au list des aliens."""
        while self.dy <= 530:
            while self.dx <= 750:
                self.bunkers_array.append(Bunker(canvas, self.dx, self.dy))
                self.dx += 20
                self.compteur += 1
                if self.compteur == 3:
                    self.dx += 140
                    self.compteur = 0
            self.dx = 70
            self.dy += 20


class Score:
    """Class pour stocker nom + score de joueur."""

    def __init__(self, nom, points, temps):
        """Deux attributes de Class."""
        self.nom = nom
        self.points = points
        self.temps = temps

    def toFile(self, fich):
        """Mode de écrire au fichier."""
        f = open(fich, "w")
        l = self
        json.dump(l.__dict__, f)
        f.close()

    @classmethod
    def fromFile(cls, fich):
        """Mode de lecture à partir de fichier."""
        f = open(fich, "r")
        d = json.load(f)
        lnew = Score(d["nom"], d["points"], d["temps"])
        f.close()
        return lnew

    def __str__(self):
        """Affichage de résultat."""
        return "[" + self.nom + "," + str(self.points) + "," + str(self.temps) + "]"


class Resultat:
    """Class pour stocker plusieurs noms + scores des playeurs."""

    def __init__(self):
        """Créer liste des playeurs."""
        self.players = []

    def ajout(self, player):
        """Méthode pour ajouter un nouveau player."""
        self.players.append(player)

    def __str__(self):
        """Affichage le dictionnaire au string."""
        self.players.sort(key=operator.attrgetter("points"), reverse=True)
        chaine = str(self.players[0])
        for i in self.players[1:9]:
            # pour afficher high score mais pas beaucoup , que 9 personnes
            chaine = chaine + "\n" + str(i)
        return chaine

    @classmethod
    def fromFile(cls, fich):
        """Mode de lecture à partir un fichier."""
        f = open(fich, "r")
        # chargement
        tmp = json.load(f)
        liste = []
        for d in tmp:
            # créer un joueur
            l = Score(d["nom"], d["points"], d["temps"])
            # l'ajouter dans la liste
            liste.append(l)
        lib = Resultat()
        lib.players = liste
        f.close()
        return lib

    def toFile(self, fich):
        """Mode d'écrire au fichier."""
        f = open(fich, "w")
        tmp = []
        for l in self.players:
            # créer un dictionnaire
            d = {}
            d["nom"] = l.nom
            d["points"] = l.points
            d["temps"] = l.temps
            tmp.append(d)
        json.dump(tmp, f)
        f.close()


# #****************************************************************
class Game:
    """Class pour mettre en lien tous les autres class."""

    def __init__(self, frame):
        """Définir les bases de game et appeler les autres méthodes."""
        width = 800
        height = 600
        self.frame = frame
        self.canvas = tk.Canvas(self.frame, width=width, height=height, bg="black")
        self.canvas.pack(side="top", fill="both", expand=True)
        self.explosion_gif = tk.PhotoImage(file="explosion.gif")
        self.photo = tk.PhotoImage(file="gameover.gif")
        self.ecran = tk.PhotoImage(file="bk.gif")
        self.defender = Defender()
        self.fleet = Fleet()
        self.bunker = Bunkers()
        self.explosions = []
        self.collide("bullet", "alien")
        self.collide("bullet", "bunker")
        self.collide("tir", "bunker")
        self.collide("tir", "defender")
        self.manage_touched_aliens_by()

        # Initialisation le numéro de score = 0
        self.score = 0
        # Initialisation le numéro de "live" = 0
        self.live = 3
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
        # Créer Label de Temps
        self.time = tk.Label(self.frame, font=("Minecraft", 15), text="Time:")
        self.time.place(x=250, y=5)
        # Créer Label d'un montre
        self.sec = 0
        self.displaytime = tk.Label(text="", font=("Helvetica", 15), fg="black")
        self.displaytime.place(x=300, y=5)
        # Variable pour prendre le temps de player
        self.get_playtime = None
        self.update_clock()

    def start(self):
        """Commencer à créer défender, aliens, bunkers."""
        self.canvas.create_image(0, 0, image=self.ecran, tags="image", anchor="nw")
        self.defender.install_in(self.canvas)
        self.defender.move_in(self.canvas)
        self.fleet.install_in(self.canvas)
        self.bunker.install_in(self.canvas)
        self.frame.winfo_toplevel().bind("<Key>", self.keypress)
        self.frame.winfo_toplevel().bind(
            "<KeyRelease>", self.keyrelease
        )  # résoudre "Binding keys to keyboard events"

    def keypress(self, event):
        """Méthode pour mettre en lien les keyboards et défender."""
        if event.keysym == "Left":
            self.defender.left = True
        if event.keysym == "Right":
            self.defender.right = True
        elif event.keysym == "space":
            self.defender.fire(self.canvas)

    def keyrelease(self, event):
        """Méthode pour mettre en lien les keyboards et défendeur (button libre, pas pressée)."""
        if event.keysym == "Left":
            self.defender.left = False
        if event.keysym == "Right":
            self.defender.right = False

    def start_animation(self):
        """Appeler la création des bases au méthode start()."""
        self.start()

    def update_clock(self):
        """Mettre à jour le temps."""
        self.sec = self.sec + 1
        self.displaytime.configure(text=self.sec)
        self.canvas.after(1000, self.update_clock)

    @staticmethod
    def calculate_distance(coord1, coord2):
        """Caluler la distance entre deux points."""
        distance = math.sqrt(
            (coord1[0] - coord2[0]) ** 2 + (coord1[1] - coord2[1]) ** 2
        )
        return distance

    def collide(self, object1, object2):
        """Envisager la collision entre object1 et object2."""
        if object2 == "alien":
            array2 = self.fleet.alien_array
        elif object2 == "bunker":
            array2 = self.bunker.bunkers_array
        elif object2 == "defender":
            array2 = [self.defender]
        if object1 == "bullet":
            array1 = self.defender.fired_bullets
        elif object1 == "tir":
            array1 = self.fleet.fired_tir
        for o1 in array1:
            for o2 in array2:
                coord1 = self.canvas.coords(o1.id)
                coord2 = self.canvas.coords(o2.id)
                if coord1 and coord2:
                    distance = self.calculate_distance(coord1, coord2)
                    if distance < 40:
                        array1.remove(o1)
                        self.canvas.delete(o1.id)
                        if object2 == "alien":
                            self.explosion(coord2[0], coord2[1])
                            array2.remove(o2)
                            self.canvas.delete(o2.id)
                            self.check()
                            if o2.nb <= 19:
                                self.update_point(
                                    100
                                )  # quand bullet de défender touche alien (big boss), on gagne 100 points
                            else:
                                self.update_point(
                                    50
                                )  # quand bullet de défender touche alien, on gagne 50 points
                        elif object2 == "defender":
                            self.update_live(
                                1
                            )  # quand tir de alien touche défender, on va perdre 1 'live'
                            if self.live == 0:
                                # quand joueur mort , on appelle méthode end_game
                                self.end_game("over")
                        elif object2 == "bunker":
                            array2.remove(o2)
                            self.canvas.delete(o2.id)
        if object2 == "alien":
            end = time.time()
            for value in self.explosions:
                explosion, start = value
                if end - start > 0.01:
                    self.explosions.remove(value)
                    self.canvas.delete(explosion)
        self.canvas.after(500, self.collide, object1, object2)

    def explosion(self, x, y):
        """Créer image d'explosions and l'ajouter au liste des explosions."""
        exp = self.canvas.create_image(x, y, image=self.explosion_gif, tags="image")
        start = time.time()
        self.explosions.append((exp, start))

    def update_point(self, pts):
        """Méthode pour mettre à jour les points de défender."""
        self.score += pts
        self.displayscore.config(
            font=("Minecraft", 15), text="Score : {0}".format(self.score)
        )

    def update_live(self, pts):
        """Méthode pour mettre à jour les "lives" de défender."""
        self.live -= pts
        self.displaylive.config(
            font=("Minecraft", 15), text="Lives : {0}/3".format(self.live)
        )

    def manage_touched_aliens_by(self):
        """Quand la matrice des aliens touche le défender, Défender va perdu."""
        for alien in self.fleet.alien_array:
            coord = self.canvas.coords(alien.id)
            if coord:
                if coord[1] > 510:
                    self.end_game("over")
        self.canvas.after(100, self.manage_touched_aliens_by)

    def get_name(self):
        """Méthode pour prendre valeur de joueur pour écrire au fichier."""
        label1 = tk.Label(self.frame, text="Type your Name:")
        label1.config(font=("helvetica", 14))
        self.canvas.create_window(400, 120, window=label1)

        entry1 = tk.Entry(self.frame)
        self.canvas.create_window(400, 170, window=entry1)

        def print_score():
            nom = entry1.get()
            abc = Score(nom, self.score, self.get_playtime)
            abc.toFile("player.json")
            libN = Resultat.fromFile("players.json")
            libN.ajout(abc)
            libN.toFile("players.json")
            libN2 = Resultat.fromFile("players.json")

            label3 = tk.Label(
                self.frame, text="Player with score and time: " + abc.__str__()
            )
            label3.config(font=("helvetica", 15))
            self.canvas.create_window(400, 250, window=label3)

            label4 = tk.Label(self.frame, text="HIGH SCORE:")
            label4.config(font=("helvetica", 16))
            self.canvas.create_window(400, 370, window=label4)

            label5 = tk.Label(self.frame, text=libN2.__str__())
            label5.config(font=("helvetica", 10))
            self.canvas.create_window(400, 500, window=label5)

        button1 = tk.Button(
            text="Score",
            command=print_score,
            bg="brown",
            fg="white",
            font=("helvetica", 13, "bold"),
        )
        self.canvas.create_window(400, 200, window=button1)

    def end_game(self, command):
        """Méthode pour delete all quand le joueur est mort ou gagné."""
        self.get_playtime = self.sec  # prendre le temps quand défendeur est mort
        self.canvas.delete(self.defender.id)
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, image=self.photo, tags="image", anchor="nw")
        if command == "over":
            self.canvas.create_text(
                400, 300, font=("MS Serif", 30), text="You died !", fill="red",
            )
        elif command == "win":
            self.canvas.create_text(
                400, 300, font=("MS Serif", 30), text="You win !", fill="red",
            )
        self.get_name()

    def check(self):
        """Méthode pour vérifier si les aliens sont tous tués."""
        if not self.fleet.alien_array:
            self.end_game("win")


class SpaceInvaders:
    """Main Game class."""

    def __init__(self):
        """Création frame et titre du jeu."""
        self.root = tk.Tk()
        self.root.title("Space Invaders")
        width = 800
        height = 600
        self.root.geometry(
            "800x600+500+50"
        )  # quand je run code avec Powershell, l'écran de game va être à droit
        # plus facile pour fix bug = print les erreurs quand jouer en même temps
        self.frame = tk.Frame(self.root, width=width, height=height, bg="green")
        self.frame.pack()
        self.game = Game(self.frame)

    def play(self):
        """Méthode pour commmencer le jeu."""
        self.game.start_animation()
        self.root.mainloop()


jeu = SpaceInvaders()
jeu.play()
