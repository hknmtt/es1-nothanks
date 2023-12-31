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
    
    def get_fichas(self):
        return self.numero_fichas
    
    def set_pontuacao(self, pontuacao):
        self.pontuacao = pontuacao

    def get_pontuacao(self):
        return self.pontuacao
    
    def get_cartas(self):
        return self.cartas
        
    def add_pontuacao(self, pontos):
        self.pontuacao += pontos
    
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

    def remove_ficha(self):
        self.numero_fichas = self.numero_fichas - 1
        
