from carta import Carta
from random import shuffle

class Baralho:
    def __init__(self):
        self.cartas = []

    def instanciar_teste(self):
        for i in range(1, 38):
            self.cartas.append(Carta(i))

        shuffle(self.cartas)
    
    def retirar_carta(self):
        return self.cartas.pop()
    
    def __len__(self):
        return len(self.cartas)
