from Grille import Grille

class Demineur() :
    def __init__(self, longueur = -1, largeur = -1, nbMines = -1, couleur=True):
        """
        Crée un objet de la classe Demineur.

        Args:
            longueur (int, optional): Nombre de ligne de la grille du démineur. -1 pour poser la question au joueur à l'initialisation.
            largeur (int, optional): Nombre de colonne de la grille du démineur. -1 pour poser la question au joueur à l'initialisation.
            nbMines (int, optional): Nombre de mines dans la grille du démineur. -1 pour poser la question au joueur à l'initialisation.
            couleur (bool, optional): Affichage des couleurs lors du print. Defaults to True.
        """
        self.longueur = longueur
        self.largeur = largeur
        self.nbMines = nbMines
        self.perdu = False
        self.nbDrapeau = nbMines
        self.couleur = couleur
        

        if self.longueur == -1 :
            self.longueur = int(input("Quelle longueur de grille ? \n\t"))
        if self.largeur == -1 :
            self.largeur = int(input("Quelle largeur de grille ? \n\t"))
        if self.nbMines == -1 :
            self.nbMines = int(input("Combien de mines présentes dans la grille ? \n\t"))

        self.caseCachees = self.longueur * self.largeur

        self.grille = Grille(self.longueur, self.largeur, 0, -1, -1, self.couleur)


    def question(self, premier = False) :
        """
        Demande l'action à réaliser jusqu'à obtenir une réponse valide.

        Args:
            premier (bool, optional): Est ce l'initialisation de la partie. Defaults to False.

        Returns:
            (string, int, int): Action, ligne, colonne.
        """
        reponse = input(f"Que souhaites tu faire ? (Action Ligne Colonne)   -   {self.nbDrapeau} drapeaux restants   -   {self.caseCachees} cases restantes\n\t").split()
        while self.testReponse(reponse, premier) :
            reponse = input(f"Je n'ai pas compris ton action, que souhaites tu faire ? (Action Ligne Colonne)   -   {self.nbDrapeau} drapeaux restants\n\t").split()

        return reponse
            

    def testReponse(self, reponse, premier) : 
        """
        Vérifie que la réponse est correcte.

        Args:
            reponse (string list): Action écrite par l'utilisateur.
            premier (bool): Est ce l'initialisation de la partie.

        Returns:
            bool: Validité de la réponse.
        """
        # Vérification du type des réponses
        try :
            reponse[1] = int(reponse[1]) - 1
            reponse[2] = int(reponse[2]) - 1
        except ValueError :
            print("Les coordonnées doivent êtres exprimées en chiffres.")
        except IndexError :
            print("La réponse doit posséder 3 composants : l'action, la ligne et la colonne.")
        else :
            
            if reponse[0] not in ["C", "c", "D", "d"] :
                print("L'action n'est pas valide.")
            elif premier and reponse[0] not in ["C", "c"] :
                print("Tu es obligé de creuser pour le premier coup.")
            elif reponse[1] < 0 or reponse[1] >= self.longueur or reponse[2] < 0 or reponse[2] >= self.largeur :
                print("L'action est en dehors des bornes.")
            elif premier :
                return False
            elif self.grille[reponse[1], reponse[2]].etat == -1 :
                print("La case est déjà creusée.")
            elif self.grille[reponse[1], reponse[2]].etat == 1 and reponse[0] in ["C", "c"] :
                print("Pour creuser la case, il faut avant tout enlever le drapeau.")
            else :
                return False
        return True


    def casesRestantes(self) :
        """
        Comptage du nombre de cases non découvertes et sans drapeau.
        """
        compteurCasesRestantes = 0
        for l in range(self.longueur) :
            for c in range(self.largeur) :
                if self.grille[l,c].etat == 0 :
                    compteurCasesRestantes += 1
        self.caseCachees = compteurCasesRestantes


    def fin(self) :
        """
        Vérification des conditions de victoire :
            - Le jouer a révélé une mine
            - Il reste autant de mine que de drapeau

        Returns:
            bool : Fin de la partie.
        """
        return self.perdu or self.caseCachees == self.nbDrapeau


    def creuser(self, ligne, colonne) :
        """
        Creuse la case.

        Args:
            ligne (int): Indice de la ligne de la case à creuser.
            colonne (int): Indice de la colonne de la case à creuser.
        """
        explosion = self.grille.creuser((ligne, colonne))
        if explosion : 
            self.perdu = True


    def drapeau(self, ligne, colonne) :
        """
        Place un drapeau sur la case.

        Args:
            ligne (int): Indice de la ligne de la case à creuser.
            colonne (int): Indice de la colonne de la case à creuser.
        """
        if self.nbDrapeau == 0 :
            if self.grille[ligne, colonne].etat == 0 :
                print("Plus aucun drapeau n'est disponible.")
            else :
                self.nbDrapeau += self.grille.placerDrapeau((ligne, colonne))
        else : 
            self.nbDrapeau += self.grille.placerDrapeau((ligne, colonne))


    def jouer(self) :
        """
        Lancement d'une partie complète de démineur.
        """
        print(self.grille)
        print("Bienvenue dans cette partie de démineur !\nPour commencer, choisi une case ou creuser. Pour cela, chaque action se décompose en 3 :\n\t- Une lettre pour l'action : C pour creuser et D pour poser un drapeau\n\t- Un nombre pour la ligne à laquelle effectuer l'action\n\t- Un nombre pour la colonne à laquelle effectuer l'action\nPar exemple, 'C 12 5' creuse la case située à la 12eme ligne et 5eme colonne !\n")
        reponse = self.question(premier=True)
        self.grille = Grille(self.longueur, self.largeur, self.nbMines, reponse[1], reponse[2], self.couleur)
        self.casesRestantes()

        while not self.fin() :
            print(self.grille)
            action, ligne, colonne = self.question()

            if action in ["C", "c"] :
                self.creuser(ligne, colonne)

            else :
                self.drapeau(ligne, colonne)

            self.casesRestantes()
            
        if self.perdu :
            self.grille.reveler(False)
            print(self.grille)
            print("\nDommage tu as perdu !\n\n")

        else :
            self.grille.reveler(True)
            print(self.grille)
            print("\nFélicitation tu as gagné cette partie !\n\n")




if __name__ == "__main__" :
    d = Demineur(4,3,1)
    d.jouer()
