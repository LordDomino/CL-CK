from .component import Component
from .articulation import ArticulatoryProperty, Backness, Height, Manner, Roundedness, Voicing, Place



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


    def __init__(self, symbol: str,
            articulatory_properties: tuple[ArticulatoryProperty, ...]) -> None:
        """
        Creates an abstract phoneme representation.

        Parameters
        ----------
        - `symbol` is the character representation of the phoneme.
        - `articulatory_properties` is the tuple of articulatory properties of
            the phoneme.
        """
        self._symbol: str = symbol
        self._articulatory_properties: tuple[ArticulatoryProperty, ...] = (
            articulatory_properties)
        self._property_names: list[str] = self._get_property_names()


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
        return self._symbol
    

    def _create_transcript(self) -> str:
        return f"/{self._symbol}/"

    
    def _get_property_names(self) -> list[str]:
        return [property.name for property in self._articulatory_properties]



class Consonant(Phoneme):
    def __init__(self, symbol: str, place: Place, manner: Manner,
            *other_properties: ArticulatoryProperty) -> None:
        super().__init__(symbol, (place, manner, *other_properties))
        self._place: Place = place
        self._manner: Manner = manner



class Vowel(Phoneme):
    def __init__(self, symbol: str,
          backness: Backness,
          height: Height,
          roundedness: Roundedness) -> None:
        self._height: Height = height
        self._backness: Backness = backness
        self._roundedness: Roundedness = roundedness
        super().__init__(symbol, (height, backness, roundedness))



class PulmonicConsonant(Consonant):
    def __init__(self, symbol: str, place: Place, manner: Manner,
          voicing: Voicing) -> None:
        self._voicing: Voicing = voicing
        super().__init__(symbol, place, manner)



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