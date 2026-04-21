from game import Puissance5
import data
if __name__ =="__main__":
    jeu = Puissance5()
    while True:
        try:
            rep = input("jouer contre un humain, une ia, ou générer des données ia vs ia ? (répondre humain, ia ou data)")
            match rep.lower():
                case "ia":
                    jeu.nouvellepartievsIA()
                    break
                case "humain":
                    jeu.nouvellepartieMultilpayer()
                    break
                case "data":
                    data.IAMatch()
                    break
                case _:
                    raise ValueError("Choisissze un mode existant (humain, ia, data)")
        except ValueError as error:
            print(f"Erreur: {error}")