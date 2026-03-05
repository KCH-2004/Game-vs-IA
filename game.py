import os
class Puissance5:

    def __init__(self,nl = 10, nc = 10, jeton=('O','X')):
        """ Constructeur, crée la grille et lance une nouvelle partie"""
        self.nl = nl
        self.nc = nc
        self.jeton = jeton
        self.board = [[' ' for i in range(nc)] for j in range(nl)]
        self.nouvellepartie(self.nl, self.nc, self.jeton)

    def __str__(self):
        board_str = ' '.join([str((i + 1) % 10) for i in range(self.nc)]) + '\n'
        for i in range(self.nl):
            board_str += ' '.join(self.board[i]) + '\n'
        return board_str

    def show_board(self):
        print("━━━┳━━━━━┳━━━━━┳━━━━━┳━━━━━┳━━━━━┳━━━━━┳━━━━━┳━━━━━┳━━━━━┳━━━━━┓")
        for i in range(1,self.nl+1):
            ligne_valeurs = "  ┃  ".join(self.board[i-1])
            if i == 10:
                print(f" {i}┃  {ligne_valeurs}  ┃")
            else:
                print(f" {i} ┃  {ligne_valeurs}  ┃")
            print("━━━╋━━━━━╋━━━━━╋━━━━━╋━━━━━╋━━━━━╋━━━━━╋━━━━━╋━━━━━╋━━━━━╋━━━━━┫")
        print("   ┃  A  ┃  B  ┃  C  ┃  D  ┃  E  ┃  F  ┃  G  ┃  H  ┃  I  ┃  J  ┃")
        print("                                                                ")


    def check_victoire(self, ligne, colonne, joueur):
        """ vérifie si le dernier coup joué, qui a placé le jeton
        de joueur en (ligne,colonne) permet de gagner.
        """
        pattern = self.jeton[joueur - 1] * 5  # si on trouve jeton qui se suivent, c'est gagné
        if pattern in ''.join([l[colonne] for l in self.board]):  # on teste la colonne
            return True

        if pattern in ''.join(self.board[ligne]):  # on teste la ligne
            return True

        diag1 = []  # on teste une première diagonale ("nord-ouest" -> "sud-est")
        for i in range(self.nl):
            check = colonne - ligne + i
            if check < 0 or check >= self.nc:
                continue
            char = self.board[i][(colonne - ligne + i)]
            diag1.append(char)
        diag1 = ''.join(diag1)
        if pattern in diag1:
            return True

        diag2 = []  # on teste une deuxième diagonale ("sud-ouest" -> "nord-est")
        for i in range(self.nl):
            check = colonne + ligne - i
            if check < 0 or check >= self.nc:
                continue
            char = self.board[i][(colonne + ligne - i)]
            diag2.append(char)
        diag2 = ''.join(diag2)
        if pattern in diag2:
            return True

        return False

    def nouvellepartie(self, nl=10, nc=10, jeton=('O', 'X')):
        """
        Fonction principale qui lance la partie.
        Par défaut, on utilise nl = 10 lignes et nc = 10 colonnes
        """
        os.system('cls' if os.name == 'nt' else 'clear')
        # affichage de la grille initiale
        self.show_board()
        conversion_lettres_entier = {}

        for i in range(1,11):
            conversion_lettres_entier[chr(65 + i-1)] = i

        victoire = False
        compteur = 0

        while not victoire and compteur < nc*nl:
            compteur += 1
            # Attention, pour l'affichage, on part de joueur 1 et 2, mais pour
            # l'accès aux jetons, c'est jeton[0] et jeton[1]
            joueur = (compteur + 1) % 2 + 1
            while True:
                print(f"Joueur {joueur} ({self.jeton[joueur-1]}), Entre les coordonnées de l'endroit où tu vas jouer (A1, B2...)")
                coord = input('Cordonnées jouée: ')

                try:
                    if len(coord) < 2 or len(coord) > 3:
                        raise ValueError("Format incorrect. Utilisez une lettre suivie d'un nombre (ex: B4).")
                    lettre = coord[0].upper()
                    partie_nombre = coord[1:]
                    if not ('A' <= lettre <= 'J'):
                        raise ValueError("La lettre doit être comprise entre A et J.")
                    lettre = int(conversion_lettres_entier[(coord[0].upper())])
                    nombre = int(partie_nombre)
                    if not (1 <= nombre <= 10):
                        raise ValueError("Le nombre doit être compris entre 1 et 10.")
                    if not(self.board[nombre-1][lettre-1] == ' '):
                        raise ValueError("Cette case a déjà été jouée.")
                    break
                except ValueError as erreur:
                    print(f"Erreur : {erreur}\n")

            colonne = int(conversion_lettres_entier[(coord[0].upper())]) -1
            ligne = int(coord[1:]) -1
            self.board[ligne][colonne] = self.jeton[joueur - 1]

            os.system('cls' if os.name == 'nt' else 'clear')
            self.show_board()

            if compteur > 6:  # on vérifie à partir du 7eme coup
                victoire = self.check_victoire(ligne, colonne, joueur)

        if victoire:
            print(f"Le Joueur {joueur} ({self.jeton[joueur-1]}) a gagné!")
        else:
            print("Match nul!")

jeu = Puissance5()