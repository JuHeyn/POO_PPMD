import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QVBoxLayout
from PyQt5.QtCore import Qt

from Demineur import Demineur
from Grille import Grille

class Interface(QWidget) :

    def __init__(self, d=Demineur(5,8,3, couleur=False)):
        self.demineur = d
        self.nouvellePartie = True
        QWidget.__init__(self)
        self.setWindowTitle("Partie de démineur")
        self.setFixedSize(55*d.largeur, 55*d.longueur)

        self.grilleBouton = [[QPushButton(str(d.grille[l,c])) for c in range(d.largeur)] for l in range(d.longueur)]
        self.grilleLayout = QVBoxLayout()

        for l in range(d.longueur) :
            ligneLayout = QHBoxLayout()
            for c in range(d.largeur) :
                self.grilleBouton[l][c].setContextMenuPolicy(Qt.CustomContextMenu)
                self.grilleBouton[l][c].clicked.connect(lambda _, ligne=l, colonne=c : self.creuser(ligne, colonne))
                self.grilleBouton[l][c].customContextMenuRequested.connect(lambda _, ligne=l, colonne=c : self.drapeau(ligne, colonne))
                self.grilleBouton[l][c].setFixedSize(50, 50)
                ligneLayout.addWidget(self.grilleBouton[l][c])
                
            self.grilleLayout.addLayout(ligneLayout)


        self.setLayout(self.grilleLayout)


    def creuser(self, l, c) :
        if self.nouvellePartie :
            self.nouvellePartie = False
            self.demineur.grille = Grille(self.demineur.longueur, self.demineur.largeur, self.demineur.nbMines, l, c, False)
        else :
            self.demineur.creuser(l, c)
            
        self.demineur.casesRestantes()

        if self.demineur.fin() :
            self.fin()

        else :
            self.actualiserGrille()


    def drapeau(self, l, c) :
        if self.nouvellePartie :
            pass
        else :
            self.demineur.drapeau(l, c)
        self.demineur.casesRestantes()

        if self.demineur.fin() :
            self.fin()

        else :
            self.actualiserGrille()


    def fin(self) :
        self.demineur.grille.reveler()
        self.actualiserGrille()
        if self.demineur.perdu :
            print("\nDommage tu as perdu !\n\n")

        else :
            print("\nFélicitation tu as gagné cette partie !\n\n")

        

    def actualiserGrille(self) :
        for l in range(self.demineur.longueur) :
            for c in range(self.demineur.largeur) :
                self.grilleBouton[l][c].setText(str(self.demineur.grille[l,c]))



if __name__ == "__main__" :

    app = QApplication.instance() 
    if not app:
        app = QApplication(sys.argv)

    jeu = Interface()
    jeu.show()

    app.exec_()
