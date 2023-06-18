from baralho import Baralho
from jogador import Jogador
from carta import Carta

class Mesa():
    def __init__(self):
        self.baralho = Baralho()
        self.jogadores = []
        self.carta_virada = None
        self.fichas_acumuladas = 0
        self.jogo_andamento = False
        self.vencedor = None
        self.jogador_em_turno = None
        self.ordem_jogadores = []
        self.jogador_local = None

    def instanciar_teste(self):
        self.baralho.instanciar_teste()
        for i in range(4):
            jogador = Jogador()
            jogador.instanciar_teste(i)
            self.jogadores.append(jogador)
        self.carta_virada = self.baralho.retirar_carta()
        self.fichas_acumuladas = 0
        self.jogador_local = str(self.jogadores[0].id)
        self.jogo_andamento = True
        self.jogador_em_turno = str(self.jogadores[0].id)
        self.ordem_jogadores = self.jogadores
    

