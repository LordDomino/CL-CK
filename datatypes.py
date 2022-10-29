"""CL-CK datatypes and containers.
"""

from typing import Any
from dataclasses import dataclass
from dataclasses import field

__all__ = [
    "UnapplicableType",
    "GrammaticalAttribute",
    "Inventory",
    "Morpheme",
    "LexicalMorpheme",
    "FunctionalMorpheme",
    "DerivationalMorpheme",
    "InflectionalMorpheme",
    "Phoneme",
    "Glosseme",
    "LexicalGlosseme",
    "InventorialGlosseme",
    "Category",
    "Case",
    "Number",
    "Noun",
    "Verb",
    "Adjective",
    "Preposition",
    "Conjunction",
    "Interjection",
    "Termination",
    "Declension",
    "Word",
]

"""
________________________________________________________________________________
=== DATACLASS CONVENTIONS ======================================================

  All class decorated with the @dataclass decorator that are potential to
  containing default values in their parameters should always follow the
  formatting below:

    class _<Name of class>_Base
    Contains all the required arguments of the class

    class _<Name of class>_BaseDef
      Contains all the arguments of the class that fall back with a
      default value.

    class <Name of main class> (_<Name of class>_BaseDef, _<Name of class>_Base)
      Main class that inherits from the _Base and _BaseDef templates.
      Acts as the class itself.

"""


class UnapplicableType:...
@dataclass
class GrammaticalAttribute:
    str_val: str

@dataclass
class Inventory:
    """Class to attribute elements and weights. If :class:`weights` is left
    blank, each element in the list defaults with a weight of :class:`0`.
    """
    elements: list
    weights: list = field(default=None)
    category: Any = field(default=None)

    def __post_init__(self) -> None:
        self._dict: dict = {}

        if self.weights is None:
            self.weights = []
            for _ in self.elements:
                self.weights.append(1)
        if len(self.elements) == len(self._dict):
            for _e, _w in zip(self.elements, self.weights):
                self._dict[_e] = _w

    def __call__(self) -> list:
        return(self.elements)

    def get_elements(self) -> list:
        return(self.elements)

    def get_weights(self) -> list:
        return(self.weights)


@dataclass
class _Morpheme_Base:
    str_val: str

@dataclass
class _Morpheme_BaseDef:...

@dataclass
class Morpheme(_Morpheme_BaseDef, _Morpheme_Base):
    """Class to attribute morphological information in the form of string
    characters.
    
    - :class:`str_val` -- attributes morphological information.
    """


@dataclass
class _LexicalMorpheme_Base(_Morpheme_Base):...
@dataclass
class _LexicalMorpheme_BaseDef(_Morpheme_BaseDef):...
@dataclass
class LexicalMorpheme(_LexicalMorpheme_BaseDef, Morpheme, _LexicalMorpheme_Base):
    """A :class:`Morpheme`-type class that is intended for lexical usage.
    """


@dataclass
class _FunctionalMorpheme_Base(_Morpheme_Base):...
@dataclass
class _FunctionalMorpheme_BaseDef(_Morpheme_BaseDef):...
@dataclass
class FunctionalMorpheme(_FunctionalMorpheme_BaseDef, Morpheme, _FunctionalMorpheme_Base):
    """A :class:`Morpheme`-type class that is intended for functional usage.
    """


@dataclass
class _DerivationalMorpheme_Base(_Morpheme_Base):...
@dataclass
class _DerivationalMorpheme_BaseDef(_Morpheme_BaseDef):...
@dataclass
class DerivationalMorpheme(_DerivationalMorpheme_BaseDef, Morpheme, _DerivationalMorpheme_Base):
    """A :class:`Morpheme`-type class that is intended for derivational usage.
    """


@dataclass
class _InflectionalMorpheme_Base(_Morpheme_Base):...
@dataclass
class _InflectionalMorpheme_BaseDef(_Morpheme_BaseDef):...
@dataclass
class InflectionalMorpheme(_InflectionalMorpheme_BaseDef, Morpheme, _InflectionalMorpheme_Base):
    """A :class:`Morpheme`-type class that is intended for inflectional usage.
    """


@dataclass
class _Phoneme_Base:
    str_val: str

@dataclass
class _Phoneme_BaseDef:
    str_repr: str = field(default=None)

@dataclass
class Phoneme(_Phoneme_BaseDef, _Phoneme_Base):
    """Class to attribute phonemical and/or phonological information in the form
    of special string formats.

    Usage:
    - :class:`str_val` -- attributes phonemical and/or phonological information.
    - :class:`str_repr` -- string representation of the phoneme. If left
        :class:`None`, then it defaults to value :class:`str_val`.
    """

    def __post_init__(self) -> None:
        if self.str_repr is None:
            self.str_repr = self.str_val

    def _get_repr(self) -> str:
        return self.str_repr



@dataclass
class _Glosseme_Base:
    morpheme: Morpheme
    phoneme: Phoneme

@dataclass
class _Glosseme_BaseDef:...

@dataclass
class Glosseme(_Glosseme_BaseDef, _Glosseme_Base):
    """Class for attributing a :class:`Morpheme` instance and a :class:`Phoneme`
    instance as one unit.

    - :class:`morpheme` -- morpheme component of the glosseme.
    - :class:`phoneme` -- phoneme component of the glosseme.
    """


@dataclass
class _LexicalGlosseme_Base(_Glosseme_Base):...

@dataclass
class _LexicalGlosseme_BaseDef(_Glosseme_BaseDef):...

@dataclass
class LexicalGlosseme(_LexicalGlosseme_BaseDef, Glosseme, _LexicalGlosseme_Base):
    """A :class:`Glosseme`-type class that is intended for lexical usage.
    """


@dataclass
class _InventorialGlosseme_Base(_Glosseme_Base):...

@dataclass
class _InventorialGlosseme_BaseDef(_Glosseme_BaseDef):...

@dataclass
class InventorialGlosseme(_InventorialGlosseme_BaseDef, Glosseme, _InventorialGlosseme_Base):
    """A :class:`Glosseme`-type class that is intended for inventorial usage.
    """

class Category(GrammaticalAttribute):...
class Case(GrammaticalAttribute):...
class Number(GrammaticalAttribute):...



"""
Here are the defaults classes (representations of the parts of speech) 
inheriting from :Category: class to serve as category identifiers of instances
of the :Word: class.
"""

class Noun(Category):...
class Verb(Category):...
class Adjective(Category):...
class Adverb(Category):...
class Preposition(Category):...
class Conjunction(Category):...
class Interjection(Category):...


@dataclass
class Termination:
    termination_type: str
    str_val: str | Morpheme
    case: Case
    number: Number

    def __post_init__(self) -> None:
        self._morpheme: Morpheme

        if self.termination_type not in ("+", "-", "="):
            print("Termination type unknown!")
        if isinstance(self.str_val, str):
            self._morpheme = Morpheme(self.str_val)
        elif isinstance(self.str_val, Morpheme):
            self._morpheme = self.str_val

    def get_morpheme(self) -> Morpheme:
        return self._morpheme


@dataclass
class Declension:
    """Class that attributes inflection rules for declining a given set of
    words.
    
    - :class:`endings` -- determines which morpheme endings this rule applies
    to.
    - :class:`terminations` -- a list of word terminations for various case,
    gender, and grammatical number.
    """
    endings: Inventory
    terminations: list[Termination]


@dataclass
class Word:
    """Class to represent word instances.

    - :class:`str_val` -- the derived word itself, as a string representation.
    - :class:`category` -- identifies the part of speech of the word.
    - :class:`morphemelist` -- list of all morphemes that comprise the word; can
        be extracted as a string representation using :class:`.get_morphemes()`.
    - :class:`phonemelist` -- list of all phonemes that comprise the word; can
        be extracted as a string representation using :class:`.get_phonemes()`.
    - :class:`case` -- identifies the case of the word.
    - :class:`number` -- identifies the grammatical number of the word.
    - :class:`declensionlist` -- list of declensions that the word instance went
        through.
    """
    str_val: str
    category: Category
    morphemelist: list[Morpheme] | Inventory
    phonemelist: list[Phoneme] | Inventory
    case: Case
    number: Number
    declensionlist: list[Declension] | Inventory
    gender = ...
    tense = ...
    aspect = ...
    mood = ...
        
    def __post_init__(self) -> None:
        self._grammar_attribs = (
            self.case,
            self.number,
            self.gender,
            self.tense,
            self.aspect,
            self.mood,
        )
    
    def _filter_params(self) -> None:
        """Filters certain parameters and sets values to
        :class:`UnapplicableType` based on :class:`self.category`'s value.
        """

    def get_morphemes(self) -> list[Morpheme]:
        """Returns a tuple sequence of the word's morphemes.
        """

    def get_phonemes(self) -> list[Phoneme]:
        """Returns a tuple sequence of the word's phonemes.
        """


if __name__ == "__main__": ...