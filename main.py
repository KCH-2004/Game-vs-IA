from game import Puissance5
if __name__ =="__main__":

    jeu = Puissance5()
    rep = input("jouer contre un humain ou une ia (possibilité de regarder deux IA s'affronter) ?")
    match rep:
        case "ia":
            jeu.nouvellepartievsIA()
        case "humain":
            jeu.nouvellepartieMultilpayer()
    