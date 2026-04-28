import ia
import game
import csv
import itertools
import concurrent.futures

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


def saveCSVFile(AIList, winrateStarting, winrateNotStarting, draw, games, nameFile="stats.csv"):
    """list, int, int, int, int, string -> none
    Fonction qui écrit les données contenues dans AIList dans un fichier csv.
    """

    with open(nameFile, 'w', newline='') as csvfile:
        # On utilise le point-virgule pour une lecture parfaite sur Excel
        writer = csv.writer(csvfile, delimiter='|')

        # En-têtes des IA
        writer.writerow(
            ['Nom du bot', '% win total', 'Temps de reflexion moyen', 'Detail matchup (joue en 1er | joue en 2e)'])

        # Données des IA
        for AI in AIList:
            stats = AI["stats"]
            matchups = stats.get_matchup()

            matchupsToText = " || ".join([
                f"{adversaire} -> 1er: {data_adv['isStarting']['wins']}V-{data_adv['isStarting']['loses']}D-{data_adv['isStarting']['draws']}N | 2e: {data_adv['isNotStarting']['wins']}V-{data_adv['isNotStarting']['loses']}D-{data_adv['isNotStarting']['draws']}N"
                for adversaire, data_adv in matchups.items()
            ])

            writer.writerow([
                stats.get_nom(),
                f"{stats.get_winrate():.1f} %",
                f"{stats.get_average_time():.5f} s",
                matchupsToText
            ])

        # Saut de ligne pour faire propre (optionnel mais recommandé)
        writer.writerow([])

        # --- CORRECTION DE L'INDENTATION ET DES CALCULS DE % ---
        writer.writerow(['Stats globales du tournoi'])

        # On évite la division par zéro au cas où
        if games > 0:
            writer.writerow([
                f"% victoire en jouant en 1er: {(winrateStarting / games) * 100:.1f} %",
                f"% victoire en jouant en 2e: {(winrateNotStarting / games) * 100:.1f} %",
                f"% de matchs nuls: {(draw / games) * 100:.1f} %",
                f"Nombre total de parties: {games}"
            ])

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
            bot1Data['nbCoups'] = ((count//2) + 1)
            bot2Data['nbCoups'] = count//2

        else: #Dans le cas contraire, le coup winner est sur un count pair
            bot1Data['nbCoups'] = count//2
            bot2Data['nbCoups'] = count//2

        bot1Data['isWinner'] = True
        bot2Data['isWinner'] = False

    elif winner == bot2.jetonAI:

        if not isBot1Starting: #Même logique ici
            bot2Data['nbCoups'] = ((count//2) + 1)
            bot1Data['nbCoups'] = count//2

        else: #Dans le cas contraire, le coup winner est sur un count pair
            bot2Data['nbCoups'] = count//2
            bot1Data['nbCoups'] = count//2

        bot2Data['isWinner'] = True
        bot1Data['isWinner'] = False

    else: #Dans le cas où il y a match nul, le gomoku ici est un plateau de 10x10, il y a donc 100 coups au total
          #Les 2 IA ont donc joué un nombre identique de coups
        bot1Data['nbCoups'] = count//2
        bot2Data['nbCoups'] = count//2
        bot1Data['isWinner'] = None
        bot2Data['isWinner'] = None

    return bot1Data,bot2Data


def worker_match(args):
    """Cette fonction est envoyée aux différents cœurs du processeur."""
    bot_start, bot_not_start, nom_start, nom_not_start = args

    # Le clone joue le match
    data_start, data_not_start = AIGame(bot_start, bot_not_start)

    # Le clone renvoie les résultats au boss
    return nom_start, nom_not_start, data_start, data_not_start

def analyseData():
    """none -> none
    Fonction qui analyse les parties des IA:
    - avec un minimax de profondeur différentes (1,2,5)
    - Si elle commence ou non (reconnu avec le jeton qu'elle possède)

    Cela nous donne 3 IA qui doivent s'affronter entre elles 50 fois,
    Le total est donc de 3*50 + 3*25*2 = 300 parties
    (Pour les différentes IA de même profondeur et de même style de jeu on obtient 6*50)
    (Pour les match "croisés" (différentes heuristiques, différents style de jeu...) on obtient 50*15)
    """
    winrateStarting, winrateNotStarting, draw, games= 0, 0, 0, 0

    #Nommage des différents IA: bot + profondeur du minimax + Style de jeu
    
    bot1Start = ia.AI('O','X',1,"neutre")
    bot1NotStart = ia.AI('X','O',1,"neutre")
    bot1Stats = AIStats("bot1Stats")
    
    bot3Start = ia.AI('O','X',3,"neutre")
    bot3NotStart = ia.AI('X','O',3,"neutre")
    bot3Stats = AIStats("bot3Stats")
    
    bot5Start = ia.AI('O','X',5,"neutre")
    bot5NotStart = ia.AI('X','O',5,"neutre")
    bot5Stats = AIStats("bot5Stats")



    #On regroupe les données dans IAList afin d'y accéder facilement
    IAList = [
        {"nom": "bot1", "start": bot1Start, "not_start": bot1NotStart, "stats": bot1Stats},
        {"nom": "bot3", "start": bot3Start, "not_start": bot3NotStart, "stats": bot3Stats},
        {"nom": "bot5", "start": bot5Start, "not_start": bot5NotStart, "stats": bot5Stats}
    ]

    dict_stats = {bot["nom"]: bot["stats"] for bot in IAList}

    # 1. On crée la To-Do List de tous les matchs
    tous_les_matchs = []

    # On ajoute les 50 matchs miroirs
    for i in range(50):
        for bot in IAList:
            tous_les_matchs.append((bot["start"], bot["not_start"], bot["nom"], bot["nom"]))

    # On ajoute les 25 tournois (Aller - Retour)
    """for i in range(25):
        for botA, botB in itertools.combinations(IAList, 2):
            tous_les_matchs.append((botA["start"], botB["not_start"], botA["nom"], botB["nom"]))
            tous_les_matchs.append((botB["start"], botA["not_start"], botB["nom"], botA["nom"]))"""

    print(f" Lancement de {len(tous_les_matchs)} matchs sur tous les cœurs du processeur...")

    winrateStarting, winrateNotStarting, draw, games = 0, 0, 0, 0

    # 2. Le Multiprocessing (La magie opère ici)
    with concurrent.futures.ProcessPoolExecutor() as executor:
        # map exécute 'worker_match' sur chaque match de la To-Do List en parallèle
        # et nous renvoie les résultats au fur et à mesure qu'ils se terminent.
        for resultat in executor.map(worker_match, tous_les_matchs):
            nom_start, nom_not_start, data_start, data_not_start = resultat

            # 5. L'Agrégation (Le boss met à jour les stats)
            dict_stats[nom_start].add_matchup(data_start, nom_not_start)
            dict_stats[nom_not_start].add_matchup(data_not_start, nom_start, isStarting = False)

            if data_start["isWinner"]:
                winrateStarting += 1
            elif data_not_start["isWinner"]:
                winrateNotStarting += 1
            else:
                draw += 1
            games += 1

            if games % 10 == 0:  # Abaissé à 10 pour voir la progression plus vite
                print(f"Avancement : {games}/{len(tous_les_matchs)} matchs terminés...")

    print("écriture du csv")
    saveCSVFile(IAList,winrateStarting, winrateNotStarting, draw, games,"statsTemoin2.csv")