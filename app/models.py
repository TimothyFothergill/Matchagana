from    dataclasses import dataclass
import  unicodedata

@dataclass
class Matchagana:
    romaji      : str
    hiragana    : str
    katakana    : str

    def __init__(self, romaji):
        self.romaji     = romaji
        self.hiragana   = unicodedata.lookup("HIRAGANA LETTER " + 
                            str(romaji).upper()
                        )
        self.katakana   = unicodedata.lookup("KATAKANA LETTER " + 
                            str(romaji).upper()
                        )

    def small(self):
        char = "HIRAGANA LETTER SMALL " + str(self.romaji.upper())
        return unicodedata.lookup(char)

@dataclass
class CurrentRound:
    score                               : int           = 0
    romaji_one                          : str           = ""
    romaji_two                          : str           = ""
    romaji_three                        : str           = ""
    next_hiragana                       : str           = ""
    match                               : int           = 0
    fail                                : int           = 0
    correct_hiragana_object             : Matchagana    = Matchagana("a")
