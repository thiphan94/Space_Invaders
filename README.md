# Space Invaders
Ma première version marche.
J'ai la difficulté pour multiple keyboard . Cela influence ma capacité de tuer les aliens. C'est-à-dire, je ne peux pas dépalcer mon Défender et tirer les bullets en même temps comme les games normaux. J'ai une idée de créer une liste vide is_pressed=[] quand on presse un Key ( key de direction: left and right), il est stocké dans ce liste et continuer déplacer selon direction de key, alors on peut tirer les bullets en même temps de déplacer. Quand on arrête de press key , on va supprimer (remove) key de groupe and update groupe.
