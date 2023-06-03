from abc import ABC, abstractmethod
from typing import Any


class ArticulatoryProperty(ABC):

    _id = 1

    def __init__(self, name: str) -> None:
        self._name: str = name
        self._id: int = self.__class__._id
        self.__class__._increment_class_incrementals()

    def __str__(self) -> str:
        return f"{self.__class__.__name__} of articulation (ID_{self._id}): \033[1m{self.name.capitalize()}\033[0m"

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} ID_{self._id} {self.name.upper()}, value={self.value}>"


    @property
    @abstractmethod
    def value(self) -> Any: ...


    @property
    def name(self) -> str:
        return self._name
    

    @property
    def id(self) -> Any:
        return self._id


    @classmethod
    def _increment_class_incrementals(cls) -> None:
        cls._id += 1



class Manner(ArticulatoryProperty):
    def __init__(self, name: str, value: int) -> None:
        super().__init__(name)
        self._value: int = value

    @property
    def value(self) -> int:
        return self._value



class Place(ArticulatoryProperty):

    def __init__(self, name: str, range: tuple[int, int] | int , description: str = "") -> None:
        super().__init__(name)
        if isinstance(range, tuple):
            self._min: int = range[0]
            self._max: int = range[1]
        else:
            self._min: int = range
            self._max: int = range

    @property
    def value(self) -> tuple[int, ...]:
        return tuple(range(self._min, self._max + 1))



NASAL               = Manner("nasal", 1)
PLOSIVE             = Manner("plosive", 2)
FRICATIVE           = Manner("fricative", 3)
APPROXIMANT         = Manner("approximant", 4)
TAP                 = Manner("tap", 5)
FLAP                = Manner("flap", 6)
TRILL               = Manner("trill", 7)
LATERAL_FRICATIVE   = Manner("lateral fricative", 8)
LATERAL_APPROXIMANT = Manner("lateral approximant", 9)

LABIAL              = Place("labial", (1, 3))
CORONAL             = Place("coronal", (4, 9))
DORSAL              = Place("dorsal", (10, 12))
LARYNGEAL           = Place("laryngeal", (13, 14))

BILABIAL            = Place("bilabial", 1)
LABIODENTAL         = Place("labiodental", 2)
LINGUOLABIAL        = Place("linguolabial", (3, 4)) # this is not an official IPA place of articulation
DENTAL              = Place("dental", 5)
ALVEOLAR            = Place("alveolar", 6)
POSTALVEOLAR        = Place("postalveolar", 7)
RETROFLEX           = Place("retroflex", 8)
PALATAL             = Place("palatal", (9, 10))
VELAR               = Place("velar", 11)
UVULAR              = Place("uvular", 12)
PHARYNGEAL          = Place("pharyngeal", 13)
GLOTTAL             = Place("glottal", 14)

IPA_MANNERS_OF_ARTICULATION: tuple[Manner, ...] = (
    NASAL,
    PLOSIVE,
    FRICATIVE,
    APPROXIMANT,
    TAP,
    FLAP,
    TRILL,
    LATERAL_FRICATIVE,
    LATERAL_APPROXIMANT,
)

IPA_PLACES_OF_ARTICULATION: tuple[Place, ...] = (
    BILABIAL,
    LABIODENTAL,
    DENTAL,
    ALVEOLAR,
    POSTALVEOLAR,
    RETROFLEX,
    PALATAL,
    VELAR,
    UVULAR,
    PHARYNGEAL,
    GLOTTAL,
)