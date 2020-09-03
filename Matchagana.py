import unicodedata
import random
import pymongo
from datetime import datetime

from flask import Flask, render_template, request, redirect, flash
app = Flask(__name__)
app.secret_key = "IbXd)K=gWm/6TAc"

client = pymongo.MongoClient(host="matchagana-db", port=27017)
db = client["Matchagana-Scores"]
col = db["Hi-Scores"]

now = datetime.now()
current_time = now.strftime("%d/%m/%Y %H:%M:%S")


@app.route("/api/hiragana", methods=["GET"])
def api_hiragana():
    return {
        "hiragana": {
            "Hiragana": hiragana_list,
            "Romaji": romaji_list
            }
    }


class GameLoop:

    @app.route("/start")
    def loader():
        score = curr_round.score
        match = curr_round.match
        fail = curr_round.fail
        limit = curr_round.rounds
        returned_objects = GameLoop.start_game(GameLoop(), limit, score, match, fail)
        print("RETURNED OBJECTS: " + str(returned_objects))
        if str(returned_objects) == "None":
            return GameLoop.end_game(GameLoop(), curr_round.score)
        else:
            next_hiragana = returned_objects[0]
            romaji_one = returned_objects[1]
            romaji_two = returned_objects[2]
            romaji_three = returned_objects[3]
        return render_template("start.html", next_hiragana=next_hiragana, romaji_one=romaji_one, romaji_two=romaji_two,
                               romaji_three=romaji_three, score=score)

    def start_game(self, limit, score, match, fail):
        print("RUNNING START_GAME")
        while limit > 0:
            returned_objects = GameLoop.game_logic(self, score, match, fail)
            return returned_objects
        print("Your total score was: " + str(score))

    @staticmethod
    @app.route("/arigatou", methods=["GET", "POST"])
    def end_game(self, score):
        print("RUNNING END_GAME")
        score = curr_round.score
        curr_round.score = 0
        curr_round.rounds = 10
        if request.method == "POST":
            p_name = request.form.get("leaderboard")
            GameLoop.player_submit_score(self, p_name, score, "Hiragana")
            return render_template("score-submitted.html")
        return render_template("arigatou.html", score=score)

    @app.route("/score-submitted")
    def player_submit_score(self, p_name, p_score, game_type):
        col.insert_one({"player_name": p_name, "score": p_score, "game_type": game_type, "date/time: ": current_time})
        print("Player score submitted to DB")
        return 1

    def game_logic(self, score, match, fail):
        print("RUNNING GAME_LOGIC")
        print("The next Hiragana to match is...")
        object_length = len(object_list)

        random_int = random.randint(0, object_length) - 1
        random_int_2 = random.randint(0, object_length) - 1
        random_int_3 = random.randint(0, object_length) - 1

        correct_hiragana_object = object_list[random_int]
        next_hiragana = correct_hiragana_object.hiragana
        print(str(next_hiragana))
        print("Which of these is the matching Romaji?")

        # TODO: Fix. This catches if there's a duplicate romaji and re-rolls. If it fails, it goes to 3rd slot.
        loopcatcher = 1
        while loopcatcher == 1:
            while random_int_2 == random_int or random_int_2 == random_int_3:
                random_int_2 = random.randint(0, object_length) - 1
            while random_int_3 == random_int:
                random_int_3 = random.randint(0, object_length) - 1
            while random_int_3 == random_int_2:
                random_int_3 = random.randint(0, object_length) - 1
            if random_int_3 == random_int_2 or random_int_3 == random_int:
                loopcatcher = 1
            elif random_int_2 == random_int or random_int_2 == random_int_3:
                loopcatcher = 1
            else:
                loopcatcher = 0

        selectable = [correct_hiragana_object, object_list[random_int_2], object_list[random_int_3], object_list[0]]
        chosen_data = random.sample(selectable, k=3)

        romaji_one = chosen_data[0].romaji
        romaji_two = chosen_data[1].romaji
        romaji_three = chosen_data[2].romaji

        if romaji_one != correct_hiragana_object.romaji and romaji_two != correct_hiragana_object.romaji \
                and romaji_three != correct_hiragana_object.romaji:
            romaji_three = correct_hiragana_object.romaji

        # END TODO

        print(romaji_one + " " + romaji_two + " " + romaji_three)

        GameLoop.game_data(self, next_hiragana, romaji_one, romaji_two, romaji_three, score, match, fail, chosen_data,
                           correct_hiragana_object)
        return next_hiragana, romaji_one, romaji_two, romaji_three

    @staticmethod
    def game_data(self, next_hiragana, romaji_one, romaji_two, romaji_three, score, match, fail, chosen_data,
                  correct_hiragana_object):
        print("RUNNING GAME_DATA")
        next_hiragana = next_hiragana

        romaji_one = romaji_one
        romaji_two = romaji_two
        romaji_three = romaji_three
        score = score
        match = match
        fail = fail

        curr_round.score = score
        curr_round.next_hiragana = next_hiragana
        curr_round.romaji_one = romaji_one
        curr_round.romaji_two = romaji_two
        curr_round.romaji_three = romaji_three
        curr_round.match = match
        curr_round.fail = fail
        curr_round.correct_hiragana_object = correct_hiragana_object

        print("Player current score is: " + str(score))
        print("Next Hiragana = " + next_hiragana)
        print("Romaji_one = " + romaji_one)
        print("Romaji_two = " + romaji_two)
        print("Romaji_three = " + romaji_three)
        return next_hiragana, romaji_one, romaji_two, romaji_three

    @staticmethod
    @app.route("/start", methods=["GET", "POST"])
    def await_player():
        print("RUNNING AWAIT_PLAYER")
        if request.method == "POST":
            outcome = request.form.get('button')
            print(outcome)
            print(curr_round.correct_hiragana_object.romaji)
            print(str(curr_round.correct_hiragana_object.romaji))
            if outcome == curr_round.correct_hiragana_object.romaji:
                curr_round.score += 100
                print("Your score is: " + str(curr_round.score))
                flash("Correct! +100 points.")
                if curr_round.rounds > 0:
                    curr_round.rounds -= 1
                    return GameLoop.loader()
                else:
                    return GameLoop.end_game(GameLoop(), curr_round.score)
            else:
                print("Fail")
                curr_round.score -= 50
                print("Your score is: " + str(curr_round.score))
                flash("Incorrect! -50 points.")
                if curr_round.rounds > 0:
                    curr_round.rounds -= 1
                    return GameLoop.loader()
                else:
                    return GameLoop.end_game(GameLoop(), curr_round.score)


class CurrentRound:
    # CurrentRound class contains data about the current round as well as other bits of useful info.
    def __init__(self, score, romaji_one, romaji_two, romaji_three, next_hiragana, match, fail, correct_hiragana_object,
                 rounds):
        self.score = score
        self.romaji_one = romaji_one
        self.romaji_two = romaji_two
        self.romaji_three = romaji_three
        self.next_hiragana = next_hiragana
        self.match = match
        self.fail = fail
        self.correct_hiragana_object = correct_hiragana_object
        self.rounds = rounds


class Hiragana:
    # Hiragana class, contains romaji and hiragana
    def __init__(self, romaji):
        if romaji == "ti":
            self.romaji = "ti/chi"
        elif romaji == "si":
            self.romaji = "si/shi"
        else:
            self.romaji = romaji
        self.hiragana = unicodedata.lookup("HIRAGANA LETTER " + str(romaji).upper())


@app.route("/", methods=["GET", "POST"])
def on_start():
    print("RUNNING ON_START")
    if request.method == "POST":
        curr_round.score = 0
        curr_round.rounds = 10
        GameLoop.loader()
        return redirect("/start")
    print("Started... Awaiting User Response.")
    hiragana_character = ""
    hiragana_character += ma.hiragana
    hiragana_character += ti.hiragana
    hiragana_character += unicodedata.lookup("HIRAGANA LETTER SMALL YA")
    hiragana_character += ga.hiragana
    hiragana_character += na.hiragana
    return render_template("index.html", hiragana_character=hiragana_character)


# Game state setup and extras.
curr_round = CurrentRound(0, "", "", "", "", 0, 0, Hiragana("a"), 10)

hiragana_list = []
romaji_list = []
object_list = []

a = Hiragana("a")
i = Hiragana("i")
u = Hiragana("u")
e = Hiragana("e")
o = Hiragana("o")
ka = Hiragana("ka")
ga = Hiragana("ga")
ku = Hiragana("ku")
gu = Hiragana("gu")
ke = Hiragana("ke")
ge = Hiragana("ge")
ko = Hiragana("ko")
go = Hiragana("go")
sa = Hiragana("sa")
za = Hiragana("za")
si = Hiragana("si")
zi = Hiragana("zi")
su = Hiragana("su")
zu = Hiragana("zu")
se = Hiragana("se")
ze = Hiragana("ze")
so = Hiragana("so")
zo = Hiragana("zo")
ta = Hiragana("ta")
da = Hiragana("da")
ti = Hiragana("ti")
di = Hiragana("di")
tu = Hiragana("tu")
du = Hiragana("du")
te = Hiragana("te")
de = Hiragana("de")
to = Hiragana("to")
do = Hiragana("do")
na = Hiragana("na")
ni = Hiragana("ni")
nu = Hiragana("nu")
ne = Hiragana("ne")
no = Hiragana("no")
ha = Hiragana("ha")
ba = Hiragana("ba")
pa = Hiragana("pa")
hi = Hiragana("hi")
bi = Hiragana("bi")
pi = Hiragana("pi")
hu = Hiragana("hu")
bu = Hiragana("bu")
pu = Hiragana("pu")
he = Hiragana("he")
be = Hiragana("be")
pe = Hiragana("pe")
ho = Hiragana("ho")
bo = Hiragana("bo")
po = Hiragana("po")
ma = Hiragana("ma")
mi = Hiragana("mi")
mu = Hiragana("mu")
me = Hiragana("me")
mo = Hiragana("mo")
ya = Hiragana("ya")
yu = Hiragana("yu")
yo = Hiragana("yo")
ra = Hiragana("ra")
ri = Hiragana("ri")
ru = Hiragana("ru")
re = Hiragana("re")
ro = Hiragana("ro")
wa = Hiragana("wa")
wi = Hiragana("wi")
we = Hiragana("we")
wo = Hiragana("wo")
n = Hiragana("n")
vu = Hiragana("vu")

ohayo = ""
ohayo += Hiragana("o").hiragana
ohayo += Hiragana("Ha").hiragana
ohayo += Hiragana("Yo").hiragana

print("OHAYO! ( " + ohayo + " )")
print("Welcome to Matchagana, the browser-based Hiragana to Romaji matching game.")

object_list += [a, i, u, e, o, ka, ga, ku, gu,
                ke, ge, ko, go, sa, za, si, zi,
                su, zu, se, ze, so, zo, ta, da,
                ti, di, tu, du, te, de, to, do,
                na, ni, nu, ne, no, ha, ba, pa,
                hi, bi, pi, hu, bu, pu, he, be,
                pe, ho, bo, po, ma, mi, mu, me,
                mo, ya, yu, yo, ra, ri, ru, re,
                ro, wa, wi, we, wo, n, vu]

for ele in object_list:
    romaji_list.append(ele.romaji)
    hiragana_list += ele.hiragana

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
