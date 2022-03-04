from tkinter import simpledialog
from Model import *
from View import *

class Controller:
    
    def __init__(self):
        self.model = Model()
        self.view = View(self)
        
    def main(self):
        'Kutsub View\'st välja mainloop()'
        self.view.main() # View.py failis olev main meetod
        
    def btn_new_click(self):
        'Uus mäng nupu vajutamine'
        #print('Klikiti nuppu Uus mäng') # Tet kas nupp töötab
        self.model.set_new_game() # Tee uus mäng
        self.view.label.configure(text=self.model.user_word) # Muutuja
        self.view.label_error.configure(text=f'Valesti 0 täht(e)', fg='black')
        self.view.btn_send['state'] = 'normal'
        self.model.reset_player_name()

    def btn_send_click(self):
        self.model.get_user_input(self.view.userinput.get().strip())
        #print(self.model.user_word) # Testiks
        self.view.label.configure(text=self.model.get_user_word()) # Samas mis rida 17 meetod
        self.view.label_error.configure(text=f'Valesti {self.model.get_counter()} täht(e). {self.model.get_all_user_chars()}')
        self.view.char_input.delete(0, 'end') # Tühjendab vormi (Entry väli)
        if self.model.get_counter() > 0:
            self.view.label_error.configure(fg='red')
        self.is_game_over()
        
    def is_game_over(self):
        if self.model.get_counter() >= 8 or '_' not in self.model.get_user_word():            
            self.view.btn_send['state'] = 'disabled'            
            player_name = simpledialog.askstring('Mäng läbi', 'Mäng on läbi!\nKuidas on mängija nimi?', parent=self.view)
            #print(type(player_name))
            self.model.set_username(player_name) # Saadama saadud info mudelile
            
    def btn_scoreboard_click(self):        
        popup_frame = self.view.create_popup_window() # Frame
        data = self.model.read_file_contents() # Loe faili sisu Listi (Objekt)
        self.view.generate_scoreboard(popup_frame, data)