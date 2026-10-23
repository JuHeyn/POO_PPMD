from Grille import Grille

class Demineur() :
    def __init__(self, longueur = -1, largeur = -1, nbMines = -1):
        self.longueur = longueur
        self.largeur = largeur
        self.nbMines = nbMines
        self.perdu = False
        self.nbDrapeau = nbMines
        

        if self.longueur == -1 :
            self.longueur = int(input("Quelle longueur de grille ? \n\t"))
        if self.largeur == -1 :
            self.largeur = int(input("Quelle largeur de grille ? \n\t"))
        if self.nbMines == -1 :
            self.nbMines = int(input("Combien de mines présentes dans la grille ? \n\t"))

        
        self.caseCachees = self.longueur * self.largeur

        ligne = " " + "----" * self.largeur + "-\n"
        affichage = ligne + " | "
        for _ in range(self.longueur) :
            for _ in range(self.largeur) :
                affichage += " " + " | "
            affichage += "\n" + ligne + " | "

        self.grille = affichage[:-2]

    def question(self, premier = False) :
        reponse = input(f"Que souhaites tu faire ? (Action Ligne Colonne)   -   {self.nbDrapeau} drapeaux restants\n\t").split()
        while self.testReponse(reponse, premier) :
            reponse = input(f"Je n'ai pas compris ton action, que souhaites tu faire ? (Action Ligne Colonne)   -   {self.nbDrapeau} drapeaux restants\n\t").split()

        return reponse
            

    def testReponse(self, reponse, premier) : 
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


    def jouer(self) :

        print("Bienvenue dans cette partie de démineur !\nPour commencer, choisi une case ou creuser. Pour cela, chaque action se décompose en 3 :\n\t- Une lettre pour l'action : C pour creuser et D pour poser un drapeau\n\t- Un nombre pour la ligne à laquelle effectuer l'action\n\t- Un nombre pour la colonne à laquelle effectuer l'action\nPar exemple, 'C 12 5' creuse la case située à la 12eme ligne et 5eme colonne !\n")
        reponse = self.question(premier=True)
        self.grille = Grille(self.longueur, self.largeur, self.nbMines, reponse[1], reponse[2])
        

        while (not self.perdu) and (self.nbDrapeau != 0) and (self.caseCachees != self.nbDrapeau) :
            print(self.grille)
            action, ligne, colonne = self.question()

            if action in ["C", "c"] :
                explosion = self.grille.creuser((ligne, colonne))
                self.caseCachees += -1
                if explosion : 
                    self.perdu = True

            else :
                if self.nbDrapeau == 0 :
                    if self.grille[ligne, colonne].etat == 0 :
                        print("Plus aucun drapeau n'est disponible.")
                    else :
                        self.nbDrapeau += self.grille.placerDrapeau((ligne, colonne))
                else : 
                    self.nbDrapeau += self.grille.placerDrapeau((ligne, colonne))

        

        if self.perdu :
            self.grille.reveler(True)
            print(self.grille)
            print("\nDommage tu as perdu !\n\n")

        else :
            self.grille.reveler(False)
            print(self.grille)
            print("\nFélicitation tu as gagné cette partie !\n\n")




if __name__ == "__main__" :
    d = Demineur(5,5,12)
    d.jouer()
