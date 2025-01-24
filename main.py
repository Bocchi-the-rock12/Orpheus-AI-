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
24/01/2025 Modificado o jogo da forca e criadas funções para interpretar comandos
======================================================
"""

from datetime import date
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
                Pre-condition: Hi > Lo """
            while True:
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
            """ Get a random word from the word file """
            words = []
            with open("words.txt", mode="r", encoding="utf-8") as f:
                content = f.readlines()
            for line in content:
                words.append(line.strip())
            return random.choice(words)

        @staticmethod
        def update_visible(visible: list[str], secret: str, c: str):
            for i in range(len(secret)):
                if secret[i] == c:
                    visible[i] = c

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

        @staticmethod
        def interaction(secret: str, max_attempts: int):
            """ Main game loop """
            visible = ['_'] * len(secret)
            guessed_letters = []
            Games.Hangman.print_visible(visible)
            attempts_used = 1
            while max_attempts > attempts_used:
                letter = Games.Hangman.input_letter("Insert a letter: ")

                # Checks if the letter was already guessed
                if letter in guessed_letters:
                    Chat.typing_effect(f"You already guessed the letter {letter}!", delay=0.1 / 1.5)
                    continue

                guessed_letters.append(letter)

                # Confirms if the letter is in the secret
                if letter not in secret:
                    Chat.typing_effect(f"The letter {letter} is not in the secret.", delay=0.1 / 1.5)
                    attempts_used += 1
                    Chat.typing_effect(f"Attempts used: {attempts_used}", delay=0.1 / 1.5)
                else:
                    Chat.typing_effect(f"The letter {letter} is in the secret.", delay=0.1 / 1.5)
                    Games.Hangman.update_visible(visible, secret, letter)
                    Chat.typing_effect(f"Attempts used: {attempts_used}", delay=0.1 / 1.5)

                Games.Hangman.print_visible(visible)

                if Games.Hangman.got_it_right(visible, secret):  # If the word is fully revealed
                    break

            Games.Hangman.end_game(visible, secret, attempts_used)  # End the game with a result

        @staticmethod
        def play_hangman():
            MAX_ATTEMPTS = 11
            Games.Hangman.interaction(Games.Hangman.choose_word(), MAX_ATTEMPTS)

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
    def typing_effect(text: str, delay: float = 0.1):
        console = Console()

        for char in text:
            console.print(char, end="")
            time.sleep(delay)

        console.print()

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

    def __init__(self):
        pass


class UI:
    """ Handles user interaction """
    def __init__(self):
        self.chat_instance = Chat()
        self.games = Games()
        self.chat = Chat()
        self.data = Data()

    def games_commands(self):
        """ This handles game command choices """
        Chat.typing_effect("Open a game:", delay=0.1 / 1.5)
        Chat.typing_effect("- High-low", delay=0.1 / 1.5)
        Chat.typing_effect("- Hangman", delay=0.1 / 1.5)
        Chat.typing_effect("- Rock, paper or scissors", delay=0.1 / 1.5)

        while True:
            game_choice = UI.input_command()
            if game_choice not in ["high-low", "hangman", "rock, paper or scissors"]:
                Chat.typing_effect(f"Sorry, we don't have {game_choice} available yet.", delay=0.1 / 1.5)
            else:
                match game_choice:
                    case "high-low":
                        hilo_game = Games.HiLo(self.games)
                        self.games.playing = True
                        while self.games.playing:
                            hilo_game.play_hilo_reverse()
                        self.games.playing = False

                    case "hangman":
                        hangman_game = Games.Hangman()
                        self.games.playing = True
                        while self.games.playing:
                            hangman_game.play_hangman()
                        self.games.playing = False

                    case "rock, paper or scissors":
                        rps_game = Games.RPS(self.games)
                        self.games.playing = True
                        while self.games.playing:
                            rps_game.rock_paper_scissors()
                        self.games.playing = False

    def chat_commands(self):
        """ Placeholder for chat commands if needed in the future """
        pass

    @staticmethod
    def command_help():
        """ Display the available commands to the user """
        Chat.typing_effect("Available commands:", delay=0.1 / 1.5)
        Chat.typing_effect("- Games, for playing our available games", delay=0.1 / 1.5)
        Chat.typing_effect("- Chat, to interact with our AI", delay=0.1 / 1.5)
        Chat.typing_effect("- Daily quote, to get your daily love quote (Note: only available for the wife)",
                           delay=0.1 / 1.5)
        Chat.typing_effect("- Exit, to leave the application", delay=0.15)

    def interpreter(self):
        """ Command interpreter for controlling the flow of the app """
        while True:
            command = UI.input_command()  # Get user command
            match command:
                case "games":
                    self.games_commands()  # Call to handle game selection
                case "chat":
                    self.chat_commands()  # Placeholder for future chat functionality
                case "exit":
                    Chat.typing_effect("Thanks for using our AI.", delay=0.1 / 1.5)
                    break
                case "help":
                    self.command_help()  # Display available commands
                case _:
                    Chat.typing_effect("Unknown command.", delay=0.1 / 1.5)

    @staticmethod
    def input_command():
        """ Get and process user input command """
        command = input("> ").lower()
        return command

    def main(self):
        """ Main entry point for starting the app """
        name = input("Insert your name: ").lower()
        if name == "shivali" or name == "shivali thakur" or name == "shivali vinodkumar thakur":
            Chat.typing_effect(Data.welcoming_message, delay=0.1 / 1.5)
        Chat.typing_effect("Type help for command list.", delay=0.1 / 1.5)
        self.interpreter()  # Start the interaction loop


# Run the UI
if __name__ == "__main__":
    ui_instance = UI()  # Create an instance of UI
    ui_instance.main()  # Start the main function

