from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import random, json, time, nltk
from main import Chat, Data

app = Flask(__name__)
app.secret_key = "770f1df81082fdc7a07dade67fd993f1f8216027f2eb40489c06b6171753e4d7"

DATABASE_PATH = "dataset/Database/personal database.json"

# ------------------- CHAT ENDPOINTS -------------------

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["GET", "POST"])
def chat():
    if request.method == "POST":
        user_input = request.form.get("message")
        response = get_chat_response(user_input, DATABASE_PATH)
        return jsonify({"response": response})
    return render_template("chat.html")

def get_chat_response(user_input, file_path):
    # Capture the output from Chat.get_ai_response by overriding its typing_effect
    output_lines = []
    def capture_typing_effect(text, delay=0.0):
        output_lines.append(text)
    original_typing_effect = Chat.typing_effect
    Chat.typing_effect = capture_typing_effect
    try:
        Chat.get_ai_response(user_input, file_path)
    except Exception as e:
        output_lines.append("Error: " + str(e))
    finally:
        Chat.typing_effect = original_typing_effect
    return "\n".join(output_lines)

# ------------------- DAILY QUOTE -------------------

@app.route("/daily-quote")
def daily_quote():
    username = session.get("username", "")
    if Data.is_wife(username):
        quote = random.choice(Data.quotes)
        return render_template("daily_quote.html", quote=quote)
    else:
        return "ERROR! Invalid credentials."

# ------------------- GAMES -------------------

@app.route("/games")
def games():
    return render_template("games.html")

# --- Rock-Paper-Scissors ---
@app.route("/games/rps", methods=["GET", "POST"])
def rps():
    if request.method == "POST":
        user_move = request.form.get("move").strip().lower()
        if user_move not in ["rock", "paper", "scissors"]:
            return jsonify({"error": "Invalid move."})
        ai_move = random.choice(["rock", "paper", "scissors"])
        if user_move == ai_move:
            result = "tie"
        elif (user_move == "rock" and ai_move == "scissors") or \
             (user_move == "paper" and ai_move == "rock") or \
             (user_move == "scissors" and ai_move == "paper"):
            result = "win"
        else:
            result = "lose"
        return jsonify({"user_move": user_move, "ai_move": ai_move, "result": result})
    return render_template("rps.html")

# --- High-Low Game (User guesses a number chosen by the AI) ---
@app.route("/games/hilo", methods=["GET", "POST"])
def hilo():
    if request.method == "POST":
        if "start" in request.form:
            lo = int(request.form.get("lo"))
            hi = int(request.form.get("hi"))
            secret = random.randint(lo, hi)
            session["hilo_secret"] = secret
            session["hilo_attempts"] = 0
            return redirect(url_for("hilo"))
        elif "guess" in request.form:
            guess = int(request.form.get("guess"))
            secret = session.get("hilo_secret")
            session["hilo_attempts"] += 1
            attempts = session["hilo_attempts"]
            if guess == secret:
                message = f"Correct! You guessed the number in {attempts} attempts."
                session.pop("hilo_secret", None)
                session.pop("hilo_attempts", None)
                return render_template("hilo_result.html", message=message)
            elif guess < secret:
                message = "Too low!"
            else:
                message = "Too high!"
            return render_template("hilo_game.html", message=message)
    # GET: If no game in session, show start form
    if "hilo_secret" not in session:
        return render_template("hilo_start.html")
    else:
        return render_template("hilo_game.html", message="Make a guess!")

# --- Hangman Game ---
@app.route("/games/hangman", methods=["GET", "POST"])
def hangman():
    if request.method == "POST":
        if "start" in request.form:
            with open("dataset/English Dictionary/words.txt", "r", encoding="utf-8") as f:
                words = [line.strip() for line in f if line.strip()]
            secret = random.choice(words)
            session["hangman_secret"] = secret
            session["hangman_visible"] = ["_"] * len(secret)
            session["hangman_attempts"] = 0
            session["hangman_guessed"] = []
            return redirect(url_for("hangman"))
        elif "letter" in request.form:
            letter = request.form.get("letter").lower()
            secret = session.get("hangman_secret")
            visible = session.get("hangman_visible")
            guessed = session.get("hangman_guessed")
            if letter in guessed:
                message = f"You already guessed {letter}!"
            else:
                guessed.append(letter)
                if letter in secret:
                    for i, ch in enumerate(secret):
                        if ch == letter:
                            visible[i] = letter
                    message = f"Good guess: {letter} is in the word."
                else:
                    session["hangman_attempts"] += 1
                    message = f"Wrong guess: {letter} is not in the word."
                session["hangman_visible"] = visible
                session["hangman_guessed"] = guessed
            if "".join(visible) == secret:
                message = f"Congratulations! You guessed the word: {secret}"
                session.pop("hangman_secret", None)
                session.pop("hangman_visible", None)
                session.pop("hangman_attempts", None)
                session.pop("hangman_guessed", None)
                return render_template("hangman_result.html", message=message)
            return render_template("hangman_game.html", message=message, visible=" ".join(visible))
    if "hangman_secret" not in session:
        return render_template("hangman_start.html")
    else:
        visible = session.get("hangman_visible")
        return render_template("hangman_game.html", message="Guess a letter!", visible=" ".join(visible))

# --- Love Quiz ---
@app.route("/games/lovequiz", methods=["GET", "POST"])
def lovequiz():
    quiz = Data.quiz_game
    if request.method == "POST":
        question = request.form.get("question")
        selected = request.form.get("answer")
        correct = quiz[question]["answer"]
        if selected == correct:
            result = "Correct!"
        else:
            result = f"Incorrect. The correct answer was {correct}."
        return render_template("lovequiz_result.html", result=result)
    else:
        question = random.choice(list(quiz.keys()))
        options = quiz[question]["options"]
        return render_template("lovequiz.html", question=question, options=options)

# ------------------- USER NAME -------------------
@app.route("/set-username", methods=["POST"])
def set_username():
    username = request.form.get("username").strip().lower()
    session["username"] = username
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
