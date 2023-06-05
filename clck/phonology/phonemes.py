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

class Phone:
    def __init__(self, symbol: str) -> None:
        self._symbol: str = symbol


    def __call__(self) -> str:
        return self._symbol


    @property
    def symbol(self) -> str:
        return self._symbol



class Phoneme(Phone):


    def __init__(self, symbol: str,
          articulatory_properties: tuple[ArticulatoryProperty, ...]) -> None:
        super().__init__(symbol)
        self._articulatory_properties: tuple[ArticulatoryProperty, ...] = (
            articulatory_properties)
        self._name: str = self._create_name()
        self._transcript: str = f"/{self._symbol}/"


    def __str__(self) -> str:
        return f"{self.__class__.__name__} phoneme \"{self._symbol}\""


    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} {self._symbol}>"


    @property
    def name(self) -> str:
        return self._name

    
    @property
    def transcript(self) -> str:
        return self._transcript


    def _create_name(self) -> str:
        articulatory_properties: list[str] = []
        for articulatory_property in self._articulatory_properties:
            articulatory_properties.append(articulatory_property.name)
        return f"{self._symbol} ({' '.join(articulatory_properties)})"



class Consonant(Phoneme):
    def __init__(self, symbol: str,
              place: Place, manner: Manner) -> None:
        self._place: Place = place
        self._manner: Manner = manner
        super().__init__(symbol, (place, manner))



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