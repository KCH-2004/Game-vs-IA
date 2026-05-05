import os
import ia


class Gomoku:

    def __init__(self, jeton=('O', 'X')):
        """self x tuple -> None
        Constructeur: initialise la classe Gomoku et crée la grille de 15 par 15
        """
        self.nl = 15  # Nombre de lignes du plateau
        self.nc = 15  # Nombre de colonnes du plateau
        self.jeton = jeton  # Tuple contenant les jetons des joueurs
        # Création d'une matrice 15x15 remplie d'espaces vides représentant le plateau
        self.board = [[' ' for i in range(self.nc)] for j in range(self.nl)]
        self.conversion_lettres_entier = {}  # Dictionnaire utilisé pour convertir les lettres des coordonnées en entiers

    def __str__(self):
        """self -> string
        Retourne une représentation en chaîne de caractères du plateau de jeu
        """
        # Création de la première ligne avec les numéros de colonnes (modulo 10 pour l'affichage)
        board_str = ' '.join([str((i + 1) % 10) for i in range(self.nc)]) + '\n'

        # Ajout de chaque ligne du plateau à la chaîne finale
        for i in range(self.nl):
            board_str += ' '.join(self.board[i]) + '\n'

        return board_str

    def show_board(self):
        """self -> None
        Affiche le plateau de 15x15 de façon stylisée dans la console
        """
        print()
        print("━━━┳━━━━━┳━━━━━┳━━━━━┳━━━━━┳━━━━━┳━━━━━┳━━━━━┳━━━━━┳━━━━━┳━━━━━┳━━━━━┳━━━━━┳━━━━━┳━━━━━┳━━━━━┓")

        # Parcours des lignes pour construire l'affichage visuel avec le formatage du tableau
        for i in range(1, self.nl + 1):
            ligne_valeurs = "  ┃  ".join(self.board[i - 1])

            # Ajustement dynamique de l'espacement pour gérer les nombres à deux chiffres (>= 10)
            if i >= 10:
                print(f" {i}┃  {ligne_valeurs}  ┃")

            else:
                print(f" {i} ┃  {ligne_valeurs}  ┃")
            print("━━━╋━━━━━╋━━━━━╋━━━━━╋━━━━━╋━━━━━╋━━━━━╋━━━━━╋━━━━━╋━━━━━╋━━━━━┫━━━━━┫━━━━━┫━━━━━┫━━━━━┫━━━━━┫")
        print("   ┃  A  ┃  B  ┃  C  ┃  D  ┃  E  ┃  F  ┃  G  ┃  H  ┃  I  ┃  J  ┃  K  ┃  L  ┃  M  ┃  N  ┃  O  ┃")
        print("                                                                ")

    def check_win(self, ligne, colonne, Jeton):
        """self x int x int x string -> bool
        vérifie si le dernier coup joué, qui a placé le jeton
        de joueur en (ligne,colonne) permet de gagner.
        """
        pattern = Jeton * 5  # si on trouve 5 jetons identiques qui se suivent, c'est gagné

        # Vérification sur l'axe vertical (colonne)
        if pattern in ''.join([l[colonne] for l in self.board]):  # on teste la colonne
            return True

        # Vérification sur l'axe horizontal (ligne)
        if pattern in ''.join(self.board[ligne]):  # on teste la ligne
            return True

        diag1 = []  # on teste une première diagonale ("\")

        for i in range(self.nl):
            check = colonne - ligne + i

            # On s'assure de ne pas déborder des limites du plateau de jeu
            if check < 0 or check >= self.nc:
                continue

            char = self.board[i][(colonne - ligne + i)]
            diag1.append(char)
        diag1 = ''.join(diag1)

        # Vérification si le motif gagnant est dans cette première diagonale
        if pattern in diag1:
            return True

        diag2 = []  # on teste une deuxième diagonale ("/")

        for i in range(self.nl):
            check = colonne + ligne - i

            # On s'assure de ne pas déborder des limites
            if check < 0 or check >= self.nc:
                continue

            char = self.board[i][(colonne + ligne - i)]
            diag2.append(char)
        diag2 = ''.join(diag2)

        # Vérification si le motif gagnant est dans cette seconde diagonale
        if pattern in diag2:
            return True

        # Si aucun alignement de 5 n'est trouvé, le joueur n'a pas gagné
        return False

    def init_paramIA(self):
        """self -> string, string, int, string
            Initialise les paramètres de l'IA:
            - sélection de la difficulté
            - style de jeu à aborder
            - Si le joueur veut commencer ou non
        """
        # Choix de la difficulté
        while True:

            try:
                difficulte = input("Quel difficulte choisir ? (Facile, Intermediaire, Difficile)\n").lower()

                match difficulte:

                    case "facile":
                        depth = 1  # Profondeur faible pour l'algorithme Minimax
                        break

                    case "intermediaire":
                        depth = 3  # Profondeur moyenne
                        break

                    case "intermédiaire":
                        depth = 3
                        break

                    case "difficile":
                        depth = 5  # Profondeur élevée pour calculer plus de coups d'avance
                        break

                    case _:
                        raise ValueError("choisir la difficulté parmi celles proposées.")

            except ValueError as erreur:
                print(f"Erreur : {erreur}\n")

        # Choix du style de jeu de l'IA
        while True:

            try:
                playstyle = input("Quel style de jeu l'IA doit elle adopter ? (Agressif, Defensif, Neutre)").lower()

                if playstyle != "agressif" and playstyle != "defensif" and playstyle != "neutre":
                    raise ValueError("Choisir le style de jeu parmi celles proposées (Agressif, Defensif, Neutre)")

                else:
                    break

            except ValueError as erreur:
                print(f"Erreur : {erreur}\n")

        # Ajustement d'équilibrage : On réduit la profondeur d'un cran si l'IA joue défensif
        if playstyle == "defensif":
            if depth != 1:
                depth -= 1

        # Configuration du premier joueur
        while True:

            try:
                isStarting = input("Voulez vous commencer ? (répondre par oui ou non)\n").lower()

                match isStarting:

                    case "oui":
                        jetonAI, jetonJoueur = 'X', 'O'  # Si le joueur commence, il prend les 'O'
                        break

                    case "non":
                        jetonAI, jetonJoueur = 'O', 'X'  # Si l'IA commence, elle prend les 'O'
                        break

                    case _:
                        raise ValueError("La réponse doit être oui ou non")

            except ValueError as erreur:
                print(f"Erreur : {erreur}\n")

        return jetonAI, jetonJoueur, depth, playstyle

    def nouvellepartievsIA(self):
        """self -> None
        Fonction principale qui lance la partie contre l'IA.
        Par défaut, on utilise nl = 10 lignes et nc = 10 colonnes
        """
        # Efface la console selon le système d'exploitation pour rendre l'affichage fluide
        os.system('cls' if os.name == 'nt' else 'clear')

        # Initialisation du dictionnaire permettant de convertir les colonnes lettrées (A, B, C...) en entiers
        for i in range(1, 15):
            self.conversion_lettres_entier[chr(65 + i - 1)] = i

        count = 0
        win = False
        winner = None
        # On initialise les paramètres avant de lancer la boucle de la partie
        jetonAI, jetonJoueur, depth, playstyle = self.init_paramIA()
        botJeu = ia.AI(jetonAI, jetonJoueur, depth, playstyle)

        # Boucle de jeu s'arrêtant en cas de victoire ou de limite de coups (ici 100)
        while not win and count < 100:
            count += 1

            # L'IA vérifie si c'est à son tour de jouer selon le jeton ('O' joue les tours impairs)
            if jetonAI == 'X':
                isAIturn = count % 2 == 0

            else:
                isAIturn = count % 2 == 1

            if isAIturn:
                # Phase de jeu de l'IA
                print(f"C'est au tour de l'IA {jetonAI} de jouer...")
                result = botJeu.get_best_move(self)
                self.board[result[1][0]][result[1][1]] = jetonAI  # Placement du jeton calculé

                if count > 8:  # on vérifie la victoire à partir du 7eme coup (impossible de gagner avant)
                    win = self.check_win(result[1][0], result[1][1], jetonAI)

                    if win:
                        winner = jetonAI
            else:
                # Phase de jeu du joueur humain
                while True:
                    os.system('cls' if os.name == 'nt' else 'clear')
                    self.show_board()  # Affichage du plateau mis à jour

                    # Informations retournées sur le coup précédent de l'IA
                    if botJeu.getDernierCoup() is not None:
                        print(f"Coup joué par l'IA: {botJeu.getDernierCoup()}\n"
                              f"Temps de réflexion: {botJeu.tempsReflexion}\n")

                    else:
                        # Message d'accueil en début de partie
                        match depth:

                            case 1:
                                print(f"C'est parti contre l'IA en mode: facile")

                            case 2:
                                print(f"C'est parti contre l'IA en mode: intermédiaire")

                            case 4:
                                print(f"C'est parti contre l'IA en mode: difficile")

                    print(
                        f"Joueur (Jeton {jetonJoueur}), Entre les coordonnées de l'endroit où tu vas jouer (A1, B2...)\n")
                    coord = input('Cordonnées jouée: ')

                    try:
                        # Validation du format de la saisie (ex: "H8")
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

                        # On empêche de jouer par-dessus un jeton existant
                        if not (self.board[nombre - 1][lettre - 1] == ' '):
                            raise ValueError("Cette case a déjà été jouée.")

                        break

                    except ValueError as erreur:
                        print(f"Erreur : {erreur}\n")

                # Conversion des entrées en index pour le tableau Python (0 à 14)
                colonne = int(self.conversion_lettres_entier[(coord[0].upper())]) - 1
                ligne = int(coord[1:]) - 1
                self.board[ligne][colonne] = jetonJoueur

                os.system('cls' if os.name == 'nt' else 'clear')
                self.show_board()

                if count > 8:  # on vérifie la victoire à partir du 9eme coup
                    win = self.check_win(ligne, colonne, jetonJoueur)

                    if win:
                        winner = jetonJoueur

        # Séquence de fin de partie : On nettoie et on affiche le résultat
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
        Fonction qui retourne les coups potentiels situés uniquement
        autour des jetons existants afin de limiter les calculs de l'IA.
        """
        res = []
        pieces = []

        # On trouve d'abord les jetons actuellement posés sur le plateau
        for i in range(15):
            for j in range(15):
                if self.board[i][j] != ' ':
                    pieces.append((i, j))

        # Si le plateau est complètement vide, on force l'IA à jouer au centre
        if not pieces:
            return [[7, 7]]

        # On ne génère des coups qu'autour des pièces existantes (dans un rayon de 2 cases)
        seen = set()
        for r, c in pieces:
            for dr in range(-2, 3):
                for dc in range(-2, 3):
                    nr, nc = r + dr, c + dc
                    # On s'assure de ne pas déborder et on ne garde que les cases vides
                    if 0 <= nr < 15 and 0 <= nc < 15 and self.board[nr][nc] == ' ':
                        if (nr, nc) not in seen:
                            seen.add((nr, nc))
                            res.append([nr, nc])

        return res

    def nouvellepartieMultilpayer(self, jeton=('O', 'X')):
        """ self x tuple -> None
        Fonction principale qui lance la partie de Gomoku en multijoueur (Humain contre Humain)
        """
        os.system('cls' if os.name == 'nt' else 'clear')
        # affichage de la grille initiale
        self.show_board()

        # Initialisation du dictionnaire de coordonnées (Génération de 'A' à 'J')
        for i in range(1, 11):
            self.conversion_lettres_entier[chr(65 + i - 1)] = i

        win = False
        count = 0

        # Boucle de jeu jusqu'à remplissage complet du plateau ou victoire
        while not win and count < self.nc * self.nl:
            count += 1
            # Alternance entre joueur 1 et joueur 2
            joueur = (count + 1) % 2 + 1

            while True:
                print(
                    f"Joueur {joueur} ({self.jeton[joueur - 1]}), Entre les coordonnées de l'endroit où tu vas jouer (A1, B2...)")

                # Historique rapide pour l'adversaire
                if count > 1: print(f"dernier coup joué par le joueur {self.jeton[joueur - 1]}: {coord}")
                coord = input('Cordonnées jouée: ')

                try:
                    # Sécurisation des données entrées
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

            # Placement du coup valide
            colonne = int(self.conversion_lettres_entier[(coord[0].upper())]) - 1
            ligne = int(coord[1:]) - 1
            self.board[ligne][colonne] = self.jeton[joueur - 1]

            # Actualisation visuelle du plateau pour le prochain joueur
            os.system('cls' if os.name == 'nt' else 'clear')
            self.show_board()

            if count > 8:  # on vérifie si un joueur a gagné partir du 9eme coup
                win = self.check_win(ligne, colonne, self.jeton[joueur - 1])

        # Annonce du gagnant de la manche
        if win:
            print(f"Le Joueur ayant le jeton ({self.jeton[joueur - 1]}) a gagné!")

        else:
            print("Match nul!")