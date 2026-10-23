class Case() :

    def __init__(self, ligne:int, colonne:int, bombe:bool) :
        self.ligne = ligne
        self.colonne = colonne
        self.bombe = bombe
        self.etat = 0 # -1 = Creuse, 0 = intact, 1 = drapeau  
        self.valeur = 0
        self.zeros = []

    def __str__(self):
        if self.bombe :
            self.valeur = "x"
        dicoCouleurs = {"x" : "\u001b[38;5;1m", 0 : "\u001b[38;5;118m", 1 : "\u001b[38;5;191m", 2 : "\u001b[38;5;221m", 3 : "\u001b[38;5;214m", 4 : "\u001b[38;5;208m", 5 : "\u001b[38;5;202m", 6 : "\u001b[38;5;166m", 7 : "\u001b[38;5;196m", 8 : "\u001b[38;5;160m"}
        dicoEtats = {-1 : f"{dicoCouleurs[self.valeur]}{self.valeur}\033[0m", 0 : " ", 1 : "\033[96m⚐\033[0m"}
        return dicoEtats[self.etat]

    def placerDrapeau(self) :
        """
        Place ou enlève un drapeau sur la case
        """
        if self.etat == 0 :
            self.etat = 1
            return -1
        elif self.etat == 1 :
            self.etat = 0
            return 1


    def creuser(self) :
        self.etat = -1
        if self.bombe :
            return True

        if self.valeur == 0 :
            return False




if __name__ == "__main__" :
    c = Case(0,0,False)
    print(c)
    c.placerDrapeau()
    print(c)
    c.placerDrapeau()
    print(c)
    c.decouvrir()
    print(c)
       