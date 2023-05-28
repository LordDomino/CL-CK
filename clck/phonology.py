from dataclasses import dataclass
from typing import Literal



@dataclass
class IPA_Phoneme:
  string: str
  place: str
  manner: str



@dataclass
class IPA_Phoneme_PulmonicConsonant(IPA_Phoneme):
  string: str
  place: Literal[
    "bilabial",
    "labiodental",
    "linguolabial",
    "dental",
    "alveolar",
    "postalveolar",
    "retroflex",
    "palatal",
    "velar",
    "uvular",
    "epiglottal",
    "glottal",
  ]
  manner: Literal[
    "nasal",
    "plosive",
    "sibilant affricate",
    "nonsibilant affricate",
    "sibilant fricative",
    "nonsibilant fricative",
    "approximanrt",
    "tap",
    "trill",
    "lateral affricate",
    "lateral fricative",
    "lateral approximant",
    "lateral tap",
  ]
  voiced: bool



@dataclass
class IPA_Phoneme_NonpulmonicConsonant(IPA_Phoneme):
  string: str
  place: Literal[
    "bilabial",
    "labiodental",
    "linguolabial",
    "dental",
    "alveolar",
    "postalveolar",
    "retroflex",
    "palatal",
    "velar",
    "uvular",
    "epiglottal",
  ]
  manner: Literal[
    "ejective stop",
    "ejective affricate",
    "ejective fractive",
    "ejective lateral affricate",
    "ejective lateral fricative",
    "click tenuis",
    "click voiced",
    "click nasal",
    "click tenuis lateral",
    "click voiced lateral",
    "click nasal lateral",
    "implosive voiced",
    "implosive voiceless",
  ]



@dataclass
class IPA_Phoneme_Vowel(IPA_Phoneme):
  string: str
  place: Literal[
    "front",
    "central",
    "back",
  ]
  manner: Literal[
    "close",
    "nearclose",
    "closemid",
    "mid",
    "openmid",
    "nearopen",
    "open",
  ]
  rounded: bool



class PhonologicalInventory:
  def __init__(self, *phonemes: IPA_Phoneme) -> None:
    self._phonemes: tuple[IPA_Phoneme] = phonemes

  @property
  def phonemes(self) -> tuple[IPA_Phoneme]:
    return self._phonemes