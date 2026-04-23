import ia
import game
import csv

def IAMatch(bot1,bot2):

    gameStart = game.Puissance5()
    compteur = 0
    victoire = False
    gagnant = None
    bot1Data = {"estGagnant":False,"tpsReflexionMoy": 0} 
    bot2Data = {"estGagnant":False,"tpsReflexionMoy": 0}
    isBot1Starting = bot1.jetonAI == 'O'

    while not victoire and compteur < 100:
        compteur += 1
        if isBot1Starting:
            isBot1turn = compteur % 2 == 1

        else:
            isBot1turn = compteur % 2 == 0

        if isBot1turn:
            result = bot1.get_best_move(gameStart)
            bot1Data['tpsReflexionMoy'] += bot1.getTempsReflexion()
            gameStart.board[result[1][0]][result[1][1]] = bot1.jetonAI

            if compteur > 6:  # on vérifie à partir du 7eme coup
                victoire = gameStart.check_victoire(result[1][0], result[1][1], bot1.jetonAI)

                if victoire:
                    gagnant = bot1.jetonAI

        else:
            result = bot2.get_best_move(gameStart)
            bot2Data['tpsReflexionMoy'] += bot2.getTempsReflexion()
            gameStart.board[result[1][0]][result[1][1]] = bot2.jetonAI

            if compteur > 6:  # on vérifie à partir du 7eme coup
                victoire = gameStart.check_victoire(result[1][0], result[1][1], bot2.jetonAI)

                if victoire:
                    gagnant = bot2.jetonAI
    """if gagnant == bot1.jetonAI:
        gameStart.show_board()
        print("Bot 1 Winner")
    else:
        gameStart.show_board()
        print("Bot 2 Winner")"""

    if gagnant == bot1.jetonAI:

        if isBot1Starting: #Si le bot1 a commencé et a gagné (son nombre de coups est donc impair)
            bot1Data['tpsReflexionMoy'] /= ((compteur//2) + 1)
            bot2Data['tpsReflexionMoy'] /= compteur//2

        else: #Dans le cas contraire, le coup gagnant est sur un compteur pair
            bot1Data['tpsReflexionMoy'] /= compteur//2
            bot2Data['tpsReflexionMoy'] /= compteur//2
        bot1Data['estGagnant'] = True
        bot2Data['estGagnant'] = False

        return bot1Data,bot2Data
    
    elif gagnant == bot2.jetonAI:

        if not isBot1Starting: #Même logique ici
            bot2Data['tpsReflexionMoy'] /= ((compteur//2) + 1)
            bot1Data['tpsReflexionMoy'] /= compteur//2

        else: #Dans le cas contraire, le coup gagnant est sur un compteur pair
            bot2Data['tpsReflexionMoy'] /= compteur//2
            bot1Data['tpsReflexionMoy'] /= compteur//2

        bot2Data['estGagnant'] = True
        bot1Data['estGagnant'] = False

        return bot1Data,bot2Data
    
    else: 
        bot1Data['tpsReflexionMoy'] /= compteur//2
        bot2Data['tpsReflexionMoy'] /= compteur//2
        bot1Data['estGagnant'] = False
        bot2Data['estGagnant'] = False

        return bot1Data,bot2Data

def analyseData():

    #Nommage des différents IA: bot + profondeur du minimax + Style de jeu + Si commence
    bot1AgroStart = ia.AI('O','X',1,"Agressif")
    bot1AgroNotStart = ia.AI('X','O',1,"Agressif")

    bot1DefStart = ia.AI('O','X',1,"Defensif")
    bot1DefNotStart = ia.AI('X','O',1,"Defensif")

    bot2AgroStart = ia.AI('O','X',2,"Agressif")
    bot2AgroNotStart = ia.AI('X','O',2,"Agressif")
    
    bot2DefStart = ia.AI('O','X',2,"Defensif")
    bot2DefNotStart = ia.AI('X','O',2,"Defensif")

    bot3AgroStart = ia.AI('O','X',3,"Agressif")
    bot3AgroNotStart = ia.AI('X','O',3,"Agressif")

    bot3DefStart = ia.AI('O','X',3,"Defensif")
    bot3DefNotStart = ia.AI('X','O',3,"Defensif")

    #Nommage des données: + data + nom de l'IA
    for i in range(55):

        dataBot1AgroStart, dataBot1AgroNotStart = IAMatch(bot1AgroStart,bot1AgroNotStart)
        dataBot2AgroStart, dataBot2AgroNotStart = IAMatch(bot2AgroStart,bot2AgroNotStart)
        dataBot3AgroStart, dataBot3AgroNotStart = IAMatch(bot3AgroStart,bot3AgroNotStart)


        dataBot1DefStart, dataBot1DefNotStart = IAMatch(bot1DefStart,bot1DefNotStart)
        dataBot2DefStart, dataBot2DefNotStart = IAMatch(bot2DefStart,bot2DefNotStart)
        dataBot3DefStart, dataBot3DefNotStart = IAMatch(bot3DefStart,bot3DefNotStart)


        dataBot1AgroStart, dataBot2AgroNotStart
        dataBot2AgroStart, dataBot1AgroNotStart

        dataBot1AgroStart, dataBot3AgroNotStart
        dataBot3AgroStart, dataBot1AgroNotStart
        
        dataBot2AgroStart, dataBot3AgroNotStart
        dataBot3AgroStart, dataBot2AgroNotStart


        dataBot1DefStart, dataBot2DefNotStart
        dataBot2DefStart, dataBot1DefNotStart

        dataBot1DefStart, dataBot3DefNotStart
        dataBot3DefStart, dataBot1DefNotStart

        dataBot2DefStart, dataBot3DefNotStart
        dataBot3DefStart, dataBot2DefNotStart


        dataBot1AgroStart, dataBot1DefNotStart = IAMatch(bot1AgroStart,bot1DefNotStart)
        dataBot1DefStart, dataBot1AgroNotStart = IAMatch(bot1DefStart,bot1AgroNotStart)

        dataBot2AgroStart, dataBot2DefNotStart = IAMatch(bot2AgroStart,bot2DefNotStart)
        dataBot2DefStart, dataBot2AgroNotStart = IAMatch(bot2DefStart,bot2AgroNotStart)

        dataBot3DefStart, dataBot3AgroNotStart = IAMatch(bot3DefStart,bot3AgroNotStart)
        dataBot3AgroStart, dataBot3DefNotStart = IAMatch(bot3AgroStart,bot3DefNotStart)


        dataBot1AgroStart, dataBot2AgroNotStart
        dataBot2AgroStart, dataBot1AgroNotStart

        dataBot1AgroStart, dataBot3AgroNotStart
        dataBot3AgroStart, dataBot1AgroNotStart
        
        dataBot2AgroStart, dataBot3AgroNotStart
        dataBot3AgroStart, dataBot2AgroNotStart


        dataBot1DefStart, dataBot2DefNotStart
        dataBot2DefStart, dataBot1DefNotStart

        dataBot1DefStart, dataBot3DefNotStart
        dataBot3DefStart, dataBot1DefNotStart

        dataBot2DefStart, dataBot3DefNotStart
        dataBot3DefStart, dataBot2DefNotStart


        dataBot1AgroStart, dataBot2AgroNotStart
        dataBot2AgroStart, dataBot1AgroNotStart

        dataBot1AgroStart, dataBot3AgroNotStart
        dataBot3AgroStart, dataBot1AgroNotStart
        
        dataBot2AgroStart, dataBot3AgroNotStart
        dataBot3AgroStart, dataBot2AgroNotStart


        dataBot1DefStart, dataBot2DefNotStart
        dataBot2DefStart, dataBot1DefNotStart

        dataBot1DefStart, dataBot3DefNotStart
        dataBot3DefStart, dataBot1DefNotStart

        dataBot2DefStart, dataBot3DefNotStart
        dataBot3DefStart, dataBot2DefNotStart



    if databot1['estGagnant']:
        print(f"Le bot 1 a gagné, temps de réflexion moyen: {databot1['tpsReflexionMoy']:.3f} sec")
        print(f"Le bot 2 a perdu, temps de réflexion moyen: {databot2['tpsReflexionMoy']:.3f} sec")

    elif databot2['estGagnant']:
        print(f"Le bot 2 a gagné, temps de réflexion moyen: {databot2['tpsReflexionMoy']:.3f} sec")
        print(f"Le bot 1 a perdu, temps de réflexion moyen: {databot1['tpsReflexionMoy']:.3f} sec")

    else:
        print(f"Match nul, Temps de réflexion du bot 1 {databot1['tpsReflexionMoy']:.3f} sec")
        print(f"           Temps de réflexion du bot 2 {databot2['tpsReflexionMoy']:.3f} sec")