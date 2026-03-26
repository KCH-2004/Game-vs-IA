import os
import ia

class Puissance5:

    def __init__(self,nl = 10, nc = 10, jeton=('O','X')):
        """ Constructeur, crée la grille et lance une nouvelle partie"""
        self.nl = nl
        self.nc = nc
        self.jeton = jeton
        self.board = [[' ' for i in range(nc)] for j in range(nl)]
        self.nouvellepartie()

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


    def check_victoire(self, ligne, colonne, Jeton):
        """ vérifie si le dernier coup joué, qui a placé le jeton
        de joueur en (ligne,colonne) permet de gagner.
        """
        pattern = Jeton * 5  # si on trouve jeton qui se suivent, c'est gagné
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

    def nouvellepartie(self):
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

        compteur = 0
        victoire = False
        gagnant = None
        rep = input("Voulez vous commencer ? (répondre par oui ou non)\n")

        while rep.lower() != 'oui' and rep.lower() != 'non':
            rep = input("Voulez vous commencer ? (répondre par oui ou non)\n")

        if rep == "oui":
            jetonAI,jetonJoueur = 'X', 'O'
        else:
            jetonAI,jetonJoueur = 'O', 'X'

        while not victoire and compteur < 100:
            compteur += 1
            if jetonAI == 'X':
                isAIturn = compteur % 2 == 0
            else:
                isAIturn = compteur % 2 == 1

            if isAIturn:
                print(f"C'est au tour de l'IA {jetonAI} de jouer...")
                result = ia.minimax(self,1,True,jetonAI,jetonJoueur)
                self.board[result[1][0]][result[1][1]] = jetonAI
                os.system('cls' if os.name == 'nt' else 'clear')
                self.show_board()
                if compteur > 6:  # on vérifie à partir du 7eme coup
                    victoire = self.check_victoire(result[1][0], result[1][1], jetonAI)
                    if victoire:
                        gagnant = jetonAI
            else:
                while True:
                    print(f"Joueur (Jeton {jetonJoueur}), Entre les coordonnées de l'endroit où tu vas jouer (A1, B2...)")
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
                self.board[ligne][colonne] = jetonJoueur

                os.system('cls' if os.name == 'nt' else 'clear')
                self.show_board()

                if compteur > 6:  # on vérifie à partir du 7eme coup
                    victoire = self.check_victoire(ligne, colonne, jetonJoueur)
                    if victoire:
                        gagnant = jetonJoueur

        if gagnant == jetonJoueur:
            print("Vous avez gagné!")
        elif gagnant == jetonAI:
            print("Dommage, ce n'est pas encore ça !")
        else:
            print("Match nul!")

    def get_remain_moves(self):
        res = []
        for i in range(10):
            for j in range(10):
                if self.board[i][j] == ' ':
                    res.append([i, j])
        return res


jeu = Puissance5()