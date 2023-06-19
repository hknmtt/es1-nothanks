from tkinter import *
from tkinter import simpledialog
from tkinter import messagebox
from baralho import Baralho
from dog.dog_interface import DogPlayerInterface
from dog.dog_actor import DogActor
from dog.start_status import StartStatus
from mesa import Mesa
from carta import Carta

class InterfaceJogador(DogPlayerInterface):
    def __init__(self):
        self.root = Tk()
        self.root.title("No Thanks!")
        self.root.geometry("1280x720")
        self.root.resizable(False, False)

        self.iniciar_programa()        
        
        self.root.mainloop()

    def iniciar_programa(self):
        self.fill_main_window()

        self.mesa = Mesa()
        player_name = self.request_player_name()
        self.dog_server_interface = DogActor()
        message = self.dog_server_interface.initialize(player_name, self)
        self.notify_result(message)


    def fill_main_window(self):
        self.top_frame = Frame(self.root, bg="white", width=1280, height=200)
        self.top_frame.pack(side="top")

        self.menubar = Menu(self.root)
        self.menubar.option_add("*tearOff", FALSE)
        self.root["menu"] = self.menubar

        self.filemenu = Menu(self.menubar)
        self.menubar.add_cascade(label="Menu", menu=self.filemenu)
        self.filemenu.add_command(label="Iniciar Partida", command=self.iniciar_partida)

        self.players_rows = []
        self.ui_player_name_labels = []
        self.ui_player_cards_labels = [[],[],[],[]]
        

        for i in range(4):
            self.players_rows.append(Frame(self.root, bg="blue", width=1280, height=130))
            self.players_rows[i].pack(side="top")

            player_name_frame = Frame(self.players_rows[i], bg="green", width=80, height=130)
            player_name_frame.grid(row=0, column=0)
            self.ui_player_name_labels.append(StringVar())
            self.ui_player_name_labels[i].set("Player " + str(i + 1))
            player_name_label = Label(player_name_frame, textvariable=self.ui_player_name_labels[i], bg="green", font=("Arial", 12)).place(relx=0.5, rely=0.5, anchor="center")


            for j in range(1, 16):
                card = Frame(self.players_rows[i], bg="white", width=60, height=90)
                self.players_rows[i].grid_columnconfigure(j, minsize=80)
                self.players_rows[i].grid_rowconfigure(0, minsize=130)
                card.grid(row=0, column=j, padx=2, pady=2)

                self.ui_player_cards_labels[i].append(StringVar())
                self.ui_player_cards_labels[i][j - 1].set('')
                card_label = Label(card, textvariable=self.ui_player_cards_labels[i][j-1], bg="white", font=("Arial", 30))

                card_label.place(relx=0.5, rely=0.5, anchor="center")



        # Text of whos turn is it on top_frame left side anchor left
        self.ui_turn_label = StringVar()
        self.ui_turn_label.set("Turno de: ")
        self.turn_label = Label(self.top_frame, textvariable=self.ui_turn_label, bg="white", font=("Arial", 20)).place(relx=0.15, rely=0.5, anchor="center")

        self.ui_remaining_cards_deck_label = StringVar()
        self.ui_remaining_cards_deck_label.set("")

        self.remaining_cards_deck = Frame(self.top_frame, bg="green", width=80, height=120)
        self.remaining_cards_deck.place(relx=0.4, rely=0.5, anchor="center")
        self.remaining_cards_deck_label = Label(self.remaining_cards_deck, textvariable=self.ui_remaining_cards_deck_label , bg="green", font=("Arial", 30)).place(relx=0.5, rely=0.5, anchor="center")

        # Grey current card with red circle indicating number of chips on it
        self.current_card = Frame(self.top_frame, bg="grey", width=80, height=120)
        self.current_card.place(relx=0.5, rely=0.5, anchor="center")
        self.ui_current_card_label = StringVar()
        self.ui_current_card_label.set("")
        self.current_card_label = Label(self.current_card, textvariable=self.ui_current_card_label, bg="grey", font=("Arial", 30)).place(relx=0.5, rely=0.5, anchor="center")
        self.current_card_chips = Frame(self.current_card, bg="red", width=30, height=30)
        self.current_card_chips.place(relx=0.5, rely=0.8, anchor="center")
        self.ui_current_card_chips_label = StringVar()
        self.ui_current_card_chips_label.set("")
        self.current_card_chips_label = Label(self.current_card_chips, textvariable=self.ui_current_card_chips_label, bg="red", font=("Arial", 12)).place(relx=0.5, rely=0.5, anchor="center")

        # top_frame right side
        # text of how many chips player has above two buttons, one to take card and other to pay chip
        self.player_chips = Frame(self.top_frame, bg="grey", width=400, height=120)
        self.player_chips.place(relx=0.8, rely=0.5, anchor="center")
        self.ui_player_chips_label = StringVar()
        self.ui_player_chips_label.set("")
        self.player_chips_label = Label(self.player_chips, textvariable=self.ui_player_chips_label, bg="white", font=("Arial", 20)).place(relx=0.5, rely=0.3, anchor="center")

        # button to take card
        self.take_card_button = Button(self.player_chips, text="Aceitar carta", bg="white", font=("Arial", 14), command=lambda: self.aceitar_carta())
        self.take_card_button.place(relx=0.2, rely=0.7, anchor="center")

        # button to pay chip
        self.pay_chip_button = Button(self.player_chips, text="Não, obrigado", bg="white", font=("Arial", 14), command=lambda: self.recusar_carta())
        self.pay_chip_button.place(relx=0.8, rely=0.7, anchor="center")

    
    def receive_start(self, start_status: StartStatus):
        message = start_status.get_message()
        jogadores = start_status.get_players()
        id_local = start_status.get_local_id()
        self.mesa.set_jogadores(jogadores)
        
        ordem = ['0', '0', '0', '0']
        for jogador in jogadores:
            ordem[int(jogador[2])-1] = jogador[1]

        self.mesa.set_ordem(ordem)

        self.mesa.set_jogador_local(id_local)

        self.mesa.set_jogador_em_turno(ordem[0])

        self.update_ui()
        self.mesa.iniciar_jogo()
        self.notify_result(message)

    def receive_move(self, a_move: dict):
        if a_move["aceitou"] == True:
            self.mesa.jogador_compra_carta(a_move["player"], Carta(int(a_move["carta_comprada"])), int(a_move["fichas"]))

        self.mesa.set_carta_virada(Carta(int(a_move["carta_virada"])))
        self.mesa.set_baralho_codificado(a_move["baralho"])
        self.mesa.set_fichas(a_move["fichas"])
        self.mesa.set_jogador_em_turno(self.mesa.ordem_jogadores[(a_move["order"] - 1) % 4])

        self.update_ui()

        if a_move["match_status"] == 'finished':

            self.mesa.terminar_jogo()
            self.notify_result(f"O jogador {a_move['vencedor']} venceu a partida!")
            self.fechar_programa()

    def receive_withdrawal_notification(self):
        self.notify_result("Um jogador abandonou a partida")
        self.fechar_programa()
    
    def request_player_name(self) -> str:
        return simpledialog.askstring(title="Player identification", prompt="Qual o seu nome?")

    def notify_result(self, message: str):
        messagebox.showinfo(message=message)

    def fechar_programa(self):
        self.root.destroy()

    def update_ui(self):
        # update fichas jogador local
        self.ui_player_chips_label.set("Fichas: " + str(self.mesa.get_jogador_por_id(self.mesa.jogador_local).numero_fichas))

        # update numero de cartas no baralho
        self.ui_remaining_cards_deck_label.set(str(len(self.mesa.baralho)))

        # update fichas na carta virada
        self.ui_current_card_chips_label.set(str(self.mesa.fichas_acumuladas))

        # update carta virada
        self.ui_current_card_label.set(str(self.mesa.carta_virada.valor))

        # update jogador em turno
        nome_jogador_em_turno = self.mesa.get_jogador_por_id(self.mesa.jogador_em_turno).nome
        self.ui_turn_label.set(f"Turno de : {nome_jogador_em_turno:<25}")

        for i in range(4):
            self.ui_player_name_labels[i].set(str(self.mesa.jogadores[i].nome))
            for j in range(1, 16):
                if j <= len(self.mesa.jogadores[i].cartas):
                    self.ui_player_cards_labels[i][j-1].set(str(self.mesa.jogadores[i].cartas[j - 1].valor))
                else:
                    self.ui_player_cards_labels[i][j-1].set("")

    def iniciar_partida(self):
        start_status = self.dog_server_interface.start_match(4)
        code = start_status.get_code()
        message = start_status.get_message()

        if code == '0' or code == '1':
            self.notify_result(message)
        else:
            baralho = Baralho()
            self.mesa.iniciar_jogo()
            self.mesa.set_baralho(baralho)
            self.mesa.retirar_cartas_iniciais()
            self.mesa.virar_nova_carta()
            jogadores = start_status.get_players()
            id_local = start_status.get_local_id()
            self.mesa.set_jogadores(jogadores)
            
            ordem = ['0', '0', '0', '0']
            for jogador in jogadores:
                ordem[int(jogador[2])-1] = jogador[1]

            self.mesa.set_ordem(ordem)

            self.mesa.set_jogador_local(id_local)

            self.mesa.set_jogador_em_turno(ordem[0])

            self.dog_server_interface.send_move(move= self.mesa.compor_dict_enviar_jogada(aceitou=False, carta=0))

            self.update_ui()
            self.notify_result(message)



    def aceitar_carta(self):
        turno_jogador_local = self.mesa.verifica_se_turno_local()

        if turno_jogador_local:
            fichas_mesas = self.mesa.get_fichas_acumuladas()
            carta_comprada = self.mesa.get_carta_virada()

            self.mesa.jogador_local_compra_carta(carta_comprada, fichas_mesas)

            match_status = self.mesa.virar_nova_carta()

            if match_status == 'finished':
                self.mesa.atribuir_vencedor()

            move_to_send = self.mesa.compor_dict_enviar_jogada(aceitou=True, carta=carta_comprada.valor)

            self.dog_server_interface.send_move(move= move_to_send)
            self.mesa.proximo_jogador()

            self.update_ui()

            if match_status == 'finished':
                self.mesa.terminar_jogo()
                self.notify_result(f"O jogador {self.mesa.vencedor.nome} venceu a partida!")
                self.fechar_programa()

        else:
            self.notify_result("Não é seu turno")

    def recusar_carta(self):
        turno_jogador_local = self.mesa.verifica_se_turno_local()

        if turno_jogador_local:
            possui_fichas = self.mesa.jogador_local_possui_fichas()
            if possui_fichas:
                self.mesa.jogador_local_remove_ficha()
                self.mesa.add_ficha()

                move_to_send = self.mesa.compor_dict_enviar_jogada(aceitou=False, carta = 0)

                self.dog_server_interface.send_move(move=move_to_send)
                self.mesa.proximo_jogador()

                self.update_ui()

            else:
                self.notify_result("Não possui fichas")
        else:
            self.notify_result("Não é seu turno")
     
