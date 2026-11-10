import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QLabel, QSpinBox
from Interface import Interface

class ChoixNiveau(QWidget) :

    def __init__(self):
            """
            Création d'un objet d'interface de jeu de démineur.
    
            Args:
                longueur (int, optional): Nombre de ligne du démineur. Defaults to 20.
                largeur (int, optional): Nombre de colonne du démineur. Defaults to 20.
                nbMines (int, optional): Nombre de mines du démineur. Defaults to 70.
            """

            QWidget.__init__(self)
            self.setWindowTitle("Démineur - Choix du niveau")
            self.setFixedSize(200, 200)

            self.layout = QVBoxLayout()
    
            boutonFacile = QPushButton("Niveau facile")
            boutonFacile.clicked.connect(self.facile)
            self.layout.addWidget(boutonFacile)

            boutonMoyen = QPushButton("Niveau moyen")
            boutonMoyen.clicked.connect(self.moyen)
            self.layout.addWidget(boutonMoyen)

            boutonDifficile = QPushButton("Niveau difficile")
            boutonDifficile.clicked.connect(self.difficile)
            self.layout.addWidget(boutonDifficile)

            separateur = QLabel()
            separateur.setText("_____________________________")
            self.layout.addWidget(separateur)

            ligne = QHBoxLayout()
            labelLongueur = QLabel("Nombre de lignes :")
            ligne.addWidget(labelLongueur)
            longueur = QSpinBox(self)
            longueur.setDisplayIntegerBase(10)
            longueur.setValue(20)
            longueur.setMinimum(3)
            ligne.addWidget(longueur)
            
            self.layout.addLayout(ligne)

            ligne = QHBoxLayout()
            labelLargeur = QLabel("Nombre de colonnes :")
            ligne.addWidget(labelLargeur)
            largeur = QSpinBox(self)
            largeur.setDisplayIntegerBase(10)
            largeur.setValue(20)
            largeur.setMinimum(3)
            ligne.addWidget(largeur)
            
            self.layout.addLayout(ligne)

            ligne = QHBoxLayout()
            labelMines = QLabel("Nombre de mines :")
            ligne.addWidget(labelMines)
            mines = QSpinBox(self)
            mines.setDisplayIntegerBase(10)
            mines.setValue(70)
            ligne.addWidget(mines)
            
            self.layout.addLayout(ligne)

            boutonCustom = QPushButton("Niveau Custom")
            boutonCustom.clicked.connect(lambda : self.custom(longueur.value(), largeur.value(), mines.value()))
            self.layout.addWidget(boutonCustom)

            self.setLayout(self.layout)

    def facile(self) :
        jeu = Interface.facile()
        jeu.show()
        self.close()

    def moyen(self) :
        jeu = Interface.moyen()
        jeu.show()
        self.close()

    def difficile(self) :
        jeu = Interface.difficile()
        jeu.show()
        self.close()

    def custom(self, longueur, largeur, nbMines) :
        jeu = Interface(longueur, largeur, nbMines)
        jeu.show()
        self.close()


if __name__ == "__main__" :

    app = QApplication.instance() 
    if not app:
        app = QApplication(sys.argv)

    jeu = ChoixNiveau()
    jeu.show()

    app.exec_()