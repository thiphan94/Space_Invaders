import json


class Score(object):
    def __init__(self, nom, points):
        self.nom = nom
        self.points = points

    def toFile(self, fich):
        f = open(fich, "w")
        l = self
        json.dump(l.__dict__, f)
        f.close()

    @classmethod
    def fromFile(cls, fich):
        f = open(fich, "r")
        d = json.load(f)
        lnew = Score(d["nom"], d["points"])
        f.close()
        return lnew

    def __str__(self):
        return "[" + self.nom + "," + str(self.points) + "]"


Player = Score("Pierre", 2500)
Player.toFile("player.json")
print(Player)
l = Score.fromFile("player.json")
print(l)
l.points = 2020
l.toFile("player.json")
print(l)


class Resultat(object):
    def __init__(self):
        self.players = []

    def ajout(self, player):
        self.players.append(player)

    def __str__(self):
        chaine = str(self.players[0])
        for e in self.players[1:]:
            chaine = chaine + "," + str(e)
        return chaine

    @classmethod
    def fromFile(cls, fich):
        f = open(fich, "r")
        # chargement
        tmp = json.load(f)

        liste = []
        for d in tmp:
            # créer un score de player
            l = Score(d["nom"], d["points"])
            # l'ajouter dans la liste
            liste.append(l)
        lib = Resultat()
        lib.players = liste
        f.close()
        return lib

    def toFile(self, fich):
        f = open(fich, "w")
        tmp = []
        for l in self.players:
            # créer un dictionnaire
            d = {}
            d["nom"] = l.nom
            d["points"] = l.points
            tmp.append(d)
        json.dump(tmp, f)
        f.close()


libN = Resultat.fromFile("players.json")
print(libN)
new = Score("Xavier", 9999)
libN.ajout(new)
libN.toFile("playersBis.json")
libN2 = Resultat.fromFile("playersBis.json")
print(libN2)
