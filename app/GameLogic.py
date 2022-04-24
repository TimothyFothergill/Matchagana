import random
from ObjectBuilder import MatchaganaBuilder

matcha_search = MatchaganaBuilder()

def start_game(rounds, score, curr_round):
    while rounds > 0:
        returned_objects = game_logic(score, curr_round)
        return returned_objects
    return None

def game_logic(score, curr_round):
    object_length               = len(matcha_search.get_matchagana_list()) - 1
    random_int                  = random.randint(0, object_length)
    correct_object              = matcha_search.get_matchagana_list()[random_int]
    incorrect_matchagana        = matcha_search.get_matchagana_list()[random.randint(0, object_length)]
    incorrect_matchagana_2      = matcha_search.get_matchagana_list()[random.randint(0, object_length)]

    while(correct_object        == incorrect_matchagana):
        incorrect_matchagana    = matcha_search.get_matchagana_list()[random.randint(0, object_length)]
    while(correct_object        == incorrect_matchagana_2):
        incorrect_matchagana_2  = matcha_search.get_matchagana_list()[random.randint(0, object_length)]
    while(incorrect_matchagana  == incorrect_matchagana_2):
        incorrect_matchagana_2  = matcha_search.get_matchagana_list()[random.randint(0, object_length)]

    selectable = [
        correct_object, 
        incorrect_matchagana, 
        incorrect_matchagana_2
    ]
    chosen_data = random.sample(selectable, k=3)

    romaji_one   = chosen_data[0].romaji
    romaji_two   = chosen_data[1].romaji
    romaji_three = chosen_data[2].romaji

    match curr_round.game_mode:
        case "hiragana": 
            game_data(correct_object.hiragana, romaji_one, romaji_two, romaji_three, score,
                correct_object, curr_round)
            return correct_object.hiragana, romaji_one, romaji_two, romaji_three
        case "katakana":
            game_data(correct_object.katakana, romaji_one, romaji_two, romaji_three, score,
                correct_object, curr_round)
            return correct_object.katakana, romaji_one, romaji_two, romaji_three
        case _:             
            game_data(correct_object.hiragana, romaji_one, romaji_two, romaji_three, score,
                correct_object, curr_round)
            return correct_object.hiragana, romaji_one, romaji_two, romaji_three

def game_data(next_hiragana, romaji_one, romaji_two, romaji_three, score,
                correct_hiragana_object, curr_round):
    curr_round.correct_hiragana_object = correct_hiragana_object
    print("Player current score is: " + str(score))
    print("Next Hiragana = " + next_hiragana)
    print("Romaji_one = " + romaji_one)
    print("Romaji_two = " + romaji_two)
    print("Romaji_three = " + romaji_three)
    return next_hiragana, romaji_one, romaji_two, romaji_three
