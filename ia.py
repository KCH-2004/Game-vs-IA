import copy

def minimax(board, depth, isMaximizing,jetonAI, jetonJoueur,dernier_coup=None):
    if dernier_coup is not None and board.check_victoire(dernier_coup[0],dernier_coup[1],jetonAI):
        return (10000,None)

    if dernier_coup is not None and board.check_victoire(dernier_coup[0],dernier_coup[1],jetonJoueur):
        return (-10000,None)

    if not board.get_remain_moves():
        return (0,None)

    if depth == 0:
        return (evaluate(board,jetonAI,jetonJoueur),0)

    if isMaximizing == True:
        meilleur_score = float('-inf')
        meilleur_coup = None
        for coup in board.get_remain_moves():
            bckup = copy.deepcopy(board)
            bckup.board[coup[0]][coup[1]] = jetonAI
            score = minimax(bckup, depth-1, not isMaximizing, jetonAI, jetonJoueur,dernier_coup=coup)
            if score[0] > meilleur_score:
                meilleur_score = score[0]
                meilleur_coup = coup
        return (meilleur_score, meilleur_coup)
    else:
        meilleur_score = float('+inf')
        meilleur_coup = None
        for coup in board.get_remain_moves():
            bckup = copy.deepcopy(board)
            bckup.board[coup[0]][coup[1]] = jetonJoueur
            score = minimax(bckup, depth - 1, not isMaximizing, jetonAI, jetonJoueur,dernier_coup=coup)
            if score[0] < meilleur_score:
                meilleur_score = score[0]
                meilleur_coup = coup
        return (meilleur_score, meilleur_coup)

def evaluate (board,jetonAI, jetonJoueur,eval_score_ouvert, eval_score_semi_ouvert):
    eval_score_ouvert = {1: 1, 2: 5, 3: 50, 4: 1000}
    eval_score_semi_ouvert = {1: 0, 2: 1, 3: 10, 4: 1000}
    score_total = 0

    for ligne in board.board:
        for i in range(6):
            gauche_ouverte = (i > 0) and (ligne[i - 1] == ' ')
            droite_ouverte = (i + 5 < 9) and (ligne[i + 5] == ' ')
            fenetre = ligne[i:i + 5]
            if jetonAI in fenetre and jetonJoueur in fenetre:
                continue
            elif jetonAI in fenetre and jetonJoueur not in fenetre:
                if gauche_ouverte and droite_ouverte:
                    score_total += eval_score_ouvert[fenetre.count(jetonAI)]
                elif gauche_ouverte or droite_ouverte:
                    score_total += eval_score_semi_ouvert[fenetre.count(jetonAI)]
            elif jetonAI not in fenetre and jetonJoueur in fenetre:
                if gauche_ouverte and droite_ouverte:
                    score_total -= eval_score_ouvert[fenetre.count(jetonJoueur)]
                elif gauche_ouverte or droite_ouverte:
                    score_total -= eval_score_semi_ouvert[fenetre.count(jetonJoueur)]

    for i in range(6):
        for j in range(6):
            fenetre = [board.board[j+k][i] for k in range(5)]
            haut_ouverte = (j > 0) and (board.board[j-1][i] == ' ')
            bas_ouverte = (j+5 < 9) and (board.board[j+5][i] == ' ')
            if jetonAI in fenetre and jetonJoueur in fenetre:
                continue
            elif jetonAI in fenetre and jetonJoueur not in fenetre:
                if haut_ouverte and bas_ouverte:
                    score_total += eval_score_ouvert[fenetre.count(jetonAI)]
                elif haut_ouverte or bas_ouverte:
                    score_total += eval_score_semi_ouvert[fenetre.count(jetonAI)]
            elif jetonAI not in fenetre and jetonJoueur in fenetre:
                if haut_ouverte and bas_ouverte:
                    score_total -= eval_score_ouvert[fenetre.count(jetonJoueur)]
                elif haut_ouverte or bas_ouverte:
                    score_total -= eval_score_semi_ouvert[fenetre.count(jetonJoueur)]

    for i in range(4,10):
        for j in range(6):
            diag_haute_ouverte = (j > 0) and (i < 9) and (board.board[j-1][i+1] == ' ')
            diag_basse_ouverte = (j+5 < 9) and (i-5 >= 0) and (board.board[j+5][i-5] == ' ')
            fenetre = [board.board[j+k][i-k] for k in range(5)]
            if jetonAI in fenetre and jetonJoueur in fenetre:
                continue
            elif jetonAI in fenetre and jetonJoueur not in fenetre:
                if diag_haute_ouverte and diag_basse_ouverte:
                    score_total += eval_score_ouvert[fenetre.count(jetonAI)]
                elif diag_haute_ouverte or diag_basse_ouverte:
                    score_total += eval_score_semi_ouvert[fenetre.count(jetonAI)]
            elif jetonAI not in fenetre and jetonJoueur in fenetre:
                if diag_haute_ouverte and diag_basse_ouverte:
                    score_total -= eval_score_ouvert[fenetre.count(jetonJoueur)]
                elif diag_haute_ouverte or diag_basse_ouverte:
                    score_total -= eval_score_semi_ouvert[fenetre.count(jetonJoueur)]

    for i in range(6):
        for j in range(6):
            diag_haute_ouverte = (j > 0) and (i > 0) and (board.board[j-1][i-1] == ' ')
            diag_basse_ouverte = (j+5 < 9) and (i+5 < 9) and (board.board[j+5][i+5] == ' ')
            fenetre = [board.board[j+k][i+k] for k in range(5)]
            if jetonAI in fenetre and jetonJoueur in fenetre:
                continue
            elif jetonAI in fenetre and jetonJoueur not in fenetre:
                if diag_haute_ouverte and diag_basse_ouverte:
                    score_total += eval_score_ouvert[fenetre.count(jetonAI)]
                elif diag_haute_ouverte or diag_basse_ouverte:
                    score_total += eval_score_semi_ouvert[fenetre.count(jetonAI)]
            elif jetonAI not in fenetre and jetonJoueur in fenetre:
                if diag_haute_ouverte and diag_basse_ouverte:
                    score_total -= eval_score_ouvert[fenetre.count(jetonJoueur)]
                elif diag_haute_ouverte or diag_basse_ouverte:
                    score_total -= eval_score_semi_ouvert[fenetre.count(jetonJoueur)]

    return score_total