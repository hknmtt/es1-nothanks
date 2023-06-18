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
    
    def set_id(self, id):
        self.id = id
    
    def set_fichas(self, numero_fichas):
        self.numero_fichas = numero_fichas

    def instanciar_teste(self, id):
        self.id = id
        self.nome = "Jogador " + str(id)
        self.numero_fichas = id*2 + 1
        self.cartas = [Carta(id+1), Carta(id+2), Carta(id+3)]
        
