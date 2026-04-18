import copy

def minimax(board, depth, isMaximizing, jetonAI, jetonJoueur, eval_score_ouvert, eval_score_semi_ouvert, playstyle,alpha=float("-inf"),beta=float("inf"),dernier_coup=None):
    if dernier_coup is not None and board.check_victoire(dernier_coup[0],dernier_coup[1],jetonAI):
        return (10000,None)

    if dernier_coup is not None and board.check_victoire(dernier_coup[0],dernier_coup[1],jetonJoueur):
        return (-10000,None)

    if not board.get_remain_moves():
        return (0,None)

    if depth == 0:
        return (evaluate(board, jetonAI, jetonJoueur, eval_score_ouvert, eval_score_semi_ouvert, playstyle), 0)

    if isMaximizing:
        meilleur_score = float('-inf')
        meilleur_coup = None
        for coup in board.get_remain_moves():
            bckup = copy.deepcopy(board)
            bckup.board[coup[0]][coup[1]] = jetonAI
            score = minimax(bckup, depth-1, not isMaximizing, jetonAI, jetonJoueur,eval_score_ouvert, eval_score_semi_ouvert,playstyle,alpha,beta,dernier_coup=coup)
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
            bckup.board[coup[0]][coup[1]] = jetonJoueur
            score = minimax(bckup, depth - 1, not isMaximizing, jetonAI, jetonJoueur,eval_score_ouvert, eval_score_semi_ouvert,playstyle,alpha,beta,dernier_coup=coup)
            if score[0] < meilleur_score:
                meilleur_score = score[0]
                meilleur_coup = coup
            beta = min(beta,meilleur_score)
            if beta <= alpha:
                break
        return (meilleur_score, meilleur_coup)

def evaluate (board,jetonAI, jetonJoueur,eval_score_ouvert, eval_score_semi_ouvert, playstyle):
    score_total = 0

    def analysefenetre(fenetre,ouvertureA,ouvertureB):
        nonlocal score_total
        if jetonAI in fenetre and jetonJoueur in fenetre:
                return
        elif jetonAI in fenetre and jetonJoueur not in fenetre:
            if ouvertureA and ouvertureB:
                if playstyle == "agressif":
                    score_total += eval_score_ouvert[fenetre.count(jetonAI)]*2
                else:
                    score_total += eval_score_ouvert[fenetre.count(jetonAI)]
            elif ouvertureA or ouvertureB:
                if playstyle == "agressif":
                    score_total += eval_score_semi_ouvert[fenetre.count(jetonAI)]*2
                else:
                    score_total += eval_score_semi_ouvert[fenetre.count(jetonAI)]
        elif jetonAI not in fenetre and jetonJoueur in fenetre:
            if ouvertureA and ouvertureB:
                if playstyle == "defensif":
                    score_total -= eval_score_ouvert[fenetre.count(jetonJoueur)]*2
                else:
                    score_total -= eval_score_ouvert[fenetre.count(jetonJoueur)]
            elif ouvertureA or ouvertureB:
                if playstyle == "defensif":
                    score_total -= eval_score_semi_ouvert[fenetre.count(jetonJoueur)]*2
                else:
                    score_total -= eval_score_semi_ouvert[fenetre.count(jetonJoueur)]
        
    for ligne in board.board:
        for i in range(6):
            gauche_ouverte = (i > 0) and (ligne[i - 1] == ' ')
            droite_ouverte = (i + 5 < 10) and (ligne[i + 5] == ' ')
            fenetre = ligne[i:i + 5]
            analysefenetre(fenetre,gauche_ouverte,droite_ouverte)

    for i in range(6):
        for j in range(6):
            haut_ouverte = (j > 0) and (board.board[j-1][i] == ' ')
            bas_ouverte = (j+5 < 10) and (board.board[j+5][i] == ' ')
            fenetre = [board.board[j+k][i] for k in range(5)]
            analysefenetre(fenetre,haut_ouverte,bas_ouverte)

    for i in range(4,10):
        for j in range(6):
            diag_haute_ouverte = (j > 0) and (i < 9) and (board.board[j-1][i+1] == ' ')
            diag_basse_ouverte = (j+5 < 9) and (i-5 >= 0) and (board.board[j+5][i-5] == ' ')
            fenetre = [board.board[j+k][i-k] for k in range(5)]
            analysefenetre(fenetre,diag_haute_ouverte,diag_basse_ouverte)
    for i in range(6):
        for j in range(6):
            diag_haute_ouverte = (j > 0) and (i > 0) and (board.board[j-1][i-1] == ' ')
            diag_basse_ouverte = (j+5 < 9) and (i+5 < 9) and (board.board[j+5][i+5] == ' ')
            fenetre = [board.board[j+k][i+k] for k in range(5)]
            analysefenetre(fenetre,diag_haute_ouverte,diag_basse_ouverte)
    return score_total