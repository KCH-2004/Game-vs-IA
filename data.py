import ia
import game
import os
import csv

def IAMatch():
    gameStart = game.Puissance5()
    botTest1 = ia.AI('O','X', 1, 'agressif',{0:0,1: 1, 2: 5, 3: 50, 4: 500})
    botTest2 = ia.AI('X','O', 2, 'agressif',{0:0,1: 1, 2: 5, 3: 50, 4: 500})
    compteur = 0
    victoire = False
    gagnant = None

    while not victoire and compteur < 100:
        compteur += 1
        if botTest1.jetonAI == 'X':
            isAIturn = compteur % 2 == 0
        else:
            isAIturn = compteur % 2 == 1

        if isAIturn:
            result = botTest1.get_best_move(gameStart)
            gameStart.board[result[1][0]][result[1][1]] = botTest1.jetonAI
            if compteur > 6:  # on vérifie à partir du 7eme coup
                victoire = gameStart.check_victoire(result[1][0], result[1][1], botTest1.jetonAI)
                if victoire:
                    gagnant = botTest1.jetonAI
        else:
            result = botTest2.get_best_move(gameStart)
            gameStart.board[result[1][0]][result[1][1]] = botTest2.jetonAI
            if compteur > 6:  # on vérifie à partir du 7eme coup
                victoire = gameStart.check_victoire(result[1][0], result[1][1], botTest2.jetonAI)
                if victoire:
                    gagnant = botTest2.jetonAI

    os.system('cls' if os.name == 'nt' else 'clear')
    gameStart.show_board()
    if gagnant == botTest1.jetonAI:
        print("botTest1 a gagné!")
    elif gagnant == botTest2.jetonAI:
        print("botTest2 a gagné!")
    else:
        print("Match nul!")

#def analyseData():
