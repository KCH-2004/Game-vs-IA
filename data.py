import ia
import game
import csv
import itertools

class IAStats:

    def __init__(self, nomIA):
        self.nomIA = nomIA
        self.victoires = 0
        self.nuls = 0
        self.defaites = 0
        self.tps_total = 0
        self.coups_totaux = 0
        self.matchups = {}

    def get_winrate(self):
        return (self.victoires / (self.nuls + self.defaites + self.victoires)) * 100
    
    def get_average_time(self):
        return self.tps_total/self.coups_totaux
    
    def get_nom(self):
        return self.nomIA
    
    def add_matchup(self, datas, matchup):
        self.matchups.setdefault(matchup, {"victoires": 0, "defaites": 0, "nuls": 0})
        match datas["estGagnant"]:

            case True:
                self.victoires +=1
                self.matchups[matchup]["victoires"] += 1

            case False:
                self.defaites +=1
                self.matchups[matchup]["defaites"] += 1

            case _:
                self.nuls +=1
                self.matchups[matchup]["nuls"] += 1
        
        self.tps_total += datas["tpsReflexion"]
        self.coups_totaux += datas["nbCoups"]
    
    def get_matchup(self):
        return self.matchups

def IAMatch(bot1,bot2):

    gameStart = game.Puissance5()
    compteur = 0
    victoire = False
    gagnant = None
    bot1Data = {"estGagnant":False,"tpsReflexion": 0, "nbCoups": 0} 
    bot2Data = {"estGagnant":False,"tpsReflexion": 0, "nbCoups": 0}
    isBot1Starting = bot1.jetonAI == 'O'

    while not victoire and compteur < 100:
        compteur += 1
        if isBot1Starting:
            isBot1turn = compteur % 2 == 1

        else:
            isBot1turn = compteur % 2 == 0

        if isBot1turn:
            result = bot1.get_best_move(gameStart)
            bot1Data['tpsReflexion'] += bot1.getTempsReflexion()
            gameStart.board[result[1][0]][result[1][1]] = bot1.jetonAI

            if compteur > 6:  # on vérifie à partir du 7eme coup
                victoire = gameStart.check_victoire(result[1][0], result[1][1], bot1.jetonAI)

                if victoire:
                    gagnant = bot1.jetonAI

        else:
            result = bot2.get_best_move(gameStart)
            bot2Data['tpsReflexion'] += bot2.getTempsReflexion()
            gameStart.board[result[1][0]][result[1][1]] = bot2.jetonAI

            if compteur > 6:  # on vérifie à partir du 7eme coup
                victoire = gameStart.check_victoire(result[1][0], result[1][1], bot2.jetonAI)

                if victoire:
                    gagnant = bot2.jetonAI
    """if gagnant == bot1.jetonAI: #Vérification du résultat (Si les bots jouent bien, 
                                                              si la partie est différente de la précédente)
        gameStart.show_board()
        print("Bot 1 Winner")
    else:
        gameStart.show_board()
        print("Bot 2 Winner")"""

    if gagnant == bot1.jetonAI:

        if isBot1Starting: #Si le bot1 a commencé et a gagné (son nombre de coups est donc impair)
            bot1Data['nbCoups'] /= ((compteur//2) + 1)
            bot2Data['nbCoups'] /= compteur//2

        else: #Dans le cas contraire, le coup gagnant est sur un compteur pair
            bot1Data['nbCoups'] /= compteur//2
            bot2Data['nbCoups'] /= compteur//2

        bot1Data['estGagnant'] = True
        bot2Data['estGagnant'] = False
    
    elif gagnant == bot2.jetonAI:

        if not isBot1Starting: #Même logique ici
            bot2Data['nbCoups'] /= ((compteur//2) + 1)
            bot1Data['nbCoups'] /= compteur//2

        else: #Dans le cas contraire, le coup gagnant est sur un compteur pair
            bot2Data['nbCoups'] /= compteur//2
            bot1Data['nbCoups'] /= compteur//2

        bot2Data['estGagnant'] = True
        bot1Data['estGagnant'] = False

    else: 
        bot1Data['nbCoups'] /= compteur//2
        bot2Data['nbCoups'] /= compteur//2
        bot1Data['estGagnant'] = None
        bot2Data['estGagnant'] = None

    return bot1Data,bot2Data

def analyseData():
    winrateStarting, winrateNotStarting, draw, games= 0, 0, 0, 0

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

    #Création d'objets permettant de stocker efficacement les données
    bot1AgroStats = IAStats("bot1AgroStats")
    bot2AgroStats = IAStats("bot2AgroStats")
    bot3AgroStats = IAStats("bot3AgroStats")
    bot1DefStats = IAStats("bot1DefStats")
    bot2DefStats = IAStats("bot2DefStats")
    bot3DefStats = IAStats("bot3DefStats")

    IAs = [
        {"nom": "bot1Agro", "start": bot1AgroStart, "not_start": bot1AgroNotStart, "stats": bot1AgroStats},
        {"nom": "bot2Agro", "start": bot2AgroStart, "not_start": bot2AgroNotStart, "stats": bot2AgroStats},
        {"nom": "bot3Agro", "start": bot3AgroStart, "not_start": bot3AgroNotStart, "stats": bot3AgroStats},
        {"nom": "bot1Def", "start": bot1DefStart, "not_start": bot1DefNotStart, "stats": bot1DefStats},
        {"nom": "bot2Def", "start": bot2DefStart, "not_start": bot2DefNotStart, "stats": bot2DefStats},
        {"nom": "bot3Def", "start": bot3DefStart, "not_start": bot3DefNotStart, "stats": bot3DefStats}
    ]

    print("Analyse data: Bot identique")

    for i in range(50):

        for bot in IAs:
            data_start, data_not_start = IAMatch(bot["start"], bot["not_start"])
            bot["stats"].add_matchup(data_start, bot["nom"])
            bot["stats"].add_matchup(data_not_start, bot["nom"])

            if data_start["estGagnant"]:
                winrateStarting += 1
            elif data_not_start["estGagnant"]:
                winrateNotStarting += 1
            else:
                draw += 1
            games += 1

        print(f"tour{i}")
    print("Analyse data: Bot qui jouent entre eux")

    for i in range(25):

        for botA, botB in itertools.combinations(IAs, 2):
            dataA_1, dataB_1 = IAMatch(botA["start"], botB["not_start"])
            botA["stats"].add_matchup(dataA_1, botB["nom"])
            botB["stats"].add_matchup(dataB_1, botA["nom"])

            if dataA_1["estGagnant"]:
                winrateStarting += 1

            elif dataB_1["estGagnant"]:
                winrateNotStarting += 1

            else:
                draw += 1

            games += 1

            dataB_2, dataA_2 = IAMatch(botB["start"], botA["not_start"])
            botB["stats"].add_matchup(dataB_2, botA["nom"])
            botA["stats"].add_matchup(dataA_2, botB["nom"])

            if dataB_2["estGagnant"]:
                winrateStarting += 1

            elif dataA_2["estGagnant"]:
                winrateNotStarting += 1

            else:
                draw += 1

            games += 1
        print(f"tour{i}")
    print("écriture du fichier CSV")
    with open('stats.csv','w',newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(['Nom du bot', '% victoire total', 'Temps de réflexion moyen', '% victoire matchups'])

        matchups_b1A = bot1AgroStats.get_matchups()
        texte_matchups_b1A = " | ".join([
                                        f"{adversaire}: {stats['victoires']}V-{stats['defaites']}D-N{stats['nuls']}" 
                                        for adversaire, stats in matchups_b1A.items()
                                        ])
        
        writer.writerow([bot1AgroStats.get_nom(), 
                            f"{bot1AgroStats.get_winrate()} %", 
                            f"{bot1AgroStats.get_average_time():.3f} sec",
                            texte_matchups_b1A])
        
        matchups_b2A = bot2AgroStats.get_matchups()
        texte_matchups_b2A = " | ".join([
                                        f"{adversaire}: {stats['victoires']}V-{stats['defaites']}D-N{stats['nuls']}" 
                                        for adversaire, stats in matchups_b2A.items()
                                        ])
        writer.writerow([bot2AgroStats.get_nom(),
                            f"{bot2AgroStats.get_winrate()} %",
                            f"{bot2AgroStats.get_average_time():.3f} sec",
                            texte_matchups_b2A])
        
        matchups_b3A = bot3AgroStats.get_matchups()
        texte_matchups_b3A = " | ".join([
                                        f"{adversaire}: {stats['victoires']}V-{stats['defaites']}D-N{stats['nuls']}" 
                                        for adversaire, stats in matchups_b3A.items()
                                        ])
        writer.writerow([bot3AgroStats.get_nom(), 
                            f"{bot3AgroStats.get_winrate()} %",
                            f"{bot3AgroStats.get_average_time():.3f} sec",
                            texte_matchups_b3A])
        
        matchups_b1D = bot1DefStats.get_matchups()
        texte_matchups_b1D = " | ".join([
                                        f"{adversaire}: {stats['victoires']}V-{stats['defaites']}D-N{stats['nuls']}" 
                                        for adversaire, stats in matchups_b1D.items()
                                        ])
        writer.writerow([bot1DefStats.get_nom(),
                        f"{bot1DefStats.get_winrate()} %",
                        f"{bot1DefStats.get_average_time():.3f} sec",
                        texte_matchups_b1D])
        
        matchups_b2D = bot2DefStats.get_matchups()
        texte_matchups_b2D = " | ".join([
                                        f"{adversaire}: {stats['victoires']}V-{stats['defaites']}D-N{stats['nuls']}" 
                                        for adversaire, stats in matchups_b2D.items()
                                        ])
        writer.writerow([bot2DefStats.get_nom(),
                        f"{bot2DefStats.get_winrate()} %",
                        f"{bot2DefStats.get_average_time():.3f} sec",
                        texte_matchups_b2D])

        matchups_b3D = bot3DefStats.get_matchups()
        texte_matchups_b3D = " | ".join([
                                        f"{adversaire}: {stats['victoires']}V-{stats['defaites']}D-N{stats['nuls']}" 
                                        for adversaire, stats in matchups_b3D.items()
                                        ])
        writer.writerow([bot3DefStats.get_nom(),
                        f"{bot3DefStats.get_winrate()} %",
                        f"{bot3DefStats.get_average_time():.3f} sec",
                        texte_matchups_b3D])