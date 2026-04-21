import copy
import time
class AI:

    def __init__(self,jetonAI,jetonJoueur,depth,playstyle,eval_score):
        self.jetonAI = jetonAI
        self.jetonJoueur = jetonJoueur
        self.depth = depth
        self.playstyle = playstyle
        self.eval_score = eval_score
        self.dernierCoup = None
        self.tempsReflexion = None
        

    def getDernierCoup(self):
        return self.dernierCoup
    
    def getTempsReflexion(self):
        return self.tempsReflexion

    def evaluate (self,board):
        score_total = 0
        def analysefenetre(fenetre):
            nonlocal score_total
            if self.jetonAI in fenetre and self.jetonJoueur in fenetre:
                return
            elif self.jetonAI in fenetre and self.jetonJoueur not in fenetre:
                if fenetre.count(self.jetonAI) == 4:
                    score_total += 4000
                    return
                if self.playstyle == "agressif":
                    score_total += self.eval_score[fenetre.count(self.jetonAI)]*2
                else:
                    score_total += self.eval_score[fenetre.count(self.jetonAI)]
            elif self.jetonAI not in fenetre and self.jetonJoueur in fenetre:
                if fenetre.count(self.jetonJoueur) == 4:
                    score_total -= 9000
                    return
                if self.playstyle == "defensif":
                    score_total -= self.eval_score[fenetre.count(self.jetonJoueur)]*2
                else:
                    score_total -= self.eval_score[fenetre.count(self.jetonJoueur)]
        
        for ligne in board.board:
            for i in range(6):
                fenetre = ligne[i:i + 5]
                analysefenetre(fenetre)

        for i in range(10):
            for j in range(6):
                fenetre = [board.board[j+k][i] for k in range(5)]
                analysefenetre(fenetre)

        for i in range(4,10):
            for j in range(6):
                fenetre = [board.board[j+k][i-k] for k in range(5)]
                analysefenetre(fenetre)

        for i in range(6):
            for j in range(6):
                fenetre = [board.board[j+k][i+k] for k in range(5)]
                analysefenetre(fenetre)

        return score_total


    def minimax(self, board,depth,isMaximizing,alpha=float("-inf"),beta=float("inf"),dernier_coup=None):
        if dernier_coup is not None and board.check_victoire(dernier_coup[0],dernier_coup[1],self.jetonAI):
            return (100000,None)

        if dernier_coup is not None and board.check_victoire(dernier_coup[0],dernier_coup[1],self.jetonJoueur):
            return (-100000,None)

        if not board.get_remain_moves():
            return (0,None)

        if depth == 0:
            return (self.evaluate(board), 0)

        if isMaximizing:
            meilleur_score = float('-inf')
            meilleur_coup = None
            for coup in board.get_remain_moves():
                bckup = copy.deepcopy(board)
                bckup.board[coup[0]][coup[1]] = self.jetonAI
                score = self.minimax(bckup, depth-1, not isMaximizing,alpha,beta,dernier_coup=coup)
                if score[0] > meilleur_score:
                    meilleur_score = score[0]
                    meilleur_coup = coup
                alpha = max(alpha,meilleur_score)
                if beta <= alpha:
                    break
            return (meilleur_score, meilleur_coup)
        else:
            meilleur_score = float('+inf')
            meilleur_coup = None
            for coup in board.get_remain_moves():
                bckup = copy.deepcopy(board)
                bckup.board[coup[0]][coup[1]] = self.jetonJoueur
                score = self.minimax(bckup, depth - 1, not isMaximizing,alpha,beta,dernier_coup=coup)
                if score[0] < meilleur_score:
                    meilleur_score = score[0]
                    meilleur_coup = coup
                beta = min(beta,meilleur_score)
                if beta <= alpha:
                    break
            return (meilleur_score, meilleur_coup)

    def get_best_move(self,board):
        start = time.perf_counter()
        result = self.minimax(board,self.depth,True)
        end = time.perf_counter()
        self.tempsReflexion = end - start
        self.dernierCoup = f"{chr(65 + (result[1][1]))}{(result[1][0]+1)}"

        return result