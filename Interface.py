import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt

from Demineur import Demineur
from Grille import Grille

class Interface(QWidget) :

    def __init__(self, d=Demineur(10,15,100, couleur=False)):
        self.tailleCase = 20
        self.demineur = d
        self.nouvellePartie = True
        QWidget.__init__(self)
        self.setWindowTitle("Partie de démineur")
        self.setFixedSize((self.tailleCase + 2)*d.largeur, (self.tailleCase + 2)*d.longueur + 40)

        self.grilleBouton = [[QPushButton(str(d.grille[l,c])) for c in range(d.largeur)] for l in range(d.longueur)]
        self.grilleLayout = QVBoxLayout()
        

        for l in range(d.longueur) :
            ligneLayout = QHBoxLayout()
            for c in range(d.largeur) :
                self.grilleBouton[l][c].setContextMenuPolicy(Qt.CustomContextMenu)
                self.grilleBouton[l][c].clicked.connect(lambda _, ligne=l, colonne=c : self.creuser(ligne, colonne))
                self.grilleBouton[l][c].customContextMenuRequested.connect(lambda _, ligne=l, colonne=c : self.drapeau(ligne, colonne))
                self.grilleBouton[l][c].setFixedSize(self.tailleCase, self.tailleCase)
                # self.grilleBouton[l][c].setStyleSheet("background-color: #00FF00; color: #00FF00;")
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
        
        if self.demineur.perdu :
            self.demineur.grille.reveler(False)
            self.actualiserGrille()
            print("\nDommage tu as perdu !\n\n")

        else :
            self.demineur.grille.reveler(True)
            self.actualiserGrille()
            print("\nFélicitation tu as gagné cette partie !\n\n")
        

        

    def actualiserGrille(self) :
        dicoCouleur = {0 : '#7DCF4A',
                       1 : '#85B541',
                       2 : '#8C9B38',
                       3 : '#94812E',
                       4 : '#9B6825',
                       5 : '#A34E1C',
                       6 : '#AA3413',
                       7 : '#B21A09',
                       8 : '#B90000'}
        
        for l in range(self.demineur.longueur) :
            for c in range(self.demineur.largeur) :
                case = self.demineur.grille[l,c]
                self.grilleBouton[l][c].setText(str(case))
                if case.etat == -1 and case.bombe :
                    self.grilleBouton[l][c].setEnabled(False)
                    self.grilleBouton[l][c].setStyleSheet("background-color: #FF0000; color: #000000;")
                elif case.etat == -1 :
                    self.grilleBouton[l][c].setEnabled(False)
                    self.grilleBouton[l][c].setStyleSheet(f"color: {dicoCouleur[case.valeur]};")
                elif case.etat == 1 and self.demineur.fin() :
                    self.grilleBouton[l][c].setEnabled(False)
                    self.grilleBouton[l][c].setStyleSheet(f"background-color: {"#7DCF4A" if case.bombe else "#FF8800"}; color: #000000;")




if __name__ == "__main__" :

    app = QApplication.instance() 
    if not app:
        app = QApplication(sys.argv)

    jeu = Interface()
    jeu.show()

    app.exec_()
