from carta import Carta
from random import shuffle

class Baralho:
    def __init__(self):
        self.cartas = []
        for i in range(1, 15):
            self.cartas.append(Carta(i))
        shuffle(self.cartas)
    
    def retirar_carta(self):
        if len(self.cartas) == 0:
            return Carta(0)
        else:
            return self.cartas.pop()
        
    def codifica(self):
        baralho = []
        for carta in self.cartas:
            baralho.append(str(carta.valor))
        return ",".join(baralho)

    def decodifica(self, baralho_codificado):
        if baralho_codificado == '':
            self.cartas = []
        else:
            cartas = baralho_codificado.split(",")
            baralho = []
            for carta in cartas:
                baralho.append(Carta(int(carta)))
            self.cartas = baralho        
    
    def __len__(self):
        return len(self.cartas)
