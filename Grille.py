from random import randint
from Case import Case

class Grille() :

    def __init__(self, longueur, largeur, nbMines) :
        self.long = longueur
        self.larg = largeur
        self.mines = nbMines

        self.grille = [[Case(l, c, False) for c in range(largeur)] for l in range(longueur)]
        minesRestantes = nbMines

        while minesRestantes > 0 :
            l, c = randint(0, longueur-1), randint(0, largeur-1)
            if not self[l,c].bombe :
                self[l,c].bombe = True
                minesRestantes -= 1 


    def __getitem__(self, key):
        if type(key) == int :
            try :
                return self.grille[key]
            except IndexError :
                print(f"ERREUR : La ligne recherchée n'existe pas : ligne d'indice {key} dans {self.larg} lignes")
            
        elif type(key) == tuple and len(key) == 2 :
            try :
                return self.grille[key[0]][key[1]]
            except IndexError :
                print(f"ERREUR : La case recherchée n'existe pas : case d'indice {key} dans {self.long}x{self.larg}")


    def __str__(self):
        ligne = " " + "----" * self.larg + "-\n"
        affichage = ligne + " | "
        for l in self.grille :
            for case in l :
                affichage += str(case) + " | "
            affichage += "\n" + ligne + " | "
        return affichage[:-2]


    def voisinage(self, l, c) :
        # Centre
        if 0 < l < self.long -1 and 0 < c < self.larg -1 :
            return [(l-1, c-1), (l-1, c), (l-1, c+1), (l, c-1), (l, c+1), (l+1, c-1), (l+1, c), (l+1, c+1)]

        # Cotes
        elif l == 0 and 0 < c < self.larg -1 :
            return [(l, c-1), (l, c+1), (l+1, c-1), (l+1, c), (l+1, c+1)]
        elif l == self.long-1 and 0 < c < self.larg -1 :
            return [(l-1, c-1), (l-1, c), (l-1, c+1), (l, c-1), (l, c+1)]
        elif 0 < l < self.long -1 and c == 0 :
            return [(l-1, c), (l-1, c+1), (l, c+1), (l+1, c), (l+1, c+1)]
        elif 0 < l < self.long -1 and c == self.larg -1 :
            return [(l-1, c-1), (l-1, c), (l, c-1), (l+1, c-1), (l+1, c)]

        # Coins
        elif l == 0 and c == 0 :
            return [(l, c+1), (l+1, c), (l+1, c+1)]
        elif l == self.long -1 and c == 0 :
            return [(l-1, c), (l-1, c+1), (l, c+1)]
        elif l == 0 and c == self.larg -1 :
            return [(l, c-1), (l+1, c-1), (l+1, c)]
        elif l == self.long -1 and c == self.larg -1 :
            return [(l-1, c-1), (l-1, c), (l, c-1)]


    def voisinsCase(self, case) :
        voisins = self.voisinage(case.ligne, case.colonne)
        nbBombes = 0
        for v in voisins :
            if self[v].bombe :
                nbBombes += 1
        case.valeur = nbBombes


    def voisinsGrille(self) :
        for l in self.grille :
            for case in l :
                self.voisinsCase(case)

if __name__ == "__main__" :

    g = Grille(5,15,60)
    g.voisinsGrille()
    g[3,3].placerDrapeau()
    g[4,4].decouvrir()
    print(g)