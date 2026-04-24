import ia
import game
import csv
import itertools

class AIStats:

    def __init__(self, AIName):
        self.AIName = AIName
        self.wins = 0
        self.draws = 0
        self.loses = 0
        self.tps_total = 0
        self.coups_totaux = 0
        self.matchups = {}

    def get_winrate(self):
        """self -> float
        fonction qui retourne le pourcentage de victoire d'une IA
        """
        if  self.draws + self.loses + self.wins == 0:
            return 0
        return (self.wins / (self.draws + self.loses + self.wins)) * 100
    
    def get_average_time(self):
        """self -> float
        fonction qui retourne le temps que mets une IA à jouer un coup"""
        if self.coups_totaux == 0:
            return 0
        
        return self.tps_total/self.coups_totaux
    
    def get_nom(self):
        """self -> string
        fonction qui retourne le nom de l'IA
        """
        return self.AIName
    
    def add_matchup(self, datas, matchup,isStarting = True):
        """self x dict x string, boolean = True -> None
        ajoute l'issue d'un match contre une IA "matchup":
        - datas est un dictionnaire contenant les données issue de AIGame 
        (détail des données retournés dans la fonction AIgame)
        - matchup est une chaine de caractère contenant le nom de l'IA
        - isStarting est un booléen pour savoir si l'IA a commencé ou non
        """

        self.matchups.setdefault(matchup, {"isStarting": {"wins": 0, "loses": 0, "draws": 0},
                                           "isNotStarting": {"wins": 0, "loses": 0, "draws": 0}})
        #Si c'est la première partie contre l'IA "matchup", alors on crée la pair clé valeur matchup : dict
        #dict contient pour chaque matchup une clé isStarting : statistiques des parties (victoires défaites nuls)
        #Il contient une clé isnotStarting qui contient les mêmes statistiques que isStarting mais c'est pour le cas où
        #l'IA ne commence pas
        
        match datas["isWinner"]:
        #On analyse les différentes issues de chaque partie
            case True:
                #En cas de victoire
                if isStarting:
                    #Si l'IA a commencé, alors on incrémente son compteur isStarting
                    #contre "matchup" de avec la clé "win"
                    self.matchups[matchup]["isStarting"]["wins"] += 1

                else:
                    #Sinon, on incrémente son compteur isNotStarting 
                    #contre "matchup" avec la clé "win"
                    self.matchups[matchup]["isNotStarting"]["wins"] += 1

                #Dans les deux cas, on incrémente cette victoire à son compteur de victoire global
                self.wins += 1

            case False:
                #En cas de défaite: Même logique qu'avec le cas de victoire
                if isStarting:
                    self.matchups[matchup]["isStarting"]["loses"] += 1

                else:
                    self.matchups[matchup]["isNotStarting"]["loses"] += 1

                self.loses += 1

            case _:
                #Idem pour s'il y a match nul
                if isStarting:
                    self.matchups[matchup]["isStarting"]["draws"] += 1

                else:
                    self.matchups[matchup]["isNotStarting"]["draws"] += 1

                self.draws += 1
        
        #On incrémente le temps de réflexion et le nombre de coups totaux de cette partie 
        self.tps_total += datas["tpsReflexion"]
        self.coups_totaux += datas["nbCoups"]
    
    def get_matchup(self):
        """self -> dict
        On retourne le dictionnaire de matchup présent dans self.matchups
        """
        return self.matchups


def saveCSVFile(AIList,nameFile = "stats.csv"):
    """list, string -> none
    Fonction qui écrit les données contenus dans AIList dans un fichier csv "nameFile"
    nom par défaut: stats.csv
    AIList est une liste de dictionnaire ayant comme clé 
    - le nom de l'IA
    - l'IA qui commence (objet AI)
    - l'IA qui ne commence pas (objet AI)
    - les statistiques de l'IA (objet AIStats)
    """

    with open(nameFile,'w',newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        #On initialise le fichier CSV
        writer.writerow(['Nom du bot', '% win total', 'Temps de réflexion moyen', 'Détail matchup (Start | Rep)'])
        #On y place les différentes informations sur la première ligne

        for AI in AIList:
        #On explore la liste d'IA
            stats = AI["stats"]
            #On stock les différentes statistiques présente dans l'objet AIStats stocké dans AIList pour une IA donnée
            matchups = stats.get_matchup
            #On y stock les différents "matchups" de AIStats pour une IA donnée

            matchupsToText = " || ".join([
                f"{adversaire} -> Start: {data_adv['isStarting']['wins']}V-{data_adv['isStarting']['loses']}D | Rep: {data_adv['isNotStarting']['wins']}V-{data_adv['isNotStarting']['loses']}D" 
                for adversaire, data_adv in matchups.items()
            ])
            #On transforme le dictionnaire en string séparé de ||

            writer.writerow(stats.get_nom(),f"{stats.get_winrate():.1f} %",f"{stats.get_average_time():.3f} s",matchupsToText)
            #On y écrit toutes les informations présentes dans stats

def AIGame(bot1,bot2):
    """AI x AI -> dict x dict
    Fonction qui simule une partie de Gomoku entre 2 IA
    retourne deux dictionnaires "Data" contenant chacun les clé suivantes associé à leur valeur
    - "isWinner": un booléen permettant de savoir si l'IA a gagné ou non
    - "tpsReflexion": un entier permettant de connaitre le temps de réflexion total dans cette en secondes
    - "nbCoups": un entier permettant d'obtenir le nombre de coups total dans cette partie """

    gameStart = game.Gomoku()
    count = 0
    win = False
    winner = None
    bot1Data = {"isWinner":False,"tpsReflexion": 0, "nbCoups": 0} 
    bot2Data = {"isWinner":False,"tpsReflexion": 0, "nbCoups": 0}
    isBot1Starting = bot1.jetonAI == 'O'
    #On initialise les données de base

    while not win and count < 100:
    #Ici, on reprend la logique du game.py, réarrangé pour que 2 IA puissent s'affronter
        count += 1
        if isBot1Starting:
            isBot1turn = count % 2 == 1

        else:
            isBot1turn = count % 2 == 0

        if isBot1turn:
            result = bot1.get_best_move(gameStart)
            bot1Data['tpsReflexion'] += bot1.getTempsReflexion()
            gameStart.board[result[1][0]][result[1][1]] = bot1.jetonAI

            if count > 6: 
                win = gameStart.check_win(result[1][0], result[1][1], bot1.jetonAI)

                if win:
                    winner = bot1.jetonAI

        else:
            #À la place de demander au joueur de jouer, on fait jouer la deuxième IA 
            #En reprennant la logique dans le bloc if précédent
            result = bot2.get_best_move(gameStart)
            bot2Data['tpsReflexion'] += bot2.getTempsReflexion()
            gameStart.board[result[1][0]][result[1][1]] = bot2.jetonAI

            if count > 6:  
                win = gameStart.check_win(result[1][0], result[1][1], bot2.jetonAI)

                if win:
                    winner = bot2.jetonAI
    """if winner == bot1.jetonAI: #Vérification du résultat (Si le random fonctionne,
                                        alors la partie est différente de la précédente)
        gameStart.show_board()
        print("Bot 1 Winner")
    else:
        gameStart.show_board()
        print("Bot 2 Winner")"""

    if winner == bot1.jetonAI:

        if isBot1Starting: #Si le bot1 a commencé et a gagné (son nombre de coups est donc impair)
            bot1Data['nbCoups'] /= ((count//2) + 1)
            bot2Data['nbCoups'] /= count//2

        else: #Dans le cas contraire, le coup winner est sur un count pair
            bot1Data['nbCoups'] /= count//2
            bot2Data['nbCoups'] /= count//2

        bot1Data['isWinner'] = True
        bot2Data['isWinner'] = False
    
    elif winner == bot2.jetonAI:

        if not isBot1Starting: #Même logique ici
            bot2Data['nbCoups'] /= ((count//2) + 1)
            bot1Data['nbCoups'] /= count//2

        else: #Dans le cas contraire, le coup winner est sur un count pair
            bot2Data['nbCoups'] /= count//2
            bot1Data['nbCoups'] /= count//2

        bot2Data['isWinner'] = True
        bot1Data['isWinner'] = False

    else: #Dans le cas où il y a match nul, le gomoku ici est un plateau de 10x10, il y a donc 100 coups au total
          #Les 2 IA ont donc joué un nombre identique de coups
        bot1Data['nbCoups'] /= count//2
        bot2Data['nbCoups'] /= count//2
        bot1Data['isWinner'] = None
        bot2Data['isWinner'] = None

    return bot1Data,bot2Data

def analyseData():
    """none -> none
    Fonction qui analyse les parties des IA:
    - avec un minimax de profondeur différentes (1,2,3)
    - Avec une heuristique variable (Agressif, Defensif)
    - Si elle commence ou non (reconnu avec le jeton qu'elle possède)

    Cela nous donne 6 IA qui doivent s'affronter entre elles 50 fois,
    Le total est donc de 6*50 + 15*50 = 1050 parties
    (Pour les différentes IA de même profondeur et de même style de jeu on obtient 6*50)
    (Pour les match "croisés" (différentes heuristiques, différents style de jeu...) on obtient 50*15)
    """
    winrateStarting, winrateNotStarting, draw, games= 0, 0, 0, 0

    #Nommage des différents IA: bot + profondeur du minimax + Style de jeu
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
    bot1AgroStats = AIStats("bot1AgroStats")
    bot2AgroStats = AIStats("bot2AgroStats")
    bot3AgroStats = AIStats("bot3AgroStats")
    bot1DefStats = AIStats("bot1DefStats")
    bot2DefStats = AIStats("bot2DefStats")
    bot3DefStats = AIStats("bot3DefStats")

    #On regroupe les données dans IAList afin d'y accéder facilement
    IAList = [
        {"nom": "bot1Agro", "start": bot1AgroStart, "not_start": bot1AgroNotStart, "stats": bot1AgroStats},
        {"nom": "bot2Agro", "start": bot2AgroStart, "not_start": bot2AgroNotStart, "stats": bot2AgroStats},
        {"nom": "bot3Agro", "start": bot3AgroStart, "not_start": bot3AgroNotStart, "stats": bot3AgroStats},
        {"nom": "bot1Def", "start": bot1DefStart, "not_start": bot1DefNotStart, "stats": bot1DefStats},
        {"nom": "bot2Def", "start": bot2DefStart, "not_start": bot2DefNotStart, "stats": bot2DefStats},
        {"nom": "bot3Def", "start": bot3DefStart, "not_start": bot3DefNotStart, "stats": bot3DefStats}
    ]

    for i in range(50):
        #On itère 50 fois car ce sont des match identique
        for bot in IAList:
            data_start, data_not_start = AIGame(bot["start"], bot["not_start"])
            bot["stats"].add_matchup(data_start, bot["nom"])
            bot["stats"].add_matchup(data_not_start, bot["nom"], isStarting = False)
            #On appelle la fonction de jeu entre l'IA qui commence et l'IA qui ne commence pas
            #Puis on stock les données dans stats

            if data_start["isWinner"]:
                winrateStarting += 1

            elif data_not_start["isWinner"]:
                winrateNotStarting += 1

            else:
                draw += 1

            games += 1
            #On stocke le winrate global de chaque match (selon s'il commence ou non)

    for i in range(25):
        #Ici, on itère 25 fois car il y a les matchs aller et les matchs retours
        for botA, botB in itertools.combinations(IAList, 2):
            #Pour avoir toutes les combinaisons de paires unique possible, on utilise itertools
            dataA_1, dataB_1 = AIGame(botA["start"], botB["not_start"])
            botA["stats"].add_matchup(dataA_1, botB["nom"])
            botB["stats"].add_matchup(dataB_1, botA["nom"], isStarting = False)

            if dataA_1["isWinner"]:
                winrateStarting += 1

            elif dataB_1["isWinner"]:
                winrateNotStarting += 1

            else:
                draw += 1

            games += 1
            #On stocke le winrate global de chaque match (selon s'il commence ou non)

            #On itère ici sur les matchs retours
            dataB_2, dataA_2 = AIGame(botB["start"], botA["not_start"])
            botB["stats"].add_matchup(dataB_2, botA["nom"])
            botA["stats"].add_matchup(dataA_2, botB["nom"])

            if dataB_2["isWinner"]:
                winrateStarting += 1

            elif dataA_2["isWinner"]:
                winrateNotStarting += 1

            else:
                draw += 1

            games += 1
            #On stocke le winrate global de chaque match (selon s'il commence ou non)

    saveCSVFile(IAList)