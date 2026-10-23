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
        dicoEtats = {-1 : f"\033[96m{self.valeur}\033[0m" if self.valeur != "x" else f"\033[91m{self.valeur}\033[0m", 0 : " ", 1 : "\033[93m⚐\033[0m"}
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




if __name__ == "__main__" :
    c = Case(0,0,False)
    print(c)
    c.placerDrapeau()
    print(c)
    c.placerDrapeau()
    print(c)
    c.decouvrir()
    print(c)
       