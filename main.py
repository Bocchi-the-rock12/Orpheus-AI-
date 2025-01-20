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
20/01/2025 Criação do jogo hangman e update em algumas classes
======================================================
"""

from datetime import date
from nltk.corpus import words
import random


class Games:
    """ Manages playable games """
    def __init__(self):
        self.playing = True
        self.ai_score = 0
        self.player_score = 0

    class HiLo:
        """ Class to manage the HiLo game """
        def __init__(self, games: "Games"):
            self.games = games

        @staticmethod
        def initial_request():
            """ Takes the range numbers as input from user about
                RPre-condition: Hi > Lo"""
            lo = int(input(f"Think about a number... "))
            hi = int(input(f"Think about another number... "))
            if lo > hi:
                print("The lower bound can't be greater than the higher bound!")
            else:
                return lo, hi

        @staticmethod
        def ask(guess: int):
            attempt = input(f"My guess is {guess}. Is the secret number bigger (>), smaller (<) or equal (=) ? ")
            return attempt

        def final_message(self, lo, hi, attempts, guess):
            if lo > hi:
                print("You're a cheater!")
                self.games.player_score =- 1
                print(f"Your score: {self.games.player_score}")
            else:
                print(f"YAY! I won in {attempts} attempts! the secret number was {guess}!")
                self.games.ai_score =+ 1
                print(f"AI score: {self.games.ai_score}")

        def play_hilo_reverse(self):
            """ Function to play high-low game"""
            lo, hi = self.initial_request()
            attempts = 0

            while lo <= hi:
                guess = random.randint(lo, hi)
                attempts += 1
                response = Games.HiLo.ask(guess)

                if response == "=":
                    self.final_message(lo, hi, attempts, guess)
                    break
                elif response == ">":
                    lo = guess + 1
                elif response == "<":
                    hi = guess - 1
                else:
                    print("Invalid input. Please use only '>', '<', or '='.")

    class Quiz:
        print("ola")

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
        def end_game(visible: list[str], secret: str, attempts: int):
            if Games.Hangman.got_it_right(visible, secret):
                print(f"Congratulations! you guessed the secret in {attempts} '{secret}'!")
            else:
                print(f"Sorry, you surpassed the number of attempts. The secret was '{secret}'.")

    class RPS:
        """ Class to manage them game rock paper and scissors"""

        def __init__(self, games: "Games"):
            self.games = games

        moves = ["Rock", "Paper", "Scissors"]

        @staticmethod
        def move():
            return random.choice(Games.RPS.moves)

        def rock_paper_scissors(self):
            play = input("Rock, paper or scissors? ")
            if play not in Games.RPS.moves:
                print("Invalid move!")
            else:
                ai = Games.RPS.move()
                print(f"AI played: {ai}")
                if ai == play:
                    print("It's a tie!")
                elif (ai == "Rock" and play == "Paper") or \
                        (ai == "Paper" and play == "Scissors") or \
                        (ai == "Scissors" and play == "Rock"):
                    print("You won!")
                    self.games.player_score += 1
                else:
                    print("You lost!")
                    self.games.ai_score += 1

                print(f"Score: You {self.games.player_score} - {self.games.ai_score} AI")

        class WordScramble:
            print("oi")


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
