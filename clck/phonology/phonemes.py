from abc import abstractmethod
from typing import Literal



class Phoneme:
  def __init__(self, string: str, place: str, manner: str) -> None:
    self._string: str = string
    self._place: str = place
    self._manner: str = manner


  def __str__(self) -> str:
    return f"/{self._string}/"


  def __repr__(self) -> str:
    return f"<Phoneme \033[1m{self._string}\033[0m>"
  

  @abstractmethod
  def get_name(self) -> str:
    pass



class Consonant(Phoneme):
  def __init__(self, string: str, place: str, manner: str) -> None:
    super().__init__(string, place, manner)



class IPA_Phoneme_PulmonicConsonant(Consonant):
  def __init__(
      self,
      string: str,
      place: Literal[
        "bilabial",
        "labiodental",
        "dental",
        "alveolar",
        "postalveolar",
        "retroflex",
        "palatal",
        "velar",
        "uvular",
        "pharyngeal",
        "glottal",
      ],
      manner: Literal[
        "nasal",
        "plosive",
        "fricative",
        "approximant",
        "tap/flap",
        "trill",
        "lateral fricative",
        "lateral approximant",
      ],
      voiced: bool
  ) -> None:
    super().__init__(string, place, manner)
    self._voiced: bool = voiced


  def get_name(self) -> str:
    if self._voiced:
      return f"voiced {self._place} {self._manner}"
    else:
      return f"voiceless {self._place} {self._manner}"



class NonpulmonicConsonant(Consonant):
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



class Vowel(Phoneme):
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
    self._rounded: bool | None = rounded


  def get_name(self) -> str:
    if self._rounded is None:
      return f"{self._place} {self._manner}"
    elif self._rounded is True:
      return f"rounded {self._place} {self._manner}"
    else:
      return f"unrounded {self._place} {self._manner}"



class PhonologicalInventory:
  def __init__(self, *phonemes: Phoneme) -> None:
    self._phonemes: tuple[Phoneme] = phonemes
    self._consonants: tuple[Consonant] = self._get_consonants()
    self._vowels: tuple[Vowel] = self._get_vowels()


  @property
  def phonemes(self) -> tuple[Phoneme]:
    return self._phonemes
  

  @property
  def consonants(self) -> tuple[Consonant]:
    return self._consonants


  @property
  def vowels(self) -> tuple[Vowel]:
    return self._vowels
  

  def _get_consonants(self) -> tuple[Consonant]:
    consonants: list[Consonant] = []
    for phoneme in self._phonemes:
      if isinstance(phoneme, Consonant):
        consonants.append(phoneme)
    return tuple(consonants)
  

  def _get_vowels(self) -> tuple[Vowel]:
    vowels: list[Vowel] = []
    for phoneme in self._phonemes:
      if isinstance(phoneme, Vowel):
        vowels.append(phoneme)
    return tuple(vowels)