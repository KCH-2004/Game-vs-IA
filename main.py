from game import Gomoku
import ia
import data

if __name__ =="__main__":
    jeu = Gomoku()

    while True:

        try:
            rep = input("jouer contre un humain ou une ia ? (répondre humain, ia)")

            match rep.lower():

                case "ia":
                    jeu.nouvellepartievsIA()
                    break

                case "humain":
                    jeu.nouvellepartieMultilpayer()
                    break

                case "Generatedata":
                    data.analyseData()
                    break

                case _:

                    raise ValueError("Choisissez un mode existant (humain, ia)")
                
        except ValueError as error:
            print(f"Erreur: {error}")