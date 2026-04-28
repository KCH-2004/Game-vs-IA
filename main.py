from game import Gomoku
import data

if __name__ =="__main__":
    jeu = Gomoku()

    while True:
        try:
            rep = input("jouer contre un humain ou une ia ? (répondre humain, ia)\n"
                        "data pour générer automatiquement les données du tournoi entre IA\n"
                        "(ATTENTION: TOUTES LES RESSOURCES DU PROCESSEUR SERONT UTILISÉES)")

            match rep.lower():
                case "ia":
                    jeu.nouvellepartievsIA()
                    break

                case "humain":
                    jeu.nouvellepartieMultilpayer()
                    break

                case "data":
                    data.analyseData()
                    break
                case _:
                    raise ValueError("Choisissez un mode existant (humain, ia)")
                
        except ValueError as error:
            print(f"Erreur: {error}")