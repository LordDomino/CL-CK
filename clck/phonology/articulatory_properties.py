from enum import Enum, auto



class ArticulatoryProperty(Enum): ...
class ConsonantArticulatoryProperty(ArticulatoryProperty): ...
class VowelArticulatoryProperty(ArticulatoryProperty): ...

class PlaceOfArticulation(ConsonantArticulatoryProperty):
    """
    The enum class containing all the constants for the place of
    articulation.

    The place of articulation describes where in the mouth the
    constriction of airflow occurs.
    """
    BILABIAL = auto()
    LABIODENTAL = auto()
    DENTAL = auto()
    ALVEOLAR = auto()
    POSTALVEOLAR = auto()
    RETROFLEX = auto()
    PALATAL = auto()
    VELAR = auto()
    UVULAR = auto()
    PHARYNGEAL = auto()
    GLOTTAL = auto()

class MannerOfArticulation(ConsonantArticulatoryProperty):
    PLOSIVE = auto()
    NASAL = auto()
    TRILL = auto()
    TAP = auto()
    FLAP = TAP
    FRICATIVE = auto()
    LATERAL_FRICATIVE = auto()
    APPROXIMANT = auto()
    LATERAL_APPROXIMANT = auto()
    SIBILANT = auto()

class Phonation(ConsonantArticulatoryProperty):
    VOICELESS = auto()
    VOICED = auto()

class Backness(VowelArticulatoryProperty):
    FRONT = auto()
    CENTRAL = auto()
    BACK = auto()

class Height(VowelArticulatoryProperty):
    CLOSE = auto()
    CLOSE_MID = auto()
    OPEN_MID = auto()
    OPEN = auto()

class Roundedness(VowelArticulatoryProperty):
    UNROUNDED = auto()
    ROUNDED = auto()



class AirstreamMechanism(ConsonantArticulatoryProperty):

    PULMONIC = auto()
    """The constant that describes the airstream mechanism as
    pulmonic."""

    NONPULMONIC = auto()
    """The constant that describes the airstream mechanism as
    non-pulmonic."""