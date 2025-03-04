"""
------------------------------------------------------
Projeto do presente: Orpheus AI

*** AI BOT ***

AUTHORS IDENTIFICATION
  - Afonso Ferreira

Comments:
- Some parts of the main code frame where also done with the assistance of AI
- the website was built with AI
------------------------------------------------------

======================================================
CHANGELOG:
18/01/2025 Criação das classes GAMES, CHAT, DATA e UI
19/01/2025 Implementação das funções dos jogos
20/01/2025 Criação do jogo hangman e update em algumas classes
22/01/2025 Adicionada a função para efeitos de texto
24/01/2025 Modificado o jogo da forca e criadas funções para interpretar comandos
1/02/2025 Implementada a função de love quote
======================================================
"""

import time
from datetime import date
import random
from rich.console import Console
import json
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Pre-requisites download
nltk.download("punkt_tab", quiet=True)
nltk.download("wordnet", quiet=True)
nltk.download("stopwords", quiet=True)

# Check for the standard punkt
try:
    nltk.data.find("tokenizers/punkt/english.pickle")
except LookupError:
    nltk.download("punkt", quiet=True)

# Check for the punkt_tab
try:
    nltk.data.find("tokenizers/punkt_tab/english")
except LookupError:
    nltk.download("punkt_tab", quiet=True)


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
                Chat.typing_effect("I want you to think about a number... Keep it to yourself", delay=0.1 / 1.5)
                Chat.typing_effect("Now, I need you to give me an interval where that number is located", delay=0.1 / 1.5)
                lo = int(input(f"Think about a number... "))
                hi = int(input(f"Think about another number... "))
                if lo > hi:
                    Chat.typing_effect("The lower bound can't be greater than the higher bound!", delay=0.1 / 1.5)
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
                    return  # Exit after winning
                elif response == ">":
                    lo = guess + 1
                elif response == "<":
                    hi = guess - 1
                else:
                    Chat.typing_effect("Invalid input. Please use only '>', '<', or '='.", delay=0.2)

                # Check if cheating occurred during gameplay
                if lo > hi:
                    Chat.typing_effect("You're a cheater!", delay=0.2)
                    self.games.player_score -= 1
                    Chat.typing_effect(f"Your score: {self.games.player_score}", delay=0.2)
                    return


    class LoveQuiz:
        """ Class to manage the love quiz """
        def __init__(self, games: "Games"):
            self.games = games

        @staticmethod
        def questions():
            questions = []
            for key in Data.quiz_game:
                questions.append(key)
            return questions

        @staticmethod
        def get_question(questions):
            return random.choice(questions)

        @staticmethod
        def ask_question(question):
            options_list = Data.quiz_game[question]["options"]
            Chat.typing_effect("Choose your answer from the options below:", delay=0.1 / 1.5)

            for i in range(len(options_list)):
                Chat.typing_effect(f"{chr(65 + i)}: {options_list[i]}", delay=0.1 / 1.5)

        @staticmethod
        def answers():
            answers = []
            for key in Data.quiz_game:
                answer = Data.quiz_game[key]["answer"]
                answers.append(answer)
            return answers

        def game(self):
            questions = self.questions()
            text_answers = self.answers()

            Chat.typing_effect("Welcome to the ultimate love quiz!", delay=0.1 / 1.5)
            Chat.typing_effect(
                "This game was designed entirely by Afonso, and serves as a gift for his beautiful wife.",
                delay=0.1 / 1.5)
            Chat.typing_effect("Let the game begin...", delay=0.1 / 1.5)

            while True:
                question_chosen = self.get_question(questions)
                Chat.typing_effect(f"{question_chosen}", delay=0.1 / 1.5)
                self.ask_question(question_chosen)

                # Manually get the correct answer
                correct_text_answer = text_answers[questions.index(question_chosen)]
                correct_answer_index = Data.quiz_game[question_chosen]["options"].index(correct_text_answer)
                correct_answer = chr(65 + correct_answer_index)

                while True:
                    answer = input("> ").upper().strip()

                    if answer not in ["A", "B", "C", "D"]:
                        Chat.typing_effect("Invalid input. Please choose a valid option.", delay=0.1 / 1.5)
                    else:
                        if answer == correct_answer:
                            Chat.typing_effect("DING DING DING! You are correct.", delay=0.1 / 1.5)
                            self.games.player_score += 1
                            Chat.typing_effect(f"Current score: {self.games.player_score}", delay=0.1 / 1.5)
                        else:
                            Chat.typing_effect(f"Sorry, the correct answer was {correct_answer}", delay=0.1 / 1.5)
                        break
                # Checks if user wants to play again
                if not UI.game_replay():
                    return


    class Hangman:
        """ Class to manage the hangman game"""
        def __init__(self, games: "Games"):
            self.games = games

        @staticmethod
        def choose_word(file_path) -> str:
            """ Get a random word from the Word file """
            words = []
            file = open(file_path, "r", encoding="utf-8")
            content = file.readlines()
            for line in content:
                words.append(line)
            return random.choice(words)

        @staticmethod
        def update_visible(visible: list[str], secret: str, c: str):
            for i in range(len(secret)):
                if secret[i] == c:
                    visible[i] = c

        @staticmethod
        def print_visible(visible: list[str]):
            Chat.typing_effect(" ".join(visible), delay = 0.1 / 1.5)

        @staticmethod
        def got_it_right(visible: list[str], secret: str) -> bool:
            return ''.join(visible) == secret

        @staticmethod
        def input_letter(prompt: str) -> str:
            while True:
                s = input(prompt)
                if len(s) == 1 and (s.isalpha() or s == "-"):
                    return s

        @staticmethod
        def end_game(visible: list[str], secret: str, attempts: int):
            if Games.Hangman.got_it_right(visible, secret):
                Chat.typing_effect(f"Congratulations! You guessed the secret in {attempts} attempts: '{secret}'!", delay=0.1 / 1.5)
            else:
                Chat.typing_effect(f"Sorry, you surpassed the number of attempts. The secret was '{secret}'.", delay=0.1 / 1.5)

        @staticmethod
        def interaction(secret: str, max_attempts: int):
            """ Main game loop """
            visible = ['_'] * len(secret)
            guessed_letters = []
            Games.Hangman.print_visible(visible)
            attempts_used = 0
            while max_attempts > attempts_used:
                letter = Games.Hangman.input_letter("Insert a letter: ")

                # Checks if the letter was already guessed
                if letter in guessed_letters:
                    Chat.typing_effect(f"You already guessed the letter {letter}.", delay=0.1 / 1.5)
                    continue

                guessed_letters.append(letter)

                # Confirms if the letter is in the secret
                if letter not in secret:
                    Chat.typing_effect(f"The letter {letter} is not in the secret.", delay=0.1 / 1.5)
                    attempts_used += 1
                    Chat.typing_effect(f"Errors: {attempts_used}", delay=0.1 / 1.5)
                else:
                    Chat.typing_effect(f"The letter {letter} is in the secret.", delay=0.1 / 1.5)
                    Games.Hangman.update_visible(visible, secret, letter)
                    Chat.typing_effect(f"Attempts used: {attempts_used}", delay=0.1 / 1.5)

                Games.Hangman.print_visible(visible)

                if Games.Hangman.got_it_right(visible, secret):
                    break

            Games.Hangman.end_game(visible, secret, attempts_used)

        @staticmethod
        def play_hangman():
            max_attempts = 10
            Games.Hangman.interaction(Games.Hangman.choose_word(r"/home/afonso/PycharmProjects/Orpheus-AI-/dataset/English Dictionary/words.txt"), max_attempts)

    class RPS:
        """ Class to manage the game rock paper and scissors """
        def __init__(self, games: "Games"):
            self.games = games

        moves = ["rock", "paper", "scissors"]

        @staticmethod
        def move():
            return random.choice(Games.RPS.moves)

        def rock_paper_scissors(self):
            while True:
                play = input("Rock, paper or scissors? ").strip().lower()
                if play not in Games.RPS.moves:
                    Chat.typing_effect("Invalid move!", delay=0.2)
                    continue
                else:
                    ai = Games.RPS.move().lower()
                    Chat.typing_effect(f"AI played: {ai}", delay=0.2)

                    if ai == play:
                        Chat.typing_effect("It's a tie!", delay=0.2)
                        break
                    elif (ai == "rock" and play == "paper") or (ai == "paper" and play == "scissors") or (
                            ai == "scissors" and play == "rock"):
                        Chat.typing_effect("You won!", delay=0.2)
                        self.games.player_score += 1
                        break
                    else:
                        Chat.typing_effect("You lost!", delay=0.2)
                        self.games.ai_score += 1
                        Chat.typing_effect(f"Score: You {self.games.player_score} - {self.games.ai_score} AI", delay=0.1 / 1.5)
                        break


class Chat:
    """ Class to handle chat information and AI"""

    # Initialize our lemmatizer and stopwords.
    lemmatizer = WordNetLemmatizer()
    stop_words = set(stopwords.words("english"))
    save_new_questions = False

    @staticmethod
    def typing_effect(text: str, delay: float = 0.1):
        console = Console()
        for char in text:
            console.print(char, end="")
            time.sleep(delay)
        console.print()

    @staticmethod
    def daily_love_quotes(quotes: list[str]):
        """Displays the daily love quote."""
        if not Data.checked_daily_quote:
            Data.checked_daily_quote = True
            Chat.typing_effect(random.choice(quotes), delay=0.1 / 1.5)
        else:
            Chat.typing_effect("You already checked your daily love quote!", delay=0.1 / 1.5)

    @staticmethod
    def preprocess_text(text: str):
        """
        Tokenizes, removes stopwords, and lemmatizes the input text.
        Filters out non-alphanumeric tokens for cleaner processing.
        """
        tokens = word_tokenize(text.lower())
        filtered_tokens = [word for word in tokens if word not in Chat.stop_words and word.isalnum()]
        lemmatized_tokens = [Chat.lemmatizer.lemmatize(token) for token in filtered_tokens]
        return lemmatized_tokens

    @staticmethod
    def load_json(file_path: str) -> list:
        """Loads JSON data from a file with error handling."""
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                return json.load(file)
        except FileNotFoundError:
            return []
        except json.JSONDecodeError:
            print("Error reading JSON file.")
            return []

    @staticmethod
    def process_single_query(query: str, file_path: str) -> str:
        """
        Processes a single query using a single JSON file for both predefined and dynamic Q&A.
        It first checks for greetings, then an exact match, and finally uses fuzzy matching.
        """
        # Define common greetings
        greetings = {
            "hello", "hi", "hey", "good morning", "good afternoon", "good evening",
            "howdy", "what's up", "yo", "greetings"
        }

        # Check if the input is a greeting
        if query.strip().lower() in greetings:
            return "Hello kind human, how can I be of service to you?"

        # Load responses from the file
        data = Chat.load_json(file_path)

        # Try to find a direct (exact) match first.
        for entry in data:
            if 'Input' in entry and entry['Input'].strip().lower() == query.strip().lower():
                return entry['Output']

        # If no direct match is found, use fuzzy matching.
        user_tokens = Chat.preprocess_text(query)
        best_match_index = None
        best_match_score = 0.0

        for index, entry in enumerate(data):
            question = entry.get("Input", "").strip()
            if not question:
                continue
            question_tokens = Chat.preprocess_text(question)
            if not question_tokens:
                continue
            common_tokens = set(user_tokens).intersection(set(question_tokens))
            score = len(common_tokens) / len(question_tokens)
            if score > best_match_score:
                best_match_score = score
                best_match_index = index

        threshold = 0.4
        if best_match_index is not None and best_match_score >= threshold:
            return data[best_match_index]["Output"]
        else:
            if Chat.save_new_questions:
                Chat.append_unknown_question(query, file_path)
            return "We're sorry, our bot can't answer that question yet."

    @staticmethod
    def get_ai_response(user_input: str, file_path: str):
        """
        Processes user input—splitting multipart queries if needed—and provides a response
        using a single JSON file for all responses.
        """
        lower_input = user_input.strip().lower()

        # Handle multipart queries separated by " and "
        if " and " in lower_input:
            parts = [part.strip() for part in lower_input.split(" and ")]
            responses = [Chat.process_single_query(part, file_path) for part in parts]
            final_response = "\n".join(responses)
        else:
            final_response = Chat.process_single_query(lower_input, file_path)
        Chat.typing_effect(final_response, delay=0.1 / 1.5)

    @staticmethod
    def append_unknown_question(question: str, file_path: str, placeholder="ANSWER"):
        """Appends an unrecognized question to the JSON file with a placeholder answer."""
        data = Chat.load_json(file_path)
        # Check if the question already exists (exact match)
        if any(entry.get("Input", "").strip().lower() == question.strip().lower() for entry in data):
            return
        data.append({"Input": question, "Output": placeholder})
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=2)


class Data:
    """ Manage program data (username, date, quotes, etc...) """
    # Variables shared by all methods
    checked_daily_quote = False
    date = date.today()
    username = str
    quotes = ["I hope you enjoy this gift <3", "I am so glad to have you",
              "I hope you know how much you mean to me", "I love you so much", "You're the best", "I have the best wife ever",
              "This gift is for the best person in the universe :3", "You're simply amazing", "I hope we can be together one day",
              "You're like a blackhole, you suck all my attention", "I don't know what I'd do without you"]
    last_checked_date = None
    last_quote = None
    welcoming_message = "Hi baby, if you’re reading this then it means you already received the gift. I just want to say that I love you a lot, and I did this with the best of intentions and love for you. Amo-te muito amor <3"
    quiz_game = {
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
        "What's Afonso's favorite color?": {
            "options": ["Purple", "Red", "Yellow", "Green"],
            "answer": "Purple"
        },
        "What's Shivali's favorite hobby?": {
            "options": ["Reading", "Sleeping", "Painting", "Dancing"],
            "answer": "Sleeping"
        },
        "What food is Shivali's favorite restaurant?": {
            "options": ["Neelkanth", "McDonald's", "Pizzahut", "Any restaurant works"],
            "answer": "Neelkanth"
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
        "What does Afonso love more about Shivali?": {
            "options": ["Her kindness", "Her cuteness", "Her intelligence", "Everything above and more"],
            "answer": "Everything above and more"
        },
        "Where did we first meet?": {
            "options": ["In school", "Online, specifically on Instagram", "At a restaurant", "At the mall"],
            "answer": "Online, specifically on Instagram"
        },
        "What is Afonso's dream job?": {
            "options": ["Research in Mathematics", "Working at a supermarket", "Janitor", "Working at a physics lab"],
            "answer": "Research in Mathematics"
        },
        "Who takes longer to get ready?": {
            "options": ["Afonso", "Shivali", "We both take time", "We're both fast"],
            "answer": "We're both fast"
        },
        "Who's more likely to fall asleep while we're talking at night?": {
            "options": ["Afonso", "Shivali"],
            "answer": "Afonso"
        },
        "Who's more likely to say 'I'm hungry' first?": {
            "options": ["Afonso", "Shivali", "Both of us"],
            "answer": "Afonso"
        },
        "What's a skill Afonso would like us to learn together?": {
            "options": ["Cooking", "Dancing", "Painting", "Learning a new language"],
            "answer": "Cooking"
        },
        "Who loses things more often?": {
            "options": ["Afonso", "Shivali"],
            "answer": "Afonso"
        },
        "What's Shivali's favorite weather?": {
            "options": ["Sunny", "Rain", "Cloudy", "Windy"],
            "answer": "Rain"
        },

        "What is the smallest unit of matter?": {
            "options": ["Atom", "Molecule", "Quark", "Electron"],
            "answer": "Quark"
        },
        "What is the chemical symbol for gold?": {
            "options": ["Go", "Au", "Ag", "Pt"],
            "answer": "Au"
        },
        "Which planet in our solar system has the most moons?": {
            "options": ["Jupiter", "Saturn", "Neptune", "Mars"],
            "answer": "Saturn"
        },
        "What gas do plants absorb from the atmosphere?": {
            "options": ["Oxygen", "Carbon Dioxide", "Nitrogen", "Hydrogen"],
            "answer": "Carbon Dioxide"
        },
        "Which part of the human body contains the most bones?": {
            "options": ["Legs", "Arms", "Hands", "Feet"],
            "answer": "Hands"
        },    "What is the unit of specific heat capacity in the SI system?": {
        "options": ["J/kg·°C", "J/g·°C", "J/mol·°C", "J/m²·°C"],
        "answer": "J/kg·°C"}
    }

    @staticmethod
    def is_wife(name):
        return name in ["shivali", "shivali thakur", "shivali vinodkumar thakur"]


class UI:
    def __init__(self):
        """Initializes the UI and loads the chatbot model."""
        # Although Chat methods are static, we create an instance in case we extend functionality.
        self.chat_instance = Chat()
        self.games = Games()
        self.data = Data()

    @staticmethod
    def game_replay():
        while True:
            message = input("Would you like to continue playing? y/n ").strip().lower()
            if message == "y":
                return True
            elif message == "n":
                return False
            else:
                print("Invalid input!")

    def games_commands(self):
        """ This handles game command choices """
        while True:
            Chat.typing_effect("Open a game:", delay=0.1 / 1.5)
            Chat.typing_effect("- High-low", delay=0.1 / 1.5)
            Chat.typing_effect("- Hangman", delay=0.1 / 1.5)
            Chat.typing_effect("- Rock, paper or scissors", delay=0.1 / 1.5)
            Chat.typing_effect("- Love quiz", delay=0.1 / 1.5)

            game_choice = UI.input_command()

            # Checks if user wants to quit the game menu
            if game_choice == "exit":
                return

            # Checks for valid input
            if game_choice not in ["high-low", "hangman", "rock, paper or scissors", "love quiz"]:
                Chat.typing_effect(f"Sorry, we don't have {game_choice} available yet.", delay=0.1 / 1.5)
                continue

            # Play the selected game
            if game_choice == "high-low":
                hilo_game = Games.HiLo(self.games)
                hilo_game.play_hilo_reverse()
                if not self.game_replay():
                    return
            elif game_choice == "hangman":
                hangman_game = Games.Hangman
                hangman_game.play_hangman()
                if not self.game_replay():
                    return
            elif game_choice == "rock, paper or scissors":
                rps_game = Games.RPS(self.games)
                rps_game.rock_paper_scissors()
                if not self.game_replay():
                    return
            elif game_choice == "love quiz":
                love_quiz = Games.LoveQuiz(self.games)
                love_quiz.game()

    @staticmethod
    def chat_commands():
        """Runs the chat loop """
        while True:
            user_input = UI.input_command()
            if user_input.lower() in ["exit", "quit"]:
                Chat.typing_effect("Exiting...", delay = 0.1 / 1.5)
                return
            Chat.get_ai_response(user_input, r"A:\College\Orpheus-AI-\dataset\Database\personal database.json")

    @staticmethod
    def daily_quote_command():
        Chat.daily_love_quotes(Data.quotes)

    @staticmethod
    def command_help():
        """ Display the available commands to the user """
        Chat.typing_effect("Available commands:", delay=0.1 / 1.5)
        Chat.typing_effect("- Games, for playing our available games", delay=0.1 / 1.5)
        Chat.typing_effect("- Chat, to interact with our AI", delay=0.1 / 1.5)
        Chat.typing_effect("- Daily quote, to get your daily love quote (Note: only available for the wife)",
                           delay=0.1 / 1.5)
        Chat.typing_effect("- Exit, to leave the application", delay=0.1 / 1.5)

    def interpreter(self):
        """ Command interpreter for controlling the app """
        while True:
            command = UI.input_command()
            match command:
                case "games":
                    self.games_commands()
                case "chat":
                    self.chat_commands()
                case "exit":
                    Chat.typing_effect("Thanks for using our AI.", delay=0.1 / 1.5)
                    break
                case "help":
                    self.command_help()
                case "daily quote":
                    if Data.is_wife(Data.username):
                        Chat.daily_love_quotes(Data.quotes)
                    else:
                        Chat.typing_effect("ERROR! Invalid credentials.", delay=0.1 / 1.5)
                case _:
                    Chat.typing_effect("Unknown command.", delay=0.1 / 1.5)

    @staticmethod
    def input_command():
        """ Get and process user input command """
        command = input("> ").lower().strip()
        return command

    @staticmethod
    def username():
        username = input(" ").lower().strip()
        return username

    def main(self):
        """ Main entry point for starting the app """
        Data.username = input("Insert your name: ").lower().strip()
        if Data.is_wife(Data.username):
            Chat.typing_effect(Data.welcoming_message, delay=0.1 / 1.5)
        Chat.typing_effect("Type Help for command list.", delay=0.1 / 1.5)
        self.interpreter()

if __name__ == "__main__":
    ui_instance = UI()
    ui_instance.main()
