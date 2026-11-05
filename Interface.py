import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt, QTimer, QTime

from Demineur import Demineur
from Grille import Grille

class Interface(QWidget) :

    def __init__(self, longueur = 20, largeur = 20, nbMines = 70):
        self.tailleCase = 20
        self.demineur = Demineur(longueur, largeur, nbMines, False)
        self.nouvellePartie = True
        QWidget.__init__(self)
        self.setWindowTitle("Partie de démineur")
        self.setFixedSize((self.tailleCase + 2)*largeur, (self.tailleCase + 2)*longueur + 60)

        self.grilleBouton = [[QPushButton(str(self.demineur.grille[l,c])) for c in range(largeur)] for l in range(longueur)]
        self.grilleLayout = QVBoxLayout()

        ligneLayout = QHBoxLayout()
        informations = QWidget()

        self.labelDrapeau = QLabel(informations)
        self.labelDrapeau.setText(f"{self.demineur.nbDrapeau} ⚑")
        ligneLayout.addWidget(self.labelDrapeau)

        boutonRejouer = QPushButton("Recommencer")
        boutonRejouer.clicked.connect(self.rejouer)
        ligneLayout.addWidget(boutonRejouer)

        self.labelTemps = QLabel(informations)
        self.labelTemps.setText("00:00:00")
        self.labelTemps.setAlignment(Qt.AlignRight)
        ligneLayout.addWidget(self.labelTemps)

        self.timer = QTimer()
        self.timer.timeout.connect(self.chaqueSeconde)
        self.temps = QTime(0, 0, 0)

        self.grilleLayout.addLayout(ligneLayout)

        for l in range(longueur) :
            ligneLayout = QHBoxLayout()
            for c in range(largeur) :
                self.grilleBouton[l][c].setContextMenuPolicy(Qt.CustomContextMenu)
                self.grilleBouton[l][c].clicked.connect(lambda _, ligne=l, colonne=c : self.creuser(ligne, colonne))
                self.grilleBouton[l][c].customContextMenuRequested.connect(lambda _, ligne=l, colonne=c : self.drapeau(ligne, colonne))
                self.grilleBouton[l][c].setFixedSize(self.tailleCase, self.tailleCase)
                ligneLayout.addWidget(self.grilleBouton[l][c])
                
            self.grilleLayout.addLayout(ligneLayout)

        ligneLayout = QHBoxLayout()
        self.labelAnnonce = QLabel(informations)
        self.labelAnnonce.setText("")
        self.labelAnnonce.setAlignment(Qt.AlignCenter)
        ligneLayout.addWidget(self.labelAnnonce)
        self.grilleLayout.addLayout(ligneLayout)

        self.setLayout(self.grilleLayout)

    def rejouer(self) :
        self.nouvellePartie = True
        self.demineur.grille = Grille(self.demineur.longueur, self.demineur.largeur, 0, -1, -1, False)
        for l in range(self.demineur.longueur) :
            for c in range(self.demineur.largeur) :
                self.grilleBouton[l][c].setEnabled(True)
                self.grilleBouton[l][c].setStyleSheet("")

        self.actualiserGrille()

        self.demineur.nbDrapeau = self.demineur.nbMines
        self.timer.stop()
        self.temps = QTime(0, 0, 0)
        self.demineur.perdu = False
        self.labelTemps.setText("00:00:00")
        self.labelDrapeau.setText(f"{self.demineur.nbDrapeau} ⚑")
        self.labelAnnonce.setText("")


    def chaqueSeconde(self):
        self.temps = self.temps.addSecs(1)
        jeu.labelTemps.setText(self.temps.toString("hh:mm:ss"))

    def creuser(self, l, c) :
        if self.nouvellePartie :
            self.nouvellePartie = False
            self.demineur.grille = Grille(self.demineur.longueur, self.demineur.largeur, self.demineur.nbMines, l, c, False)
            self.timer.start(1000)

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
        self.labelDrapeau.setText(f"{self.demineur.nbDrapeau} ⚑")

        if self.demineur.fin() :
            self.fin()

        else :
            self.actualiserGrille()


    def fin(self) :

        self.timer.stop()
        
        if self.demineur.perdu :
            self.demineur.grille.reveler(False)
            self.actualiserGrille()
            self.labelAnnonce.setText("Dommage, tu as perdu ...")

        else :
            self.demineur.grille.reveler(True)
            self.actualiserGrille()
            self.labelAnnonce.setText("Bravo ! Tu as gagné cette partie !")
        

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
