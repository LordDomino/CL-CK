from clck.fundamentals.phonology import Consonant, Phoneme, Vowel
from clck.phonology.containers import PhoneGroup
from .phonology.articulatory_properties import *
from .fundamentals.phonetics import DummyPhone, PulmonicConsonant



DUMMY_PHONEME = DummyPhone()

IPA_VOICED_BILABIAL_PLOSIVE         = Phoneme(PulmonicConsonant("p", PlaceOfArticulation.BILABIAL, MannerOfArticulation.PLOSIVE, Phonation.VOICED, (), True))
IPA_VOICELESS_BILABIAL_PLOSIVE      = Phoneme(PulmonicConsonant("p", PlaceOfArticulation.BILABIAL, MannerOfArticulation.PLOSIVE, Phonation.VOICELESS, (), True))
IPA_VOICED_ALVEOLAR_PLOSIVE         = Phoneme(PulmonicConsonant("p", PlaceOfArticulation.ALVEOLAR, MannerOfArticulation.PLOSIVE, Phonation.VOICED, (), True))
IPA_VOICELESS_ALVEOLAR_PLOSIVE      = Phoneme(PulmonicConsonant("p", PlaceOfArticulation.ALVEOLAR, MannerOfArticulation.PLOSIVE, Phonation.VOICELESS, (), True))
IPA_VOICED_RETROFLEX_PLOSIVE        = Phoneme(PulmonicConsonant("p", PlaceOfArticulation.RETROFLEX, MannerOfArticulation.PLOSIVE, Phonation.VOICED, (), True))
IPA_VOICELESS_RETROFLEX_PLOSIVE     = Phoneme(PulmonicConsonant("p", PlaceOfArticulation.RETROFLEX, MannerOfArticulation.PLOSIVE, Phonation.VOICELESS, (), True))
IPA_VOICED_PALATAL_PLOSIVE          = Phoneme(PulmonicConsonant("p", PlaceOfArticulation.PALATAL, MannerOfArticulation.PLOSIVE, Phonation.VOICED, (), True))
IPA_VOICELESS_PALATAL_PLOSIVE       = Phoneme(PulmonicConsonant("p", PlaceOfArticulation.PALATAL, MannerOfArticulation.PLOSIVE, Phonation.VOICELESS, (), True))
IPA_VOICED_VELAR_PLOSIVE            = Phoneme(PulmonicConsonant("p", PlaceOfArticulation.VELAR, MannerOfArticulation.PLOSIVE, Phonation.VOICED, (), True))
IPA_VOICELESS_VELAR_PLOSIVE         = Phoneme(PulmonicConsonant("p", PlaceOfArticulation.VELAR, MannerOfArticulation.PLOSIVE, Phonation.VOICELESS, (), True))
IPA_VOICED_UVULAR_PLOSIVE           = Phoneme(PulmonicConsonant("p", PlaceOfArticulation.UVULAR, MannerOfArticulation.PLOSIVE, Phonation.VOICED, (), True))
IPA_VOICELESS_UVULAR_PLOSIVE        = Phoneme(PulmonicConsonant("p", PlaceOfArticulation.UVULAR, MannerOfArticulation.PLOSIVE, Phonation.VOICELESS, (), True))
IPA_VOICED_GLOTTAL_PLOSIVE          = Phoneme(PulmonicConsonant("p", PlaceOfArticulation.GLOTTAL, MannerOfArticulation.PLOSIVE, Phonation.VOICED, (), True))
IPA_VOICELESS_BILABIAL_NASAL        = Phoneme(PulmonicConsonant("p", PlaceOfArticulation.BILABIAL, MannerOfArticulation.NASAL, Phonation.VOICELESS, (), True))
IPA_VOICELESS_LABIODENTAL_NASAL     = Phoneme(PulmonicConsonant("p", PlaceOfArticulation.LABIODENTAL, MannerOfArticulation.NASAL, Phonation.VOICELESS, (), True))
IPA_VOICELESS_ALVEOLAR_NASAL        = Phoneme(PulmonicConsonant("p", PlaceOfArticulation.ALVEOLAR, MannerOfArticulation.NASAL, Phonation.VOICELESS, (), True))
IPA_VOICELESS_RETROFLEX_NASAL       = Phoneme(PulmonicConsonant("p", PlaceOfArticulation.RETROFLEX, MannerOfArticulation.NASAL, Phonation.VOICELESS, (), True))
IPA_VOICELESS_PALATAL_NASAL         = Phoneme(PulmonicConsonant("p", PlaceOfArticulation.PALATAL, MannerOfArticulation.NASAL, Phonation.VOICELESS, (), True))
IPA_VOICELESS_VELAR_NASAL           = Phoneme(PulmonicConsonant("p", PlaceOfArticulation.VELAR, MannerOfArticulation.NASAL, Phonation.VOICELESS, (), True))
IPA_VOICELESS_UVULAR_NASAL          = Phoneme(PulmonicConsonant("p", PlaceOfArticulation.UVULAR, MannerOfArticulation.NASAL, Phonation.VOICELESS, (), True))
IPA_VOICELESS_BILABIAL_TRILL        = Phoneme(PulmonicConsonant("p", PlaceOfArticulation.BILABIAL, MannerOfArticulation.TRILL, Phonation.VOICELESS, (), True))
IPA_VOICELESS_ALVEOLAR_TRILL        = Phoneme(PulmonicConsonant("p", PlaceOfArticulation.ALVEOLAR, MannerOfArticulation.TRILL, Phonation.VOICELESS, (), True))
IPA_VOICELESS_UVULAR_TRILL          = Phoneme(PulmonicConsonant("p", PlaceOfArticulation.UVULAR, MannerOfArticulation.TRILL, Phonation.VOICELESS, (), True))
IPA_VOICELESS_LABIODENTAL_TAP       = Phoneme(PulmonicConsonant("p", PlaceOfArticulation.LABIODENTAL, MannerOfArticulation.TAP, Phonation.VOICELESS, (), True))


DEFAULT_PATTERN_WILDCARDS: dict[str, PhoneGroup] = {
    "C" : PhoneGroup.from_type("C", Consonant),
    "V" : PhoneGroup.from_type("V", Vowel),
    # "N" : PhonemeGroup.from_property("N", "nasal"),
    # "A" : PhoneGroup.from_property("A", "approximant"),
    # "S" : PhoneGroup.from_property("S", "plosive")
}