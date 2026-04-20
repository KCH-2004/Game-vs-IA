import os
import ia
import time

class Puissance5:

    def __init__(self,nl = 10, nc = 10, jeton=('O','X')):
        """ Constructeur, crée la grille et lance une nouvelle partie"""
        self.nl = nl
        self.nc = nc
        self.jeton = jeton
        self.board = [[' ' for i in range(nc)] for j in range(nl)]
        self.conversion_lettres_entier = {}

    def __str__(self):
        board_str = ' '.join([str((i + 1) % 10) for i in range(self.nc)]) + '\n'
        for i in range(self.nl):
            board_str += ' '.join(self.board[i]) + '\n'
        return board_str

    def show_board(self):
        print()
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

    def init_paramIA(self):
            while True:
                try:
                    isStarting = input("Voulez vous commencer ? (répondre par oui ou non)\n").lower()
                    match isStarting:
                        case "oui":
                            jetonAI,jetonJoueur = 'X', 'O'
                            break
                        case "non":
                            jetonAI,jetonJoueur = 'O', 'X'
                            break
                        case _:
                            raise ValueError("La réponse doit être oui ou non")
                except ValueError as erreur:
                    print(f"Erreur : {erreur}\n")

            while True:
                try:
                    difficulte = input("Quel difficulte choisir ? (Facile, Intermediaire, Difficile)\n").lower()
                    match difficulte:
                        case "facile":
                            depth = 1
                            break
                        case "intermediaire":
                            depth = 2
                            break
                        case "intermédiaire":
                            depth = 2
                            break
                        case "difficile":
                            depth = 3
                            break
                        case _:
                            raise ValueError("choisir la difficulté parmi celles proposées.")
                except ValueError as erreur:
                        print(f"Erreur : {erreur}\n")

            while True:
                try:
                    playstyle = input("Quel style de jeu l'IA doit elle aborder ? (Agressif, Defensif)").lower()
                    if playstyle != "agressif" and playstyle != "defensif":
                        raise ValueError("Choisir le style de jeu parmi celles proposées")
                    else:
                        break
                except ValueError as erreur:
                    print(f"Erreur : {erreur}\n")

            while True:
                try:
                    evalMode = input("Quel mode d'évaluation pour l'IA ? (linéaire ou réaliste)").lower()
                    match evalMode:
                        case "linéaire":
                            evaluate_ouvert = {0:0,1:2, 2:3, 3:4, 4:5,5:6}
                            break
                        case "lineaire":
                            evaluate_ouvert = {0:0,1:2, 2:3, 3:4, 4:5,5:6}
                            break
                        case "realiste":
                            evaluate_ouvert = {0:0,1: 1, 2: 5, 3: 50, 4: 500}
                            break
                        case "réaliste":
                            evaluate_ouvert = {0:0,1: 1, 2: 5, 3: 50, 4: 500}
                            break
                        case _:
                            raise ValueError("Choisir l'évaluation parmi celles proposées.")
                except ValueError as erreur:
                    print(f"Erreur : {erreur}\n")

            return jetonAI,jetonJoueur,depth,playstyle,evaluate_ouvert

    def nouvellepartievsIA(self):
        """
        Fonction principale qui lance la partie.
        Par défaut, on utilise nl = 10 lignes et nc = 10 colonnes
        """
        os.system('cls' if os.name == 'nt' else 'clear')
        # affichage de la grille initiale
        temps_IA = None
        coup_IA = None

        for i in range(1,11):
            self.conversion_lettres_entier[chr(65 + i-1)] = i

        compteur = 0
        victoire = False
        gagnant = None
        jetonAI,jetonJoueur,depth,playstyle,evaluate_ouvert = self.init_paramIA()

        while not victoire and compteur < 100:
            compteur += 1
            if jetonAI == 'X':
                isAIturn = compteur % 2 == 0
            else:
                isAIturn = compteur % 2 == 1

            if isAIturn:
                print(f"C'est au tour de l'IA {jetonAI} de jouer...")
                start = time.perf_counter()
                result = ia.minimax(self,depth,True,jetonAI,jetonJoueur,evaluate_ouvert,playstyle)
                end = time.perf_counter()
                temps_IA = end - start
                coup_IA = [chr(65 + (result[1][1])),str(result[1][0]+1)]
                self.board[result[1][0]][result[1][1]] = jetonAI
                if compteur > 6:  # on vérifie à partir du 7eme coup
                    victoire = self.check_victoire(result[1][0], result[1][1], jetonAI)
                    if victoire:
                        gagnant = jetonAI
            else:
                while True:
                    os.system('cls' if os.name == 'nt' else 'clear')
                    self.show_board()
                    if coup_IA is not None:
                        str_coup = ' '.join(coup_IA)
                        print(f"Coup joué par l'IA: {str_coup}\n"
                              f"Temps de réflexion: {temps_IA}\n")
                    else:
                        match depth:
                            case 2:
                                print(f"C'est parti contre l'IA en mode: facile")
                            case 3:
                                print(f"C'est parti contre l'IA en mode: intermédiaire")
                            case 4:
                                print(f"C'est parti contre l'IA en mode: difficile")

                    print(f"Joueur (Jeton {jetonJoueur}), Entre les coordonnées de l'endroit où tu vas jouer (A1, B2...)\n")
                    coord = input('Cordonnées jouée: ')
                    try:
                        if len(coord) < 2 or len(coord) > 3:
                            raise ValueError("Format incorrect. Utilisez une lettre suivie d'un nombre (ex: B4).")
                        lettre = coord[0].upper()
                        partie_nombre = coord[1:]
                        if not ('A' <= lettre <= 'J'):
                            raise ValueError("La lettre doit être comprise entre A et J.")
                        lettre = int(self.conversion_lettres_entier[(coord[0].upper())])
                        nombre = int(partie_nombre)
                        if not (1 <= nombre <= 10):
                            raise ValueError("Le nombre doit être compris entre 1 et 10.")
                        if not(self.board[nombre-1][lettre-1] == ' '):
                            raise ValueError("Cette case a déjà été jouée.")
                        break
                    except ValueError as erreur:
                        print(f"Erreur : {erreur}\n")

                colonne = int(self.conversion_lettres_entier[(coord[0].upper())]) -1
                ligne = int(coord[1:]) -1
                self.board[ligne][colonne] = jetonJoueur

                os.system('cls' if os.name == 'nt' else 'clear')
                self.show_board()

                if compteur > 6:  # on vérifie à partir du 7eme coup
                    victoire = self.check_victoire(ligne, colonne, jetonJoueur)
                    if victoire:
                        gagnant = jetonJoueur

        os.system('cls' if os.name == 'nt' else 'clear')
        self.show_board()

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
                    voisin_trouve = False
                    for decalage_ligne in range (-1,2):
                        voisin_ligne = i + decalage_ligne
                        for decalage_colonne in range (-1,2):
                            voisin_colonne = j + decalage_colonne
                            if 0 <= voisin_ligne < 10 and 0 <= voisin_colonne < 10:
                                if self.board[voisin_ligne][voisin_colonne] != ' ':
                                    voisin_trouve = True
                                    break
                        if voisin_trouve:
                            res.append([i, j])
                            break
        if len(res) == 0:
            return [[4, 4]]
        else:
            return res

    def nouvellepartieMultilpayer(self, jeton=('O', 'X')):
        """
        Fonction principale qui lance la partie.
        Par défaut, on utilise nl = 10 lignes et nc = 10 colonnes
        """
        os.system('cls' if os.name == 'nt' else 'clear')
        # affichage de la grille initiale
        self.show_board()

        for i in range(1, 11):
            self.conversion_lettres_entier[chr(65 + i - 1)] = i

        victoire = False
        compteur = 0

        while not victoire and compteur < self.nc*self.nl:
            compteur += 1
            # Attention, pour l'affichage, on part de joueur 1 et 2, mais pour
            # l'accès aux jetons, c'est jeton[0] et jeton[1]
            joueur = (compteur + 1) % 2 + 1
            while True:
                print(
                    f"Joueur {joueur} ({self.jeton[joueur - 1]}), Entre les coordonnées de l'endroit où tu vas jouer (A1, B2...)")
                if compteur > 1: print(f"dernier coup joué par le joueur {self.jeton[joueur - 1]}: {coord}")
                coord = input('Cordonnées jouée: ')

                try:
                    if len(coord) < 2 or len(coord) > 3:
                        raise ValueError("Format incorrect. Utilisez une lettre suivie d'un nombre (ex: B4).")
                    lettre = coord[0].upper()
                    partie_nombre = coord[1:]
                    if not ('A' <= lettre <= 'J'):
                        raise ValueError("La lettre doit être comprise entre A et J.")
                    lettre = int(self.conversion_lettres_entier[(coord[0].upper())])
                    nombre = int(partie_nombre)
                    if not (1 <= nombre <= 10):
                        raise ValueError("Le nombre doit être compris entre 1 et 10.")
                    if not (self.board[nombre - 1][lettre - 1] == ' '):
                        raise ValueError("Cette case a déjà été jouée.")
                    break
                except ValueError as erreur:
                    print(f"Erreur : {erreur}\n")

            colonne = int(self.conversion_lettres_entier[(coord[0].upper())]) - 1
            ligne = int(coord[1:]) - 1
            self.board[ligne][colonne] = self.jeton[joueur - 1]

            os.system('cls' if os.name == 'nt' else 'clear')
            self.show_board()

            if compteur > 6:  # on vérifie à partir du 7eme coup
                victoire = self.check_victoire(ligne, colonne, self.jeton[joueur - 1])

        if victoire:
            print(f"Le Joueur ayant le jeton ({self.jeton[joueur - 1]}) a gagné!")
        else:
            print("Match nul!")