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
from random import randint
from nltk.corpus import words
import random


class Games:
    """ Manages playable games """
    def __init__(self):
        self.playing = True

    class HiLo:
        """ Class to manage the HiLo game """
        @staticmethod
        def initial_request():
            lo = int(input(f"Think about a number... "))
            hi = int(input(f"Think about another another number... "))
            return lo, hi

        @staticmethod
        def ask(guess: int):
            attempt = input(f"My guess is {guess}. Is the secret number bigger (>), smaller (<) or equal (=) ? ")
            return attempt

        @staticmethod
        def final_message(lo: int, hi: int, attempts: int, guess: int):
            if lo > hi:
                print("You're a cheater!")
            else:
                print(f"YAY! I won in {attempts} attempts! the secret number was {guess}!")

        @staticmethod
        def play_hilo_reverse(lo: int, hi: int):
            Games.HiLo.initial_request()
            attempts = 0
            while lo <= hi:
                guess = randint(lo, hi)
                attempts += 1
                response = Games.HiLo.ask(guess)
                if response == "=":
                    Games.HiLo.final_message(lo, hi, attempts, guess)
                    break
                elif response == ">":
                    lo = guess + 1
                elif response == "<":
                    hi = guess - 1
                else:
                    print("Invalid input. Please use only '>', '<', or '='.")

    def quiz(self):
        pass

    class Hangman:
        """ Class to manage the hangman game"""
        @staticmethod
        def choose_word():
            """ Get words from eng dictionary """
            word = random.choice(Data.english_dict)
            return word.lower()

        @staticmethod
        def update_visible(visible: list[str], secret: str, c: str):
            n = len(secret)

        @staticmethod
        def print_visible(visible: list[str]):
            print(" ".join(visible))

        @staticmethod
        def got_it_right(visible: list[str], secret: str) -> bool:
            return ''.join(visible) == secret

        @staticmethod
        def input_letter(prompt: str) -> str:
            while True:
                s = input(prompt)
                if len(s) == 1 and s.isalpha():
                    return s

        @staticmethod
        def end_game(visible: list[str], secret: str, attempts: int) -> str:
            if Games.Hangman.got_it_right(visible, secret):
                print(f"Congratulations! you guessed the secret in {attempts} '{secret}'!")
            else:
                print(f"Sorry, you surpassed the number of attempts. The secret was '{secret}'.")


    def rock_paper(self):
        pass

    def word_scramble(self):
        pass


class Chat:
    """ AI chatbot """
    def __init__(self):
        pass

    @staticmethod
    def chat():
        """ Receive chat input from user
            Pre-condition: Input must be valid """
        chat = input("Hello! How can I be of help?")


class Data:
    """ Manage program data (username, date, quotes, etc...) """

    # Variables shared by all methods
    date = date.today()
    quotes = []
    quiz_questions = []
    english_dict = words.words()

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

    def interpreter(self):
        pass

    @staticmethod
    def main():
        print("Orpheus AI!")
        games = Games()
        chat = Chat()
        data = Data()
        pass


UI.main()
