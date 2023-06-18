from baralho import Baralho
from jogador import Jogador
from carta import Carta

class Mesa():
    def __init__(self):
        self.baralho = Baralho()
        self.jogadores = []
        for i in range(4):
            jogador = Jogador()
            self.jogadores.append(jogador)

        self.carta_virada = Carta(0)
        self.fichas_acumuladas = 0
        self.jogo_andamento = False
        self.vencedor = None
        self.jogador_em_turno = None
        self.ordem_jogadores = []
        self.jogador_local = None


    def set_baralho(self, baralho):
        self.baralho = baralho

    def retirar_cartas_iniciais(self):
        for i in range(4):
            self.baralho.retirar_carta()

    def virar_nova_carta(self):
        carta_virada = self.baralho.retirar_carta()
        if carta_virada.valor == 0:
            self.terminar_jogo()
            return 'finished'
        else:
            self.carta_virada = carta_virada
            self.fichas_acumuladas = 0
            return 'next'
        
    def terminar_jogo(self):
        self.jogo_andamento = False
    
    def inicia_jogo(self):
        self.jogo_andamento = True

    def set_jogadores(self, jogadores):
        # ['nome', 'id', 'ordem']
        for i, jogador in enumerate(jogadores):
            self.jogadores[i].set_nome(jogador[0])
            self.jogadores[i].set_id(jogador[1])
            self.jogadores[i].set_fichas(11)

    def set_ordem(self, ordem):
        print(ordem)
        self.ordem_jogadores = ordem

    def set_jogador_local(self, jogador_local):
        self.jogador_local = jogador_local

    def set_jogador_em_turno(self, jogador_em_turno):
        self.jogador_em_turno = jogador_em_turno
    
    def verifica_se_turno_local(self):
        return self.jogador_local == self.jogador_em_turno
    
    def get_jogador_por_id(self, id):
        for jogador in self.jogadores:
            if jogador.id == id:
                return jogador
        raise Exception("Jogador não encontrado")

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
    

