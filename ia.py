import time
import random


class AI:

    def __init__(self, jetonAI, jetonJoueur, depth, playstyle, heuristic = "exponentielle"):
        """Constructeur: Crée l'IA"""
        self.jetonAI = jetonAI
        self.jetonJoueur = jetonJoueur
        self.depth = depth
        self.playstyle = playstyle
        self.dernierCoup = None
        self.tempsReflexion = None

        self.memoization = {}
        self.eval_score = None

        if heuristic == "linéaire":
            self.eval_score = {0: 0, 1: 10, 2: 20, 3: 30, 4: 40, 5: 50}
        else:
            self.eval_score = {0: 0, 1: 2, 2: 20, 3: 200, 4: 20000, 5: 2000000}

    def getDernierCoup(self):
        """self -> string
        retourne le dernier coup sous forme de string"""
        return self.dernierCoup

    def getTempsReflexion(self):
        """self->int
        retourne le temps de reflexion de l'IA"""
        return self.tempsReflexion

    def get_window_score(self, fenetre):
        """self x list -> int
        retourne un score selon une fenetre de 5"""

        if self.jetonAI in fenetre and self.jetonJoueur in fenetre:
        #Si les jetons de l'IA et du joueur sont dans la fenêtre:
        #Alors il n'y a pas de coup gagnant possible, on retourne donc 0
            return 0

        score = 0
        if self.jetonAI in fenetre:
            count = fenetre.count(self.jetonAI) #On compte le nombre de jetons dans cette position
            points = self.eval_score[count] #On le traduit en points via le score d'évaluation de l'IA
            #On vérifie s'il s'agit d'un alignement direct ou d'un alignement partiel de 4 jetons
            if count == 4:
                chaine = "".join(fenetre)
                #S'il s'agit d'un alignement partiel, alors on baisse la priorité du coup, car facilement blocable
                if (self.jetonAI * 4) not in chaine:
                    points /= 10
            #Si la version de l'IA est agressive, alors on ajoute un bonus pour le gain
            if self.playstyle == "agressif":
                points = int(points * 1.5)
            score += points

        elif self.jetonJoueur in fenetre:
            count = fenetre.count(self.jetonJoueur)
            #Une menace est prioritaire par rapport à une opportunité équivalente
            points = self.eval_score[count] * 2
            if count == 4:
                chaine = "".join(fenetre)
                if (self.jetonJoueur * 4) not in chaine:
                    points /= 5
            #Cas spécifique pour la profondeur de 1: Elle ne "voit pas" les menaces de 4 jetons alignés.
            # On attribue donc une valeur manuellement
            if count >= 4 and self.depth == 1:
               points = 150000

            if self.playstyle == "defensif":
                points = int(points * 1.5)
            score -= points

        return score

    def heuristic(self, board):
        """object Gomoku -> int
        Parcours l'ensemble du plateau via une fenêtre glissante
        retourne le score total de cette position
        """
        score_total = 0
        #parcours en colonne
        for ligne in board.board:
            for i in range(11):
                score_total += self.get_window_score(ligne[i:i + 5])
        #parcours en ligne
        for i in range(15):
            for j in range(11):
                score_total += self.get_window_score([board.board[j + k][i] for k in range(5)])
        #parcours en diagonale (\)
        for i in range(4, 15):
            for j in range(6):
                score_total += self.get_window_score([board.board[j + k][i - k] for k in range(5)])
        #parcours dans l'autre diagonale (/)
        for i in range(11):
            for j in range(11):
                score_total += self.get_window_score([board.board[j + k][i + k] for k in range(5)])
        return score_total

    def evaluate_local(self, board, r, c):
        """self x object Gomoku x int x int -> int
        Évalue et retourne le score local autour d'une case donnée (r, c) sur les 4 axes.
        Cela évite de recalculer tout le plateau à chaque coup."""
        score = 0

        # Axe Horizontal : on récupère les 5 cases autour de (r,c) sur la même ligne
        for i in range(max(0, c - 4), min(11, c + 1)):
            fenetre = board.board[r][i:i + 5]
            score += self.get_window_score(fenetre)

        # Axe Vertical : on récupère les 5 cases autour de (r,c) sur la même colonne
        for i in range(max(0, r - 4), min(11, r + 1)):
            fenetre = [board.board[i + k][c] for k in range(5)]
            score += self.get_window_score(fenetre)
        # Diagonale Principale (\)
        for k in range(-4, 1):
            r_start, c_start = r + k, c + k
            if 0 <= r_start <= 10 and 0 <= c_start <= 10:
                fenetre = [board.board[r_start + i][c_start + i] for i in range(5)]
                score += self.get_window_score(fenetre)
        # Diagonale Secondaire (/)
        for k in range(-4, 1):
            r_start, c_start = r + k, c - k
            if 0 <= r_start <= 10 and 4 <= c_start <= 14:
                fenetre = [board.board[r_start + i][c_start - i] for i in range(5)]
                score += self.get_window_score(fenetre)
        return score

    def get_top_moves(self, board, max_moves):
        """self x object Gomoku x int -> list
        Trie et retourne les meilleurs coups possibles pour restreindre l'arbre de recherche (Beam Search).
        Permet au Minimax de se concentrer uniquement sur les coups les plus pertinents."""
        moves = board.get_remain_moves()
        # S'il y a très peu de coups, on les renvoie directement
        if len(moves) <= 1:
            return moves

        scores = []
        for move in moves:
            r, c = move
            score_avant = self.evaluate_local(board, r, c)

            # Simulation 1 : Potentiel si l'IA joue sur cette case
            board.board[r][c] = self.jetonAI
            score_apres_IA = self.evaluate_local(board, r, c)
            delta_IA = score_apres_IA - score_avant
            board.board[r][c] = ' ' #On remet la case vide

            #Simulation 2 : Potentiel si le Joueur adverse joue sur cette case (pour bloquer)
            board.board[r][c] = self.jetonJoueur
            score_apres_Joueur = self.evaluate_local(board, r, c)
            delta_Joueur = score_avant - score_apres_Joueur
            board.board[r][c] = ' '

            # Le potentiel du coup combine l'attaque (delta_IA) et la défense (delta_Joueur)
            potentiel = delta_IA + delta_Joueur
            # Bonus de centralité : On favorise légèrement les coups proches du centre (7,7)
            potentiel -= (abs(7 - r) + abs(7 - c)) * 0.1
            scores.append((potentiel, move))

        # Tri de la liste de manière décroissante (les plus hauts potentiels en premier)
        scores.sort(key=lambda x: x[0], reverse=True)

        # On retourne uniquement les coordonnées des 'max_moves' meilleurs coups
        return [m[1] for m in scores[:max_moves]]

    def minimax(self, board, depth, isMaximizing, current_score, alpha=float("-inf"), beta=float("inf"), dernier_coup=None):
        """self x object Gomoku x int x bool x int x float x float x tuple -> tuple
                Algorithme de recherche Minimax avec élagage Alpha-Bêta et Table de Transposition.
                Retourne un tuple contenant (meilleur_score, meilleur_coup)."""

        # Création d'une clé unique pour le plateau actuel (Table de Transposition)
        hash_key = tuple(tuple(ligne) for ligne in board.board)
        alpha_original = alpha
        beta_original = beta

        # Vérification si cette position a déjà été calculée précédemment (Memoization)
        if hash_key in self.memoization:
            entree = self.memoization[hash_key]
            if entree['depth'] >= depth:
                if entree['flag'] == 'EXACT':
                    return entree['value'], entree['best_move']
                elif entree['flag'] == 'LOWERBOUND':
                    alpha = max(alpha, entree['value'])
                elif entree['flag'] == 'UPPERBOUND':
                    beta = min(beta, entree['value'])
                if alpha >= beta: return entree['value'], entree['best_move']

        # Conditions de fin de partie (Victoire de l'IA)
        if dernier_coup is not None and board.check_win(dernier_coup[0], dernier_coup[1], self.jetonAI):
            return (20000000 + depth, None)

        # Conditions de fin de partie (Victoire du Joueur)
        if dernier_coup is not None and board.check_win(dernier_coup[0], dernier_coup[1], self.jetonJoueur):
            return (-20000000 - depth, None)

        # Condition d'arrêt : profondeur atteinte ou plateau rempli
        if depth == 0 or not board.get_remain_moves():
            return (current_score, None)

        tt_best_move = None
        if hash_key in self.memoization:
            tt_best_move = self.memoization[hash_key].get('best_move')

        meilleurs_coups = []

        # Beam search: plus la profondeur du minimax est basse, plus on réduit le nombre de coups explorés
        dynamic_max = 12 if depth >= 3 else 8
        top_moves = self.get_top_moves(board, dynamic_max)

        # Move Ordering : On place le coup de la Table de Transposition en premier s'il existe
        if tt_best_move in top_moves:
            top_moves.remove(tt_best_move)
            top_moves.insert(0, tt_best_move)

        # Tour de l'IA (On cherche à maximiser le score)
        if isMaximizing:
            meilleur_score = float('-inf')
            for coup in top_moves:
                r, c = coup
                score_avant = self.evaluate_local(board, r, c)
                board.board[r][c] = self.jetonAI
                score_apres = self.evaluate_local(board, r, c)
                nouveau_score = current_score - score_avant + score_apres

                score = self.minimax(board, depth - 1, False, nouveau_score, alpha, beta, dernier_coup=coup)
                board.board[r][c] = ' '

                if score[0] > meilleur_score:
                    meilleur_score = score[0]
                    meilleurs_coups = [coup]
                elif score[0] == meilleur_score:
                    meilleurs_coups.append(coup)

                alpha = max(alpha, meilleur_score)
                # Élagage Alpha-Bêta : on coupe la branche si on sait que l'adversaire l'évitera
                if beta <= alpha: break

        # Tour du Joueur adverse (On cherche à minimiser le score)
        else:
            meilleur_score = float('+inf')
            for coup in top_moves:
                r, c = coup
                score_avant = self.evaluate_local(board, r, c)
                board.board[r][c] = self.jetonJoueur
                score_apres = self.evaluate_local(board, r, c)
                nouveau_score = current_score - score_avant + score_apres

                score = self.minimax(board, depth - 1, True, nouveau_score, alpha, beta, dernier_coup=coup)
                board.board[r][c] = ' '

                if score[0] < meilleur_score:
                    meilleur_score = score[0]
                    meilleurs_coups = [coup]
                elif score[0] == meilleur_score:
                    meilleurs_coups.append(coup)

                beta = min(beta, meilleur_score)
                # Élagage Alpha-Bêta
                if beta <= alpha: break

        # S'il y a plusieurs coups à égalité, on en choisit un au hasard pour varier le jeu
        meilleur_coup_choisi = random.choice(meilleurs_coups) if meilleurs_coups else None

        # Sauvegarde du résultat dans la Table de Transposition
        flag = 'EXACT'
        if meilleur_score <= alpha_original:
            flag = 'UPPERBOUND'
        elif meilleur_score >= beta_original:
            flag = 'LOWERBOUND'

        self.memoization[hash_key] = {
            'value': meilleur_score, 'depth': depth, 'flag': flag, 'best_move': meilleur_coup_choisi
        }

        return (meilleur_score, meilleur_coup_choisi)

    def get_best_move(self, board):
        """self x object Gomoku -> tuple
            Point d'entrée principal pour faire jouer l'IA.
            Utilise l'Iterative Deepening pour chercher le meilleur coup et mesure le temps de calcul."""
        self.memoization = {} # Réinitialisation de la mémoire pour ce nouveau tour
        start = time.perf_counter() # Démarrage du chronomètre

        initial_score = self.heuristic(board)
        meilleur_coup_final = None

        # Iterative Deepening : On cherche d'abord à profondeur 1, puis 2, etc.
        # Cela permet d'ordonner l'arbre et d'améliorer considérablement l'élagage Alpha-Bêta
        for d in range(1, self.depth + 1):
            resultat = self.minimax(board, d, True, current_score=initial_score)
            meilleur_coup_final = resultat
            if resultat[0] > 100000:  # Victoire trouvée grâce à Iterative Deepening
                break

        end = time.perf_counter()
        self.tempsReflexion = end - start # Mise à jour du temps de calcul
        # Formatage du dernier coup ( "G4")
        if meilleur_coup_final and meilleur_coup_final[1]:
            self.dernierCoup = f"{chr(65 + (meilleur_coup_final[1][1]))}{(meilleur_coup_final[1][0] + 1)}"
        else:
            self.dernierCoup = None

        return meilleur_coup_final