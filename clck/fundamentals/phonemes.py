from clck.phonology.articulation import ArticulatoryProperty
from clck.fundamentals.component import Component
from ..phonology.articulation import Backness, Height, Manner, Roundedness, Voicing, Place



__all__: list[str] = [
    "Phoneme",
    "Consonant",
    "Vowel",
    "PulmonicConsonant",
    "NonpulmonicConsonant",
    "EjectiveConsonant",
    "ImplosiveConsonant",
    "ClickConsonant",
]


class Phoneme(Component):

    DEFAULT_IPA_PHONEMES: tuple["Phoneme", ...] = ()

    def __init__(self, symbol: str,
            articulatory_properties: tuple[ArticulatoryProperty, ...],
            _default: bool = False) -> None:
        """
        Creates an abstract phoneme representation.
        Parameters
        ----------
        - `symbol` - the character representation of the phoneme.
        - `articulatory_properties` is the tuple of articulatory properties of
            the phoneme.
        """
        self._is_default: bool = _default
        self._symbol: str = symbol
        self._articulatory_properties: tuple[ArticulatoryProperty, ...] = (
            articulatory_properties)
        self._property_names: list[str] = self._get_property_names()

        super().__init__()  # only then call the super constructor to initialize the transcript and output

        if self.is_default_IPA_phoneme():
            Phoneme._append_to_defaults(self)


    def __call__(self) -> str:
        return self._symbol

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} {self._symbol}>"

    def __str__(self) -> str:
        s: list[str] = []
        for property in self._articulatory_properties:
            s.append(property.name)
        return f"{self.__class__.__name__} /{self._symbol}/ ({' '.join(s)})"

    @property
    def name(self) -> str:
        """The name of this phoneme."""
        return self.__str__()

    @property
    def symbol(self) -> str:
        """The assigned Unicode character for this phoneme."""
        return self._symbol

    def is_default_IPA_phoneme(self) -> bool:
        """
        Returns `True` if this phoneme is an official IPA phoneme, otherwise
        returns 
        `False`.
        """
        return self._is_default

    def _create_output(self) -> str:
        return self._symbol

    def _create_transcript(self) -> str:
        return f"/{self._symbol}/"

    def _get_property_names(self) -> list[str]:
        return [property.name for property in self._articulatory_properties]

    @classmethod
    def _append_to_defaults(cls, phoneme: "Phoneme") -> None:
        Phoneme.DEFAULT_IPA_PHONEMES = tuple([*Phoneme.DEFAULT_IPA_PHONEMES,
                                              phoneme])



class Consonant(Phoneme):
    def __init__(self, symbol: str, place: Place, manner: Manner,
            _deafult: bool = False) -> None:
        super().__init__(symbol, (place, manner), _deafult)
        self._place: Place = place
        self._manner: Manner = manner



class Vowel(Phoneme):
    def __init__(self, symbol: str, backness: Backness, height: Height,
            roundedness: Roundedness, _default: bool = False) -> None:
        super().__init__(symbol, (height, backness, roundedness), _default)
        self._height: Height = height
        self._backness: Backness = backness
        self._roundedness: Roundedness = roundedness



class PulmonicConsonant(Consonant):
    def __init__(self, symbol: str, place: Place, manner: Manner,
            voicing: Voicing, _deafult: bool = False) -> None:
        self._voicing: Voicing = voicing
        super().__init__(symbol, place, manner, _deafult)



class NonpulmonicConsonant(Consonant):
    def __init__(self, symbol: str, place: Place, manner: Manner) -> None:
        super().__init__(symbol, place, manner)



class EjectiveConsonant(NonpulmonicConsonant):
    def __init__(self, symbol: str, place: Place, manner: Manner) -> None:
        super().__init__(symbol, place, manner)



class ImplosiveConsonant(NonpulmonicConsonant):
    def __init__(self, symbol: str, place: Place, manner: Manner) -> None:
        super().__init__(symbol, place, manner)



class ClickConsonant(NonpulmonicConsonant):
    def __init__(self, symbol: str, place: Place, manner: Manner) -> None:
        super().__init__(symbol, place, manner)



class DummyPhoneme(Phoneme):
    def __init__(self) -> None:
        super().__init__("", ())