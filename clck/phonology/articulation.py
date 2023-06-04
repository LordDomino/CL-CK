from abc import ABC, abstractmethod
from typing import Any



class PhonologicalProperty(ABC):

    _id: int = 1
    
    def __init__(self, name: str) -> None:
        super().__init__()
        self._name: str = name
        self._id: int = self.__class__._id
        self.__class__._increment_class_incrementals()

    @abstractmethod
    def __str__(self) -> str: pass

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} ID_{self._id} {self.name.upper()}, value={self.value}>"


    @property
    @abstractmethod
    def value(self) -> Any: pass


    @property
    def name(self) -> str:
        return self._name
    

    @property
    def id(self) -> Any:
        return self._id


    @classmethod
    def _increment_class_incrementals(cls) -> None:
        cls._id += 1



class ArticulatoryProperty(PhonologicalProperty):
    def __init__(self, name: str) -> None:
        super().__init__(name)

    @abstractmethod
    def __str__(self) -> str: pass



class Voicing(ArticulatoryProperty):
    def __init__(self, name: str, value: int) -> None:
        super().__init__(name)
        self._value: int = value

    def __str__(self) -> str:
        return f"Voicing (articulatory property, ID_{self._id}): \033[1m{self.name.capitalize()}\033[0m"
    
    @property
    def value(self) -> int:
        return self._value



class ConsonantalProperty(ArticulatoryProperty):
    def __init__(self, name: str) -> None:
        super().__init__(name)

    @abstractmethod
    def __str__(self) -> str: pass



class VocalicProperty(ArticulatoryProperty):
    def __init__(self, name: str) -> None:
        super().__init__(name)



class Manner(ConsonantalProperty):
    def __init__(self, name: str, value: int) -> None:
        super().__init__(name)
        self._value: int = value

    def __str__(self) -> str:
        return f"Manner of articulation (articulatory property, ID_{self._id}): \033[1m{self.name.capitalize()}\033[0m"

    @property
    def value(self) -> int:
        return self._value



class Place(ConsonantalProperty):
    def __init__(self, name: str, range: tuple[int, int] | int) -> None:
        super().__init__(name)
        if isinstance(range, tuple):
            self._min: int = range[0]
            self._max: int = range[1]
        else:
            self._min: int = range
            self._max: int = range

    def __str__(self) -> str:
        return f"Place of articulation (articulatory property, ID_{self._id}): \033[1m{self.name.capitalize()}\033[0m"


    @property
    def value(self) -> tuple[int, ...]:
        return tuple(range(self._min, self._max + 1))



class AirflowType: ...



class AirstreamMechanism(ConsonantalProperty):
    def __init__(self, name: str, value: float, airflow: AirflowType) -> None:
        super().__init__(name)
        self._value: float = value
        self._airflow: AirflowType = airflow

    
    @property
    def value(self) -> float:
        return self._value

    
    def __str__(self) -> str:
        return f"Airstream mechanism (articulatory property, ID_{self._id}): \033[1m{self.name.capitalize()}\033[0m"



class Height(VocalicProperty):
    def __init__(self, name: str, value: float) -> None:
        super().__init__(name)
        self._value: float = value

    
    def __str__(self) -> str:
        return f"Vowel height (articulatory property, ID_{self._id}): \033[1m{self.name.capitalize()}\033[0m"


    @property
    def value(self) -> float:
        return self._value    



class Backness(VocalicProperty):
    def __init__(self, name: str, value: float) -> None:
        super().__init__(name)
        self._value: float = value

    def __str__(self) -> str:
        return f"Vowel backness (articulatory property, ID_{self._id}): \033[1m{self.name.capitalize()}\033[0m"

    @property
    def value(self) -> float:
        return self._value


class Roundedness(VocalicProperty):
    def __init__(self, name: str, value: float) -> None:
        super().__init__(name)
        self._value: float = value

    def __str__(self) -> str:
        return f"Vowel roundedness (articulatory property, ID_{self._id}): \033[1m{self.name.capitalize()}\033[0m"

    @property
    def value(self) -> float:
        return self._value



# MAIN ARTICULATORY PROPERTIES
VOICED              = Voicing("voiced", 2)
VOICELESS           = Voicing("voiceless", 1)
UNVOICED            = Voicing("unvoiced", 0)

# CONSONANTAL ARTICULATORY PROPERTIES
# Manners of articulation of pulmonic consonants
NASAL               = Manner("nasal", 1)
PLOSIVE             = Manner("plosive", 2)
FRICATIVE           = Manner("fricative", 3)
APPROXIMANT         = Manner("approximant", 4)
TAP                 = Manner("tap", 5)
TRILL               = Manner("trill", 6)
LATERAL_FRICATIVE   = Manner("lateral fricative", 7)
LATERAL_APPROXIMANT = Manner("lateral approximant", 8)

# Broad places of articulation for pulmonic consonants
LABIAL              = Place("labial", (1, 3))
CORONAL             = Place("coronal", (4, 9))
DORSAL              = Place("dorsal", (10, 12))
LARYNGEAL           = Place("laryngeal", (13, 14))

# Specific places of articulation for pulmonic consonants, defined in the IPA chart
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

# Airflow types
EGRESSIVE = AirflowType()
INGRESSIVE = AirflowType()

# Airstream mechanisms
PULMONIC_EGRESSIVE  = AirstreamMechanism("pulmonic egressive", 0, EGRESSIVE)
GLOTTALIC_EGRESSIVE = AirstreamMechanism("glottalic egressive", 1, EGRESSIVE)
GLOTTALIC_INGRESSIVE = AirstreamMechanism("glottalic ingressive", 2, INGRESSIVE)
LINGUAL_INGRESSIVE  = AirstreamMechanism("lingual ingressive", 3, INGRESSIVE)
VELARIC_INGRESSIVE: AirstreamMechanism = LINGUAL_INGRESSIVE


# VOCALIC ARTICULATORY PROPERTIES
# Heights of articulation of vowels
CLOSE               = Height("close", 0)
NEARCLOSE           = Height("near-close", 1)
CLOSEMID            = Height("close-mid", 2)
MID                 = Height("mid", 3)
OPENMID             = Height("open-mid", 4)
NEAROPEN            = Height("near-open", 5)
OPEN                = Height("open", 6)

# Backnesses of articulation of vowels
FRONT               = Backness("front", 0)
NEARFRONT           = Backness("near front", 1)
CENTRAL             = Backness("central", 2)
NEARBACK            = Backness("near back", 3)
BACK                = Backness("back", 4)

# Roundedness of vowels
UNROUNDED           = Roundedness("unrounded", 0)
NEUTRAL_ROUNDEDNESS = Roundedness("", 0.5)
ROUNDED             = Roundedness("rounded", 1)



IPA_MANNERS_OF_CONSONANTAL_ARTICULATION: tuple[Manner, ...] = (
    NASAL,
    PLOSIVE,
    FRICATIVE,
    APPROXIMANT,
    TAP,
    TRILL,
    LATERAL_FRICATIVE,
    LATERAL_APPROXIMANT,
)

IPA_PLACES_OF_CONSONANTAL_ARTICULATION: tuple[Place, ...] = (
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