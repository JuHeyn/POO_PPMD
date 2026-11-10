# Démineur - Projet POO PPMD

Pour lancer une partie de démineur, plusieurs possibilités s'offrent à vous :
- [Démineur dans la console](#jouer-depuis-la-console)
- [Lancer depuis la console mais avec interface](#depuis-linterface-de-jeu)
- [Lancer depuis l'interface de selection de niveau](#avec-choix-du-niveau)
---
### Jouer depuis la console

Pour lancer une partie de démineur depuis la console, il suffit de créer un objet de la classe Demineur du fichier [Demineur.py](Demineur.py). Pour cela, vous pouvez choisir le niveau (`Demineur.facile()`, `Demineur.moyen()` ou `Demineur.difficile()`) ou creer vous même votre grille `Demineur(longueur, largeur, nbMines)`. Une fois fait, il suffit d'appeler cette objet avec la fonction `jouer()`.

Par exemple :
```
d = Demineur.facile()
d.jouer()
```

---
### Depuis l'interface de jeu
Pour jouer sur l'interface PyQT, il suffit d'executer le fichier [Interface.py](Interface.py).
Pour modifier la difficulté du niveau, il faut modifier la fin du fichier en suivant les mêmes noms que depuis la console.

Par exemple, remplacer 
```
if __name__ == "__main__" :

    app = QApplication.instance() 
    if not app:
        app = QApplication(sys.argv)

    jeu = Interface.difficile()
    jeu.show()

    app.exec_()
```
par
```
if __name__ == "__main__" :

    app = QApplication.instance() 
    if not app:
        app = QApplication(sys.argv)

    jeu = Interface.moyen()
    jeu.show()

    app.exec_()
```
pour obtenir une partie moyenne.

---
### Avec choix du niveau

Pour lancer depuis le selecteur de niveau, il suffit d'executer le fichier [ChoixNiveau.py](ChoixNiveau.py). Depuis l'interface il est possible de sélectionner la difficulté du niveau ou de créer directement un niveau personnalisé.


---
Jules Heyndels - PPMD ING24 - 2026