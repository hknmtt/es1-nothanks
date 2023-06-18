from carta import Carta
from random import shuffle

class Baralho:
    def __init__(self):
        self.cartas = []
        for i in range(1, 34):
            self.cartas.append(Carta(i))
        shuffle(self.cartas)

    def instanciar_teste(self):
        for i in range(1, 38):
            self.cartas.append(Carta(i))

        shuffle(self.cartas)
    
    def retirar_carta(self):
        if len(self.cartas) == 0:
            return Carta(0)
        else:
            return self.cartas.pop()
    
    def __len__(self):
        return len(self.cartas)
