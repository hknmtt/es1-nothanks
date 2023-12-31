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

    def set_baralho_codificado(self, baralho_codificado):
        self.baralho.decodifica(baralho_codificado)

    def set_carta_virada(self, carta_virada):
        self.carta_virada = carta_virada

    def set_jogadores(self, jogadores):
        # ['nome', 'id', 'ordem']
        for i, jogador in enumerate(jogadores):
            self.jogadores[i].set_nome(jogador[0])
            self.jogadores[i].set_id(jogador[1])
            self.jogadores[i].set_fichas(11)

    def set_ordem(self, ordem):
        self.ordem_jogadores = ordem

    def set_jogador_local(self, jogador_local):
        self.jogador_local = jogador_local

    def set_jogador_em_turno(self, jogador_em_turno):
        self.jogador_em_turno = jogador_em_turno

    def get_jogador_por_id(self, id):
        for jogador in self.jogadores:
            if jogador.id == id:
                return jogador
        raise Exception("Jogador não encontrado")
    
    def add_ficha(self):
        self.fichas_acumuladas += 1
    
    def set_fichas(self, fichas):
        self.fichas_acumuladas = fichas

    def get_fichas_acumuladas(self):
        return self.fichas_acumuladas
    
    def get_carta_virada(self):
        return self.carta_virada
    
    def get_nome_vencedor(self):
        return self.vencedor.get_nome()

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
    
    def iniciar_jogo(self):
        self.jogo_andamento = True

    
    
    def verifica_se_turno_local(self):
        return self.jogador_local == self.jogador_em_turno
    
    

    def compor_dict_enviar_jogada(self, aceitou, carta):
        match_status = 'next'
        if self.jogo_andamento == False:
            match_status = 'finished'
            jogada = {
                'player' : self.jogador_em_turno,
                'aceitou' : aceitou,
                'carta_comprada' : carta,
                'match_status' : match_status,
                'baralho' : self.baralho.codifica(),
                'carta_virada' : self.carta_virada.valor,
                'fichas' : self.fichas_acumuladas,
                'vencedor' : self.vencedor.get_nome(),
            }
        else:
            jogada = {
                'player' : self.jogador_em_turno,
                'aceitou' : aceitou,
                'carta_comprada' : carta,
                'match_status' : match_status,
                'baralho' : self.baralho.codifica(),
                'carta_virada' : self.carta_virada.valor,
                'fichas' : self.fichas_acumuladas,
            }
        
        return jogada
    
    
    def jogador_possui_fichas(self, id):
        return self.get_jogador_por_id(id).possui_fichas()
    
    def jogador_local_possui_fichas(self):
        return self.jogador_possui_fichas(self.jogador_local)
    
    def jogador_remove_ficha(self, id):
        self.get_jogador_por_id(id).remove_ficha()

    def jogador_local_remove_ficha(self):
        self.jogador_remove_ficha(self.jogador_local)

    def jogador_compra_carta(self, id, carta, fichas):
        self.get_jogador_por_id(id).adiciona_carta(carta)
        self.get_jogador_por_id(id).adiciona_fichas(fichas)
        self.get_jogador_por_id(id).reordenar_cartas()

    def jogador_local_compra_carta(self, carta, fichas):
        self.jogador_compra_carta(self.jogador_local, carta, fichas)
    
    

    def proximo_jogador(self):
        for i in range(4):
            if self.ordem_jogadores[i] == self.jogador_em_turno:
                self.jogador_em_turno = self.ordem_jogadores[(i+1)%4]
                break 
    
    def atribuir_vencedor(self):
        self.vencedor = self.jogadores[0]
        for jogador in self.jogadores:
            lista_sequencias = []
            sequencia = []
            carta_anterior = -1

            for carta in jogador.get_cartas():
                if carta.valor == carta_anterior + 1:
                    sequencia.append(carta.valor)
                else:
                    lista_sequencias.append(sequencia)
                    sequencia = [carta.valor]
                carta_anterior = carta.valor

            lista_sequencias.append(sequencia)

            for sequencia in lista_sequencias:
                if sequencia:
                    jogador.add_pontuacao(min(sequencia))

            jogador.set_pontuacao(jogador.get_pontuacao() - jogador.get_fichas())

            if jogador.get_pontuacao() < self.vencedor.get_pontuacao():
                self.vencedor = jogador
            

