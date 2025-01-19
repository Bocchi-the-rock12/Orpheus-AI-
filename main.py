"""
------------------------------------------------------
Projeto do presente: Orpheus AI

*** AI BOT ***

AUTHORS IDENTIFICATION 
  - Afonso Ferreira

Comments:
-
------------------------------------------------------

======================================================
CHANGELOG:
18/01/2025 Criação das classes GAMES, CHAT, DATA e UI
19/01/2025 Implementação das funções dos jogos
======================================================
"""

from datetime import date


class GAMES:
    """ Manages playable games """
    def __init__(self):
        pass

    def hilo(self):
        """ High-low game with AI or multiplayer mode """
        pass

    def quiz(self):
        pass

    def hangman(self):
        pass

    def rock_paper(self):
        pass

    def word_scramble(self):
        pass


class CHAT:
    """ AI chatbot """
    def __init__(self):
        pass

    @staticmethod
    def chat():
        """ Receive chat input from user
            Pre-condition: Input must be valid """
        chat = input("Hello! How can I be of help?")


class DATA:
    """ Manage program data (username, date, quotes, etc...) """

    # Variables shared by all methods
    date = date.today()

    def __init__(self):
        pass

    def user_data(self):
        pass

    def game_data(self):
        pass

class UI:
    """ Handles user interaction """
    def __init__(self):
        pass

    @staticmethod
    def main():
        print("Welcome to Orpheus AI!")
        games = GAMES()
        chat = CHAT()
        data = DATA()
        pass


UI.main()
