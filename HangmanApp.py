from Controller import *

class HangmanApp:
    
    def __init__(self):
        app = Controller()
        app.main() # Graafiline aken mainloop
        
if __name__ == '__main__':
    hangman = HangmanApp()