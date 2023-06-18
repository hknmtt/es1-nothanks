from carta import Carta

class Jogador:
    def __init__(self):
        self.nome = None
        self.id = None
        self.cartas = []
        self.numero_fichas = None
        self.pontuacao = 0

    def set_nome(self, nome):
        self.nome = nome

    def get_nome(self):
        return self.nome
    
    def set_id(self, id):
        self.id = id
    
    def set_fichas(self, numero_fichas):
        self.numero_fichas = numero_fichas
    
    def adiciona_carta(self, carta):
        self.cartas.append(carta)
    
    def adiciona_fichas(self, numero_fichas):
        self.numero_fichas += numero_fichas

    def possui_fichas(self):
        return self.numero_fichas > 0
    
    def reordenar_cartas(self):
        # bubble sort
        qtd_cartas = len(self.cartas)
        for i in range(qtd_cartas):
            for j in range(i+1, qtd_cartas):
                if self.cartas[i].valor > self.cartas[j].valor:
                    self.cartas[i], self.cartas[j] = self.cartas[j], self.cartas[i]

    def instanciar_teste(self, id):
        self.id = id
        self.nome = "Jogador " + str(id)
        self.numero_fichas = id*2 + 1
        self.cartas = [Carta(id+1), Carta(id+2), Carta(id+3)]
        
