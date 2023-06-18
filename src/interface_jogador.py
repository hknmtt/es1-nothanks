from tkinter import *
from tkinter import simpledialog
from tkinter import messagebox
from baralho import Baralho
from dog.dog_interface import DogPlayerInterface
from dog.dog_actor import DogActor
from dog.start_status import StartStatus
from mesa import Mesa

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
        # remover depois
        #self.mesa.instanciar_teste()
        player_name = self.request_player_name()
        self.dog_server_interface = DogActor()
        message = self.dog_server_interface.initialize(player_name, self)
        self.notify_result(message)
        #self.update_ui()


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

        for i in range(4):
            self.players_rows.append(Frame(self.root, bg="blue", width=1280, height=130))
            self.players_rows[i].pack(side="top")

            player_name_frame = Frame(self.players_rows[i], bg="green", width=80, height=130)
            player_name_frame.grid(row=0, column=0)
            player_name_label = Label(player_name_frame, text="Player " + str(i + 1), bg="green", font=("Arial", 12)).place(relx=0.5, rely=0.5, anchor="center")


            for j in range(1, 16):
                card = Frame(self.players_rows[i], bg="white", width=60, height=90)
                self.players_rows[i].grid_columnconfigure(j, minsize=80)
                self.players_rows[i].grid_rowconfigure(0, minsize=130)
                card.grid(row=0, column=j, padx=2, pady=2)
                card_label = Label(card, text="", bg="white", font=("Arial", 30))
                
                # if j <= len(self.cards[i]):
                #     card_label.config(text=self.cards[i][j - 1], bg="grey")
                #     card.config(bg="grey")

                card_label.place(relx=0.5, rely=0.5, anchor="center")



            # Text of whos turn is it on top_frame left side anchor left
        self.turn_label = Label(self.top_frame, text="", bg="white", font=("Arial", 20)).place(relx=0.15, rely=0.5, anchor="center")

        self.remaining_cards_deck = Frame(self.top_frame, bg="green", width=80, height=120)
        self.remaining_cards_deck.place(relx=0.4, rely=0.5, anchor="center")
        self.remaining_cards_deck_label = Label(self.remaining_cards_deck, text="", bg="green", font=("Arial", 30)).place(relx=0.5, rely=0.5, anchor="center")

        # Grey current card with red circle indicating number of chips on it
        self.current_card = Frame(self.top_frame, bg="grey", width=80, height=120)
        self.current_card.place(relx=0.5, rely=0.5, anchor="center")
        self.current_card_label = Label(self.current_card, text="", bg="grey", font=("Arial", 30)).place(relx=0.5, rely=0.5, anchor="center")
        self.current_card_chips = Frame(self.current_card, bg="red", width=30, height=30)
        self.current_card_chips.place(relx=0.5, rely=0.8, anchor="center")
        self.current_card_chips_label = Label(self.current_card_chips, text="", bg="red", font=("Arial", 12)).place(relx=0.5, rely=0.5, anchor="center")

        # top_frame right side
        # text of how many chips player has above two buttons, one to take card and other to pay chip
        self.player_chips = Frame(self.top_frame, bg="grey", width=400, height=120)
        self.player_chips.place(relx=0.8, rely=0.5, anchor="center")
        self.player_chips_label = Label(self.player_chips, text="", bg="white", font=("Arial", 20)).place(relx=0.5, rely=0.3, anchor="center")

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
        self.mesa.inicia_jogo()
        self.notify_result(message)

    def receive_move(self, a_move: dict):
        print("Recebeu movimento")
        print(a_move)

    def receive_withdrawal_notification(self):
        self.notify_result("Um jogador abandonou a partida")
        self.fechar_programa()
    
    def request_player_name(self) -> str:
        return simpledialog.askstring(title="Player identification", prompt="Qual o seu nome?")

    def notify_result(self, message: str):
        messagebox.showinfo(message=message)

    def fechar_programa(self):
        exit()

    def update_ui(self):
        # update fichas jogador local
        Label(self.player_chips, text= "Fichas: " + str(self.mesa.get_jogador_por_id(self.mesa.jogador_local).numero_fichas)
              , bg="white", font=("Arial", 20)).place(relx=0.5, rely=0.3, anchor="center")

        # update numero de cartas no baralho
        Label(self.remaining_cards_deck, text=str(len(self.mesa.baralho)), bg="green", font=("Arial", 30)).place(relx=0.5, rely=0.5, anchor="center")

        # update fichas na carta virada
        Label(self.current_card_chips, text=str(self.mesa.fichas_acumuladas), bg="red", font=("Arial", 12)).place(relx=0.5, rely=0.5, anchor="center")
        
        # update carta virada
        Label(self.current_card, text=str(self.mesa.carta_virada.valor), bg="grey", font=("Arial", 30)).place(relx=0.5, rely=0.5, anchor="center")

        # update jogador em turno
        nome_jogador_em_turno = self.mesa.get_jogador_por_id(self.mesa.jogador_em_turno).nome
        Label(self.top_frame, text=f"Turno de : {nome_jogador_em_turno:<25}", bg="white", font=("Arial", 20)).place(relx=0.15, rely=0.5, anchor="center")

        # update cartas dos jogadores
        for i in range(4):
            player_name_frame = Frame(self.players_rows[i], bg="green", width=80, height=130)
            player_name_frame.grid(row=0, column=0)
            player_name_label = Label(player_name_frame, text=str(self.mesa.jogadores[i].nome), bg="green", font=("Arial", 12)).place(relx=0.5, rely=0.5, anchor="center")


            for j in range(1, 16):
                card = Frame(self.players_rows[i], bg="white", width=60, height=90)
                self.players_rows[i].grid_columnconfigure(j, minsize=80)
                self.players_rows[i].grid_rowconfigure(0, minsize=130)
                card.grid(row=0, column=j, padx=2, pady=2)
                card_label = Label(card, text="", bg="white", font=("Arial", 30))
                
                if j <= len(self.mesa.jogadores[i].cartas):
                    card_label.config(text=self.mesa.jogadores[i].cartas[j - 1].valor, bg="grey")
                    card.config(bg="grey")

                card_label.place(relx=0.5, rely=0.5, anchor="center")

            self.players_rows[i].pack(side="top")

    def iniciar_partida(self):
        start_status = self.dog_server_interface.start_match(4)
        message = start_status.get_message()
        code = start_status.get_code()

        if code == '0' or code == '1':
            self.notify_result(message)
        else:
            baralho = Baralho()
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

            primeiro = self.mesa.verifica_se_turno_local()

            if not primeiro:
                # colocar comopr dicionario
                self.dog_server_interface.send_move(move= {"tipo": "iniciar_partida", "match_status" : "next"})

            self.update_ui()
            self.mesa.inicia_jogo()
            self.notify_result(message)

        print(start_status.get_players())
        self.mesa.jogador_local = str(start_status.get_local_id())

    def aceitar_carta(self):
        self.dog_server_interface.send_move(move= {"tipo": "aceitar_carta", "match_status" : "next"})
        self.notify_result("Aceitou carta")

    def recusar_carta(self):
        self.mesa.fichas_acumuladas += 1
        self.mesa.jogadores[int(self.mesa.jogador_local)].numero_fichas -= 1
        self.update_ui()
        self.dog_server_interface.send_move(move= {"tipo": "recusar_carta", "match_status" : "next"})
        self.notify_result("Recusou carta")


    # def open_popup(self, pop_up_text):
    #     top= Toplevel(self.root)
    #     top.title("Child Window")
    #     top.geometry("300x100")
    #     Label(top, text=pop_up_text, font=('Arial', 14)).place(relx=0.5, rely=0.5, anchor="center")

 
interface = InterfaceJogador()
    
