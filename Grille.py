from random import randint
from Case import Case

class Grille() :

    def __init__(self, longueur, largeur, nbMines, ligne_depart, colonne_depart) :
        if nbMines >= largeur * longueur - 9 :
            raise Exception("La grille possède trop de mines")
        self.long = longueur
        self.larg = largeur
        self.mines = nbMines

        self.grille = [[Case(l, c, False) for c in range(largeur)] for l in range(longueur)]
        minesRestantes = nbMines

        environ = self.voisinage(ligne_depart,colonne_depart)
        while minesRestantes > 0 :
            l, c = randint(0, longueur-1), randint(0, largeur-1)
            if not self[l,c].bombe and (l,c) not in environ and (l,c) != (ligne_depart, colonne_depart):
                self[l,c].bombe = True
                minesRestantes -= 1 

        self.voisinsGrille()
        self.valeurVoisins()
        for v in environ :
            self.creuser(v)
        self.creuser((ligne_depart, colonne_depart))



    def __getitem__(self, key):
        if type(key) == int :
            try :
                return self.grille[key]
            except IndexError :
                raise IndexError(f"La ligne recherchée n'existe pas : ligne d'indice {key} dans {self.larg} lignes")
            
        elif type(key) == tuple and len(key) == 2 :
            try :
                return self.grille[key[0]][key[1]]
            except IndexError :
                raise IndexError(f"La case recherchée n'existe pas : case d'indice {key} dans {self.long}x{self.larg}")

        elif type(key) == Case :
            return Case


    def __str__(self):
        ligne = "    " + "----" * self.larg + "-\n"
        affichage = "    "
        for j in range(self.larg) :
            affichage += f" {" "*(3-len(str(j+1))) + str(j+1)}"

        affichage += "\n" + ligne + "  1 | "
        for i in range(self.long) :
            for j in range(self.larg) :
                affichage += str(self[i,j]) + " | "
            affichage += "\n" + ligne + f"{" "*(3-len(str(i+2))) + str(i+2)} | "

        return affichage[:-7]


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

    def valeurVoisins(self) :
        for l in self.grille :
            for case in l :
                voisins = self.voisinage(case.ligne, case.colonne)
                valeurs_0 = []
                for v in voisins :
                    if self[v].valeur == 0 :
                        valeurs_0.append(v)
                case.zeros = valeurs_0 

    def placerDrapeau(self, case) :
        return self[case].placerDrapeau()

    def creuser(self, case) :
        etat = self[case].creuser()
        if etat == True :
            return True 
        elif etat == False :
            for v in [v for v in self.voisinage(*case) if self[v].etat ==0] :
                self.creuser(v)

    def reveler(self) :
        for l in self.grille :
            for case in l :
                if case.etat == 0 :
                    case.creuser()


if __name__ == "__main__" :

    g = Grille(5,15,60, 1,1)
    g.voisinsGrille()
    g[3,3].placerDrapeau()
    g[4,4].decouvrir()
    print(g)