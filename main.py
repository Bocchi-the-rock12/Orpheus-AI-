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
22/01/2025 Adicionada a função para efeitos de texto
======================================================
"""

from datetime import date
import nltk
import random
import time
from rich.console import Console
from rich.text import Text

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
                Pre-condition: Hi > Lo"""
            lo = int(input(f"Think about a number... "))
            hi = int(input(f"Think about another number... "))
            if lo > hi:
                Chat.typing_effect("The lower bound can't be greater than the higher bound!", delay=0.2)
            else:
                return lo, hi

        @staticmethod
        def ask(guess: int):
            attempt = input(f"My guess is {guess}. Is the secret number bigger (>), smaller (<) or equal (=) ? ")
            return attempt

        def final_message(self, lo, hi, attempts, guess):
            if lo > hi:
                Chat.typing_effect("You're a cheater!", delay=0.2)
                self.games.player_score -= 1
                Chat.typing_effect(f"Your score: {self.games.player_score}", delay=0.2)
            else:
                Chat.typing_effect(f"YAY! I won in {attempts} attempts! The secret number was {guess}!", delay=0.2)
                self.games.ai_score += 1
                Chat.typing_effect(f"AI score: {self.games.ai_score}", delay=0.2)

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
                    Chat.typing_effect("Invalid input. Please use only '>', '<', or '='.", delay=0.2)

    class LoveQuiz:
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
            Chat.typing_effect(" ".join(visible), delay=0.2)

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
                Chat.typing_effect(f"Congratulations! You guessed the secret in {attempts} attempts: '{secret}'!", delay=0.2)
            else:
                Chat.typing_effect(f"Sorry, you surpassed the number of attempts. The secret was '{secret}'.", delay=0.2)

    class RPS:
        """ Class to manage the game rock paper and scissors"""
        def __init__(self, games: "Games"):
            self.games = games

        moves = ["Rock", "Paper", "Scissors"]

        @staticmethod
        def move():
            return random.choice(Games.RPS.moves)

        def rock_paper_scissors(self):
            play = input("Rock, paper or scissors? ")
            if play not in Games.RPS.moves:
                Chat.typing_effect("Invalid move!", delay=0.2)
            else:
                ai = Games.RPS.move()
                Chat.typing_effect(f"AI played: {ai}", delay=0.2)
                if ai == play:
                    Chat.typing_effect("It's a tie!", delay=0.2)
                elif (ai == "Rock" and play == "Paper") or \
                        (ai == "Paper" and play == "Scissors") or \
                        (ai == "Scissors" and play == "Rock"):
                    Chat.typing_effect("You won!", delay=0.2)
                    self.games.player_score += 1
                else:
                    Chat.typing_effect("You lost!", delay=0.2)
                    self.games.ai_score += 1

                Chat.typing_effect(f"Score: You {self.games.player_score} - {self.games.ai_score} AI", delay=0.2)



class Chat:
    """ AI chatbot """
    def __init__(self):
        self.chating = True

    @staticmethod
    def typing_effect(text, delay=0.1):
        console = Console()
        rich_text = Text(text)
        for char in rich_text:
            console.print(char, end="")  # Make sure flush is used with `Console.print()`
            time.sleep(delay)

        console.print()  # Move to the next line after typing is done

    @staticmethod
    def chat():
        """ Receive chat input from user """
        input("Hello! How can I be of help?")


class Data:
    """ Manage program data (username, date, quotes, etc...) """

    # Variables shared by all methods
    date = date.today()
    quotes = ["I love you so much amor", "I'm so glad to have you", "I hope you enjoy this gift <3"]
    welcoming_message = "Hi baby, if you’re reading this then it means you already received the gift. I just want to say that I love you a lot, and I did this with the best of intentions and love for you. Amo-te muito amor <3"
    quiz_game= {
        "What was the date we confessed to each other?": {
            "options": ["14/02/2024", "10/03/2024", "25/12/2023", "01/06/2024"],
            "answer": "10/03/2024"
        },
        "What is Afonso's favorite movie?": {
            "options": ["Wall-E", "Tangled", "Interstellar", "Star Wars"],
            "answer": "Wall-E"
        },
        "What is Afonso's favorite food?": {
            "options": ["Sushi", "Carbonara", "Pizza", "Rice"],
            "answer": "Carbonara"
        },
        "What is Shivali's favorite color?": {
            "options": ["Red", "Blue", "Green", "Pink"],
            "answer": "Red"
        },
        "Who said 'I love you' first?": {
            "options": ["Afonso", "Shivali", "Neither, we both said it at the same time", "It was a mutual confession"],
            "answer": "Afonso"
        },
        "What is Shivali's favorite food?": {
            "options": ["Panipuri", "Biryani", "Pasta", "Ice cream"],
            "answer": "Panipuri"
        },
        "What goal do we want to achieve in the future?": {
            "options": ["Traveling around the world", "Living happily together, no matter how", "Starting a family",
                        "Becoming financially independent"],
            "answer": "Living happily together, no matter how"
        },
        "Where do we dream of living in the future?": {
            "options": ["In a big city", "Anywhere as long as we're together", "In the countryside", "Near the beach"],
            "answer": "Anywhere as long as we're together"
        },
        "What nickname does Afonso prefer to be called?": {
            "options": ["Bae", "Love", "Honey", "Hubby"],
            "answer": "Love"
        },
        "What song reminds Afonso of her?": {
            "options": ["I Like You from Post Malone", "Shape of You by Ed Sheeran", "Perfect by Ed Sheeran",
                        "Counting Stars by OneRepublic"],
            "answer": "I Like You from Post Malone"
        },
        "What's Afonso's favorite place in Lisbon?": {
            "options": ["The planetarium", "Belem Tower", "Chiado", "Mosteiro dos jeronimos"],
            "answer": "The planetarium"
        },
        "What's Afonso's favorite subject?": {
            "options": ["Mathematics", "Chemistry", "Physics", "Literature"],
            "answer": "Mathematics"
        },
        "What's Afonso's favorite animal?": {
            "options": ["Peacocks", "Orcas", "Butterflies", "Cats"],
            "answer": "Peacocks"
        },
        "What's Shivali's favorite color?": {
            "options": ["Purple", "Red", "Yellow", "Green"],
            "answer": "Purple"
        },
        "What's Shivali's favorite hobby?": {
            "options": ["Reading", "Sleeping", "Painting", "Dancing"],
            "answer": "Sleeping"
        },
        "What food is Shivali's favorite Italian cuisine?": {
            "options": ["Neetlank", "Pizza", "Pasta", "Lasagna"],
            "answer": "Neetlank"
        },
        "How does Shivali like her food?": {
            "options": ["With spices and tasty", "Mild and savory", "Sweet and sour", "Spicy but not too hot"],
            "answer": "With spices and tasty"
        },
        "What's Afonso's favorite season?": {
            "options": ["Summer", "Winter", "Spring", "Autumn"],
            "answer": "Summer"
        },
        "What's Afonso's favorite dessert?": {
            "options": ["Doce da casa", "Baba de camelo", "Bolo de bolacha", "Soufle"],
            "answer": "Doce da casa"
        },
        "What is Afonso's favorite anime?": {
            "options": ["Souson no Frieren", "Bocchi the Rock", "Bluelock", "Kimetsu no Yaiba"],
            "answer": "Souson no Frieren"
        },
        "What's Afonso's favorite videogame?": {
            "options": ["Fallout 4", "GTA V", "Genshin Impact", "Pokémon"],
            "answer": "Fallout 4"
        },
        "What does Afonso loves more about Shivali?": {
            "options": ["Her kindness", "Her cuteness", "Her intelligence", "Everything above and more"],
            "answer": "Everything above and more"
        }
    }

    try:
        nltk.data.find('corpora/words.zip')
    except LookupError:
        print("Downloading NLTK words corpus...")
        nltk.download('words')

    def __init__(self):
        pass

    def user_data(self):
        pass

    def game_data(self):
        pass

class UI:
    """ Handles user interaction """

    def __init__(self):
        self.chat_instance = Chat()
        self.games = Games()
        self.chat = Chat()
        self.data = Data()

    def interpreter(self):
        pass

    def main(self):
        Chat.typing_effect(self.data.welcoming_message, delay=0.1 / 1.5)
        Chat.typing_effect("Orpheus AI", delay=0.1 / 1.5)

        while True:
            user_input = input("> ")
            user_input.lower()
            match user_input:
                case "games":
                    Chat.typing_effect("Games", delay=0.1 / 1.5)
                case "chat":
                    Chat.typing_effect("Chat", delay=0.1 / 1.5)
                case "exit":
                    Chat.typing_effect("Thanks for using our AI.", delay=0.1 / 1.5)
                    break
                case _:
                    Chat.typing_effect("Unknown command.", delay=0.1 / 1.5)

Main_function = UI()
Main_function.main()

