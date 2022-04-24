from    dataclasses import dataclass
from    enum        import Enum
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

    def small(self, kana):
        match kana:
            case KanaMode.HIRAGANA:         
                char = "HIRAGANA LETTER SMALL " + str(self.romaji.upper())
            case KanaMode.KATAKANA:
                char = "KATAKANA LETTER SMALL " + str(self.romaji.upper())
        return unicodedata.lookup(char)

@dataclass
class CurrentRound:
    score                      : int           = 0
    romaji_one                 : str           = ""
    romaji_two                 : str           = ""
    romaji_three               : str           = ""
    next_kana                  : str           = ""
    match                      : int           = 0
    fail                       : int           = 0
    correct_object             : Matchagana    = Matchagana("a")
    game_mode                  : str           = ""

class KanaMode(Enum):
    MATCHAGANA  = 0
    HIRAGANA    = 1
    KATAKANA    = 2
