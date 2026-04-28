import os
import ia

class Gomoku:

    def __init__(self, jeton=('O','X')):
        """ Constructeur: crée la grille de 15 par 15"""
        self.nl = 15
        self.nc = 15
        self.jeton = jeton
        self.board = [[' ' for i in range(self.nc)] for j in range(self.nl)]
        self.conversion_lettres_entier = {}

    def __str__(self):
        board_str = ' '.join([str((i + 1) % 10) for i in range(self.nc)]) + '\n'

        for i in range(self.nl):
            board_str += ' '.join(self.board[i]) + '\n'

        return board_str

    def show_board(self):
        """self -> None
        Affiche le plateau de 15x15
        """
        print()
        print("━━━┳━━━━━┳━━━━━┳━━━━━┳━━━━━┳━━━━━┳━━━━━┳━━━━━┳━━━━━┳━━━━━┳━━━━━┳━━━━━┳━━━━━┳━━━━━┳━━━━━┳━━━━━┓")

        for i in range(1,self.nl+1):
            ligne_valeurs = "  ┃  ".join(self.board[i-1])

            if i >= 10:
                print(f" {i}┃  {ligne_valeurs}  ┃")

            else:
                print(f" {i} ┃  {ligne_valeurs}  ┃")
            print("━━━╋━━━━━╋━━━━━╋━━━━━╋━━━━━╋━━━━━╋━━━━━╋━━━━━╋━━━━━╋━━━━━╋━━━━━┫━━━━━┫━━━━━┫━━━━━┫━━━━━┫━━━━━┫")
        print("   ┃  A  ┃  B  ┃  C  ┃  D  ┃  E  ┃  F  ┃  G  ┃  H  ┃  I  ┃  J  ┃  K  ┃  L  ┃  M  ┃  N  ┃  O  ┃")
        print("                                                                ")


    def check_win(self, ligne, colonne, Jeton):
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
        """self -> string, string, int, int, string
            Initialise les paramètres de l'IA:
            - sélection de la difficulté
            - style de jeu à aborder
            - Si le joueur veut commencer ou non
        """

        while True:

            try:
                difficulte = input("Quel difficulte choisir ? (Facile, Intermediaire, Difficile)\n").lower()

                match difficulte:

                    case "facile":
                        depth = 1
                        break

                    case "intermediaire":
                        depth = 3
                        break

                    case "intermédiaire":
                        depth = 3
                        break

                    case "difficile":
                        depth = 5
                        break

                    case _:
                        raise ValueError("choisir la difficulté parmi celles proposées.")
                        
            except ValueError as erreur:
                    print(f"Erreur : {erreur}\n")

        while True:

            try:
                playstyle = input("Quel style de jeu l'IA doit elle adopter ? (Agressif, Defensif, Neutre)").lower()

                if playstyle != "agressif" and playstyle != "defensif" and playstyle != "neutre":
                    raise ValueError("Choisir le style de jeu parmi celles proposées (Agressif, Defensif, Neutre)")
                    
                else:
                    break

            except ValueError as erreur:
                print(f"Erreur : {erreur}\n")

        if playstyle == "defensif":
            if depth != 1:
                depth -= 1

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

        return jetonAI,jetonJoueur,depth,playstyle

    def nouvellepartievsIA(self):
        """self -> None
        Fonction principale qui lance la partie contre l'IA.
        Par défaut, on utilise nl = 10 lignes et nc = 10 colonnes
        """
        os.system('cls' if os.name == 'nt' else 'clear')

        for i in range(1,15):
            self.conversion_lettres_entier[chr(65 + i-1)] = i

        count = 0
        win = False
        winner = None
        jetonAI,jetonJoueur,depth,playstyle = self.init_paramIA()
        botJeu = ia.AI(jetonAI,jetonJoueur,depth,playstyle)

        while not win and count < 100:
            count += 1

            if jetonAI == 'X':
                isAIturn = count % 2 == 0

            else:
                isAIturn = count % 2 == 1

            if isAIturn:
                print(f"C'est au tour de l'IA {jetonAI} de jouer...")
                result = botJeu.get_best_move(self)
                self.board[result[1][0]][result[1][1]] = jetonAI

                if count > 6:  # on vérifie à partir du 7eme coup
                    win = self.check_win(result[1][0], result[1][1], jetonAI)

                    if win:
                        winner = jetonAI
            else:

                while True:
                    os.system('cls' if os.name == 'nt' else 'clear')
                    self.show_board()

                    if botJeu.getDernierCoup() is not None:
                        print(f"Coup joué par l'IA: {botJeu.getDernierCoup()}\n"
                              f"Temps de réflexion: {botJeu.tempsReflexion}\n")
                        
                    else:

                        match depth:

                            case 1:
                                print(f"C'est parti contre l'IA en mode: facile")

                            case 2:
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

                        if not ('A' <= lettre <= 'O'):
                            raise ValueError("La lettre doit être comprise entre A et O.")
                        
                        lettre = int(self.conversion_lettres_entier[(coord[0].upper())])
                        nombre = int(partie_nombre)
                        
                        if not (1 <= nombre <= 15):
                            raise ValueError("Le nombre doit être compris entre 1 et 15.")
                        
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

                if count > 6:  # on vérifie à partir du 7eme coup
                    win = self.check_win(ligne, colonne, jetonJoueur)

                    if win:
                        winner = jetonJoueur

        os.system('cls' if os.name == 'nt' else 'clear')
        self.show_board()

        if winner == jetonJoueur:
            print("Vous avez gagné!")

        elif winner == jetonAI:
            print("Dommage, ce n'est pas encore ça !")

        else:
            print("Match nul!")

    def get_remain_moves(self):
        """self -> list
        Fonction qui retourne les coups autour des jetons existants.
        """
        res = []
        pieces = []

        # On trouve d'abord les jetons posés
        for i in range(15):
            for j in range(15):
                if self.board[i][j] != ' ':
                    pieces.append((i, j))

        # Si le plateau est vide, alors on place le permier jeton au centre
        if not pieces:
            return [[7, 7]]

        # On ne génère des coups qu'autour des pièces existantes
        seen = set()
        for r, c in pieces:
            for dr in range(-2, 3):
                for dc in range(-2, 3):
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < 15 and 0 <= nc < 15 and self.board[nr][nc] == ' ':
                        if (nr, nc) not in seen:
                            seen.add((nr, nc))
                            res.append([nr, nc])

        return res

    def nouvellepartieMultilpayer(self, jeton=('O', 'X')):
        """ self x jeton -> none
        Fonction principale qui lance la partie de Gomoku en multijoueur
        """
        os.system('cls' if os.name == 'nt' else 'clear')
        # affichage de la grille initiale
        self.show_board()

        for i in range(1, 11):
            self.conversion_lettres_entier[chr(65 + i - 1)] = i

        win = False
        count = 0

        while not win and count < self.nc*self.nl:
            count += 1
            joueur = (count + 1) % 2 + 1

            while True:
                print(
                    f"Joueur {joueur} ({self.jeton[joueur - 1]}), Entre les coordonnées de l'endroit où tu vas jouer (A1, B2...)")
                
                if count > 1: print(f"dernier coup joué par le joueur {self.jeton[joueur - 1]}: {coord}")
                coord = input('Cordonnées jouée: ')

                try:

                    if len(coord) < 2 or len(coord) > 3:
                        raise ValueError("Format incorrect. Utilisez une lettre suivie d'un nombre (ex: B4).")
                    
                    lettre = coord[0].upper()
                    partie_nombre = coord[1:]

                    if not ('A' <= lettre <= 'O'):
                        raise ValueError("La lettre doit être comprise entre A et O.")
                    
                    lettre = int(self.conversion_lettres_entier[(coord[0].upper())])
                    nombre = int(partie_nombre)
                    
                    if not (1 <= nombre <= 15):
                        raise ValueError("Le nombre doit être compris entre 1 et 15.")
                    
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

            if count > 6:  # on vérifie si un joueur a gagné partir du 7eme coup
                win = self.check_win(ligne, colonne, self.jeton[joueur - 1])

        if win:
            print(f"Le Joueur ayant le jeton ({self.jeton[joueur - 1]}) a gagné!")
            
        else:
            print("Match nul!")