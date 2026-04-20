import copy

def minimax(board, depth, isMaximizing, jetonAI, jetonJoueur, eval_score_ouvert, playstyle,alpha=float("-inf"),beta=float("inf"),dernier_coup=None):
    if dernier_coup is not None and board.check_victoire(dernier_coup[0],dernier_coup[1],jetonAI):
        return (100000,None)

    if dernier_coup is not None and board.check_victoire(dernier_coup[0],dernier_coup[1],jetonJoueur):
        return (-100000,None)

    if not board.get_remain_moves():
        return (0,None)

    if depth == 0:
        return (evaluate(board, jetonAI, jetonJoueur, eval_score_ouvert, playstyle), 0)

    if isMaximizing:
        meilleur_score = float('-inf')
        meilleur_coup = None
        for coup in board.get_remain_moves():
            bckup = copy.deepcopy(board)
            bckup.board[coup[0]][coup[1]] = jetonAI
            score = minimax(bckup, depth-1, not isMaximizing, jetonAI, jetonJoueur,eval_score_ouvert, playstyle,alpha,beta,dernier_coup=coup)
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
            score = minimax(bckup, depth - 1, not isMaximizing, jetonAI, jetonJoueur,eval_score_ouvert, playstyle,alpha,beta,dernier_coup=coup)
            if score[0] < meilleur_score:
                meilleur_score = score[0]
                meilleur_coup = coup
            beta = min(beta,meilleur_score)
            if beta <= alpha:
                break
        return (meilleur_score, meilleur_coup)

def evaluate (board,jetonAI, jetonJoueur,eval_score_ouvert, playstyle):
    score_total = 0

    def analysefenetre(fenetre):
        nonlocal score_total
        if jetonAI in fenetre and jetonJoueur in fenetre:
                return
        elif jetonAI in fenetre and jetonJoueur not in fenetre:
            if fenetre.count(jetonAI) == 4:
                score_total += 4000
                return
            if playstyle == "agressif":
                score_total += eval_score_ouvert[fenetre.count(jetonAI)]*2
            else:
                score_total += eval_score_ouvert[fenetre.count(jetonAI)]
        elif jetonAI not in fenetre and jetonJoueur in fenetre:
            if fenetre.count(jetonJoueur) == 4:
                score_total -= 9000
                return
            if playstyle == "defensif":
                score_total -= eval_score_ouvert[fenetre.count(jetonJoueur)]*2
            else:
                score_total -= eval_score_ouvert[fenetre.count(jetonJoueur)]
        
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