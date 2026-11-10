from random import randint
from Case import Case

class Grille() :

    def __init__(self, longueur, largeur, nbMines, ligneDepart, colonneDepart, couleur = True) :
        """
        Création d'un objet de la classe Grille.

        Args:
            longueur (int): Nombre de ligne de la grille.
            largeur (int): Nombre de colonnes de la grille.
            nbMines (int): Nombre de mines présentes dans la grille.
            ligneDepart (int): Indice de la ligne de la case à creuser pour initialiser. Pour une grille intacte, écrire -1.
            colonneDepart (int): Indice de la colonne de la case à creuser pour intialiser. Pour une grille intacte écrire -1.
            couleur (bool, optional): Affichage des couleurs lors du print. Defaults to True.

        Raises:
            Exception: Nombre de mine supérieur à ce qui est possible.
            IndexError: Case d'initialisation en dehors des bornes
        """

        if nbMines >= largeur * longueur - 9 :
            raise Exception("La grille possède trop de mines")
        
        self.longueur = longueur
        self.largeur = largeur
        self.couleur = couleur

        self.grille = [[Case(l, c, False, self.couleur) for c in range(self.largeur)] for l in range(self.longueur)]
        minesRestantes = nbMines

        if (ligneDepart, colonneDepart) == (-1, -1) :
            pass
        elif not (0 <= ligneDepart < self.longueur) or not (0 <= colonneDepart < self.largeur) :
            raise IndexError("La case de démarrage n'est pas dans la grille.")
        else :
            environ = self.voisinage(ligneDepart,colonneDepart)
            # Placement aléatoire des mines
            while minesRestantes > 0 :
                l, c = randint(0, self.longueur-1), randint(0, self.largeur-1)
                if not self[l,c].bombe and (l,c) not in environ and (l,c) != (ligneDepart, colonneDepart):
                    self[l,c].bombe = True
                    minesRestantes -= 1 

            # Actualiser les valeurs de bombes dans la grille
            self.voisinsGrille()
            self.valeurVoisins()
            # Creuser la case de départ et son voisinage
            for v in environ :
                self.creuser(v)
            self.creuser((ligneDepart, colonneDepart))
        

    def __getitem__(self, key):
        """
        Récupération de la case en fonction du type de key.
        """
        if type(key) == int :
            try :
                return self.grille[key]
            except IndexError :
                raise IndexError(f"La ligne recherchée n'existe pas : ligne d'indice {key} dans {self.largeur} lignes")
            
        elif type(key) == tuple and len(key) == 2 :
            try :
                return self.grille[key[0]][key[1]]
            except IndexError :
                raise IndexError(f"La case recherchée n'existe pas : case d'indice {key} dans {self.longueur}x{self.largeur}")

        elif type(key) == Case :
            return Case


    def __str__(self):
        ligne = "    " + "----" * self.largeur + "-\n"
        affichage = "    "
        for j in range(self.largeur) :
            affichage += f" {" "*(3-len(str(j+1))) + str(j+1)}"

        affichage += "\n" + ligne + "  1 | "
        for i in range(self.longueur) :
            for j in range(self.largeur) :
                affichage += str(self[i,j]) + " | "
            affichage += "\n" + ligne + f"{" "*(3-len(str(i+2))) + str(i+2)} | "

        return affichage[:-7]


    def voisinage(self, l, c) :
        """
        Permet de récuperer les coordonnées des cases 8-voisines de celle précisée.

        Args:
            l (int): Indice de la ligne de la case choisie.
            c (int): Indice de la colonne de la case choisie.

        Returns:
            ((int, int) list) : Liste des coordonnées des cases présentes dans le voisinage de la case sélectionnée.
        """
        # Centre
        if 0 < l < self.longueur -1 and 0 < c < self.largeur -1 :
            return [(l-1, c-1), (l-1, c), (l-1, c+1), (l, c-1), (l, c+1), (l+1, c-1), (l+1, c), (l+1, c+1)]

        # Cotes
        elif l == 0 and 0 < c < self.largeur -1 :
            return [(l, c-1), (l, c+1), (l+1, c-1), (l+1, c), (l+1, c+1)]
        elif l == self.longueur-1 and 0 < c < self.largeur -1 :
            return [(l-1, c-1), (l-1, c), (l-1, c+1), (l, c-1), (l, c+1)]
        elif 0 < l < self.longueur -1 and c == 0 :
            return [(l-1, c), (l-1, c+1), (l, c+1), (l+1, c), (l+1, c+1)]
        elif 0 < l < self.longueur -1 and c == self.largeur -1 :
            return [(l-1, c-1), (l-1, c), (l, c-1), (l+1, c-1), (l+1, c)]

        # Coins
        elif l == 0 and c == 0 :
            return [(l, c+1), (l+1, c), (l+1, c+1)]
        elif l == self.longueur -1 and c == 0 :
            return [(l-1, c), (l-1, c+1), (l, c+1)]
        elif l == 0 and c == self.largeur -1 :
            return [(l, c-1), (l+1, c-1), (l+1, c)]
        elif l == self.longueur -1 and c == self.largeur -1 :
            return [(l-1, c-1), (l-1, c), (l, c-1)]


    def voisinsCase(self, case) :
        """
        Compte le nombre de mine présentes dans le voisinage d'une case.

        Args:
            case (Case) : Case pour laquelle nous recherchons le nombre de mines autours.
        """
        voisins = self.voisinage(case.ligne, case.colonne)
        nbBombes = 0
        for v in voisins :
            if self[v].bombe :
                nbBombes += 1
        case.valeur = nbBombes


    def voisinsGrille(self) :
        """
        Calcul du nombre de mines voisines pour chaque case.
        """
        for l in self.grille :
            for case in l :
                self.voisinsCase(case)


    def valeurVoisins(self) :
        """
        Parcourt la grille pour débloquer automatiquement les cases ayant pour valeur 0 lorsqu'un voisin est creusé.
        """
        for l in self.grille :
            for case in l :
                voisins = self.voisinage(case.ligne, case.colonne)
                valeurs_0 = []
                for v in voisins :
                    if self[v].valeur == 0 :
                        valeurs_0.append(v)
                case.zeros = valeurs_0 


    def placerDrapeau(self, case) :
        """
        Place un drapeau sur la case choisie.

        Args:
            case ((int,int)): Coordonnées de la case.

        Returns:
            int : Incrémentation du nombre de drapeau disponibles.
        """
        return self[case].placerDrapeau()


    def creuser(self, case) :
        """
        Creuse la case choisie

        Args:
            case ((int, int)): Coordonnées de la case.

        Returns:
            bool : Présence d'une bombe sur la case
        """
        etat = self[case].creuser()
        if etat == True :
            return True 
        elif etat == False :
            for v in [v for v in self.voisinage(*case) if self[v].etat ==0] :
                self.creuser(v)
            return False


    def reveler(self, victoire) :
        """
        Creuse l'entierté des case restantes à la fin de la partie.

        Args:
            victoire (bool): Etat de la fin de partie.
        """
        for l in self.grille :
            for case in l :
                if case.etat == 0 and case.bombe and victoire :
                    case.etat = 1
                elif case.etat == 0 :
                    case.creuser()


if __name__ == "__main__" :

    g = Grille(5,15,60, 1,1)
    g.voisinsGrille()
    g[3,3].placerDrapeau()
    g[4,4].decouvrir()
    print(g)