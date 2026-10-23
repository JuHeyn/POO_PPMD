class Case() :

    def __init__(self, ligne:int, colonne:int, bombe:bool) :
        self.ligne = ligne
        self.colonne = colonne
        self.bombe = bombe
        self.etat = 0 # -1 = Creuse, 0 = intact, 1 = drapeau  
        self.valeur = 0

    def __str__(self):
        if self.bombe :
            self.valeur = "x"
        dicoEtats = {-1 : str(self.valeur), 0 : " ", 1 : "⚐"}
        return dicoEtats[self.etat]

    def placerDrapeau(self) :
        """
        Place ou enlève un drapeau sur la case
        """
        if self.etat == 0 :
            self.etat = 1
        elif self.etat == 1 :
            self.etat = 0


    def decouvrir(self) :
        if self.bombe :
            return False

        self.etat = -1



if __name__ == "__main__" :
    c = Case(0,0,False)
    print(c)
    c.placerDrapeau()
    print(c)
    c.placerDrapeau()
    print(c)
    c.decouvrir()
    print(c)
       