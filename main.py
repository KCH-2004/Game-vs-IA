from game import Puissance5
if __name__ =="__main__":

    jeu = Puissance5()
    while True:
        try:
            rep = input("jouer contre un humain ou une ia ?")
            match rep:
                case "ia":
                    jeu.nouvellepartievsIA()
                    break
                case "humain":
                    jeu.nouvellepartieMultilpayer()
                    break
                case _:
                    raise ValueError("Choisissze un mode existant (humain, ia, data)")
        except ValueError as error:
            print(f"Erreur: {error}")