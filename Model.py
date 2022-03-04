import sqlite3
from datetime import datetime
from Score import *

class Model:
    
    def __init__(self):
        self.database_name = 'words.db' # Andmebaasi nimi
        self.new_word = None # Sõna mida ära arvatakse - String
        self.user_word = [] # Kasutaja leitud tähed
        self.all_user_chars = [] # Kõik valesti sisestatud tähed
        self.counter = 0 # Vigade loendur
        self.player_name = 'TEADMATA' # Mängija nimi kui pole sisestatud
        self.score_filename = 'score.txt' # Mängijate "edetabeli" failinimi
        self.score_data = [] # score.txt faili sisu
        
    def get_random_word(self):
        'Üks juhuslik sõna tabelist'
        connection = sqlite3.connect(self.database_name)
        cursor = connection.execute('SELECT * FROM words ORDER BY RANDOM() LIMIT 1') # AInult üks kijre
        self.new_word = cursor.fetchone()[1] # veerg word on [1] id on [0]
        connection.close()
        
    def set_new_game(self):
        'Tee uus mäng'
        self.get_random_word() # Tee uus sõna                
        self.user_word = [] # Leitud tähed eemaldada
        self.all_user_chars = [] # Valesti sisestatud tähed eemaldada
        self.counter = 0 # Vigade loendur nulliks
        for i in range(len(self.new_word)):
            self.user_word.append('_')
        #print(self.new_word) # Test!
        #print(self.user_word) # Test!
        
    def get_user_input(self, value):
        'Mida kasutaja sisestas'
        if value: # Kasutaja on midagi sisesatnud ja see pole tühi
            user_char = value[0:1] # Sõltumata stringi pikkusest ainult esimene märk 
            if user_char.lower() in self.new_word.lower(): # a in autojuht
                self.change_user_input(user_char) # Leiti
            else: # Ei leitud
                self.counter += 1 # Vigade loendur kasvab +1
                self.all_user_chars.append(user_char.upper())
                
    def change_user_input(self, user_char):              
        current_word = self.chars_to_list(self.new_word)
        i = 0
        for c in current_word:
            if user_char.lower() == c.lower():
                self.user_word[i] = user_char.upper()
            i += 1
    
    def chars_to_list(self, string):
        chars = []
        chars[:0] = string
        return chars
    
    def get_user_word(self):
        'Tagastab kasutaja leitud tähed'
        return self.user_word
    
    def get_counter(self):
        'Tagasta loenduri väärtus'
        return self.counter
    
    def get_all_user_chars(self):
        'Tagasta Listina kõik valed sisestuased'
        return ', '.join(self.all_user_chars)
    
    def reset_player_name(self):
        self.player_name = 'TEADMATA'
    
    def set_username(self, username):
        line = []
        now = datetime.now().strftime('%Y-%m-%d %T')
        if username:
            self.player_name = username
        
        line.append(now)
        line.append(self.player_name)
        line.append(self.new_word)
        line.append(self.get_all_user_chars())
        
        #print(line)
        with open(self.score_filename, 'a+', encoding='utf-8') as f:
            f.write(';'.join(line) + '\n')
        
    def read_file_contents(self):
        self.score_data = []
        with open(self.score_filename, 'r', encoding='utf-8') as f:
            all_lines = f.readlines() # Loe faili sisu listi
            for line in all_lines:
                parts = line.strip().split(';')
                self.score_data.append(Score(parts[0], parts[1], parts[2], parts[3]))
            #print(self.score_data[0].get_name()) # TEST!
        return self.score_data