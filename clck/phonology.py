from dataclasses import dataclass
from typing import Literal



class IPA_Phoneme:
  def __init__(self, string: str, place: str, manner: str) -> None:
    self._string: str = string
    self._place: str = place
    self._manner: str = manner

  def __str__(self) -> str:
    return self._string

  def __repr__(self) -> str:
    return f"<Phoneme {self._string}>"



class IPA_Phoneme_PulmonicConsonant(IPA_Phoneme):
  def __init__(
      self,
      string: str,
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
      ],
      manner: Literal[
        "nasal",
        "plosive",
        "sibilant affricate",
        "nonsibilant affricate",
        "sibilant fricative",
        "nonsibilant fricative",
        "approximant",
        "tap",
        "trill",
        "lateral affricate",
        "lateral fricative",
        "lateral approximant",
        "lateral tap",
      ],
      voiced: bool
  ) -> None:
    super().__init__(string, place, manner)
    self._voiced: bool = voiced



class IPA_Phoneme_NonpulmonicConsonant(IPA_Phoneme):
  def __init__(
      self,
      string: str,
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
      ],
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
  ) -> None:
    super().__init__(string, place, manner)



@dataclass
class IPA_Phoneme_Vowel(IPA_Phoneme):
  def __init__(
      self,
      string: str,
      place: Literal[
        "front",
        "central",
        "back",
      ],
      manner: Literal[
        "close",
        "nearclose",
        "closemid",
        "mid",
        "openmid",
        "nearopen",
        "open",
      ],
      rounded: bool | None
  ) -> None:
    super().__init__(string, place, manner)



class PhonologicalInventory:
  def __init__(self, *phonemes: IPA_Phoneme) -> None:
    self._phonemes: tuple[IPA_Phoneme] = phonemes

  @property
  def phonemes(self) -> tuple[IPA_Phoneme]:
    return self._phonemes