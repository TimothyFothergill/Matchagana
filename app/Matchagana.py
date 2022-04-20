import os

from dotenv import load_dotenv
from flask  import Flask, render_template, request, redirect, flash, jsonify, url_for

from models import Matchagana, CurrentRound
from ObjectBuilder import MatchaganaBuilder

import GameLogic

load_dotenv()
app                 = Flask(__name__)
app.secret_key      = os.getenv('APP_SECRET_KEY')
matcha_search       = MatchaganaBuilder()
curr_round          = CurrentRound()

@app.route("/api/matchagana", methods=["GET"])
def matchagana_api():
    return jsonify(matcha_search.get_matchagana_list())

@app.route("/api/matchagana/<romaji>", methods=["GET"])
def matchagana_by_romaji_api(romaji):
    return jsonify(matcha_search.get_matchagana(romaji))

@app.route("/", methods=["GET", "POST"])
def index():
    hiragana_character  = matcha_search.get_hiragana_multiples(["ma", "ti"]) +\
                          matcha_search.get_matchagana("ya").small() +\
                          matcha_search.get_hiragana_multiples(["ga", "na"])
    return render_template("index.html", hiragana_character=hiragana_character)

@app.route("/about", methods=["GET"])
def about_page():
    return render_template("about.html")

@app.route("/start")
def new_game():
    curr_round.score    = 0
    curr_round.rounds   = 10
    loader()
    return redirect("/game")

@app.route("/game")
def loader():
    returned_objects = GameLogic.start_game(curr_round.rounds, curr_round.score, curr_round)
    if returned_objects == None:
        end_game()
        return redirect(url_for("end_game"))
    else:
        next_hiragana   = returned_objects[0]
        romaji_one      = returned_objects[1]
        romaji_two      = returned_objects[2]
        romaji_three    = returned_objects[3]
    return render_template("start.html", next_hiragana=next_hiragana, romaji_one=romaji_one, romaji_two=romaji_two,
                            romaji_three=romaji_three, score=curr_round.score)

@app.route("/game", methods=["POST"])
def await_player():
    outcome = request.form.get('button')
    if outcome == curr_round.correct_hiragana_object.romaji:
        curr_round.score += 100
        flash("Correct! +100 points.")
        if curr_round.rounds > 0:
            curr_round.rounds -= 1
            return loader()
        else:
            end_game()
            return redirect(url_for("end_game"))
    else:
        curr_round.score -= 50
        flash("Incorrect! -50 points.")
        if curr_round.rounds > 0:
            curr_round.rounds -= 1
            return loader()
        else:
            end_game()
            return redirect(url_for("end_game"))

@app.route("/arigatou", methods=["GET", "POST"])
def end_game():
    return render_template("arigatou.html", score=curr_round.score)

@app.route("/finished", methods=["GET", "POST"])
def score_submitted():
    if request.method == "POST":
        print("Yo dummy")
    return index()

@app.route("/hiraganachar", methods=["GET"])
def hiragana_char_page():
    return render_template("hiragana.html", hiragana_list=matcha_search.get_hiragana_list())

@app.route("/updates", methods=["GET"])
def updates():
    return render_template("updates.html")

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
