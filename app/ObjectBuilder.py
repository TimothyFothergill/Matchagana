from models import Matchagana, KanaMode

class MatchaganaBuilder:
    object_list     = []
    hiragana_list   = []
    romaji_list     = []

    def __init__(self):
        clusters =["a", "i", "u", "e", "o", "ka", "ga", "ku", "gu",
                    "ke", "ge", "ko", "go", "sa", "za", "si", "zi",
                    "su", "zu", "se", "ze", "so", "zo", "ta", "da",
                    "ti", "di", "tu", "du", "te", "de", "to", "do",
                    "na", "ni", "nu", "ne", "no", "ha", "ba", "pa",
                    "hi", "bi", "pi", "hu", "bu", "pu", "he", "be",
                    "pe", "ho", "bo", "po", "ma", "mi", "mu", "me",
                    "mo", "ya", "yu", "yo", "ra", "ri", "ru", "re",
                    "ro", "wa", "wo", "n"]
        for c in clusters:
            self.object_list.append(Matchagana(c))
        self.hiragana_list  += (x.hiragana for x in self.object_list)
        self.romaji_list    += (x.romaji for x in self.object_list)

    def get_matchagana(self, romaji):
        character = next((
            x for x in self.object_list if x == Matchagana(romaji)),
            None)
        return character

    def get_matchagana_multiples(self, romaji):
        word = []
        for r in romaji:
            word += next((
                x for x in self.object_list if x == Matchagana(r) ), 
                None)
        return word

    def get_hiragana(self, romaji):
        character = next((
            x for x in self.object_list if x == Matchagana(romaji) ),
            None)
        return character.hiragana
    
    def get_hiragana_list(self):
        return self.hiragana_list

    def get_hiragana_multiples(self, romaji):
        word = ""
        for r in romaji:
            word += next((
                x for x in self.object_list if x == Matchagana(r) ),
                None).hiragana
        return word

    def get_romaji_list(self):
        return self.romaji_list

    def get_matchagana_list(self):
        return self.object_list

    def get_kana(self, romaji, type = 0):
        character = next((
        x for x in self.object_list if x == Matchagana(romaji) ),
        None)
        match type:
            case KanaMode.HIRAGANA:
                    return character.hiragana
            case KanaMode.KATAKANA:
                    return character.katakana
            case _:
                return character

    def get_kana_multiples(self, romaji, type = 0):
        word = ""
        for r in romaji:
            match type:
                case KanaMode.HIRAGANA:
                    word += next((
                        x for x in self.object_list if x == Matchagana(r) ),
                        None).hiragana
                case KanaMode.KATAKANA:
                    word += next((
                        x for x in self.object_list if x == Matchagana(r) ),
                        None).katakana
                case 0:
                    word += next((
                        x for x in self.object_list if x == Matchagana(r) ),
                        None)
        return word
