from clck.fundamentals.phonology import Consonant, Dummy, Vowel
from clck.phonology.containers import PhonemeGroup
from .phonology.articulatory_properties import *
from .fundamentals.phonetics import PulmonicConsonant


DUMMY = DUMMY_PHONEME = Dummy()

IPA_VOICED_BILABIAL_PLOSIVE         = Consonant(PulmonicConsonant("p", PlaceOfArticulation.BILABIAL, MannerOfArticulation.PLOSIVE, Phonation.VOICED, (), True))
IPA_VOICELESS_BILABIAL_PLOSIVE      = Consonant(PulmonicConsonant("p", PlaceOfArticulation.BILABIAL, MannerOfArticulation.PLOSIVE, Phonation.VOICELESS, (), True))
IPA_VOICED_ALVEOLAR_PLOSIVE         = Consonant(PulmonicConsonant("p", PlaceOfArticulation.ALVEOLAR, MannerOfArticulation.PLOSIVE, Phonation.VOICED, (), True))
IPA_VOICELESS_ALVEOLAR_PLOSIVE      = Consonant(PulmonicConsonant("p", PlaceOfArticulation.ALVEOLAR, MannerOfArticulation.PLOSIVE, Phonation.VOICELESS, (), True))
IPA_VOICED_RETROFLEX_PLOSIVE        = Consonant(PulmonicConsonant("p", PlaceOfArticulation.RETROFLEX, MannerOfArticulation.PLOSIVE, Phonation.VOICED, (), True))
IPA_VOICELESS_RETROFLEX_PLOSIVE     = Consonant(PulmonicConsonant("p", PlaceOfArticulation.RETROFLEX, MannerOfArticulation.PLOSIVE, Phonation.VOICELESS, (), True))
IPA_VOICED_PALATAL_PLOSIVE          = Consonant(PulmonicConsonant("p", PlaceOfArticulation.PALATAL, MannerOfArticulation.PLOSIVE, Phonation.VOICED, (), True))
IPA_VOICELESS_PALATAL_PLOSIVE       = Consonant(PulmonicConsonant("p", PlaceOfArticulation.PALATAL, MannerOfArticulation.PLOSIVE, Phonation.VOICELESS, (), True))
IPA_VOICED_VELAR_PLOSIVE            = Consonant(PulmonicConsonant("p", PlaceOfArticulation.VELAR, MannerOfArticulation.PLOSIVE, Phonation.VOICED, (), True))
IPA_VOICELESS_VELAR_PLOSIVE         = Consonant(PulmonicConsonant("p", PlaceOfArticulation.VELAR, MannerOfArticulation.PLOSIVE, Phonation.VOICELESS, (), True))
IPA_VOICED_UVULAR_PLOSIVE           = Consonant(PulmonicConsonant("p", PlaceOfArticulation.UVULAR, MannerOfArticulation.PLOSIVE, Phonation.VOICED, (), True))
IPA_VOICELESS_UVULAR_PLOSIVE        = Consonant(PulmonicConsonant("p", PlaceOfArticulation.UVULAR, MannerOfArticulation.PLOSIVE, Phonation.VOICELESS, (), True))
IPA_VOICED_GLOTTAL_PLOSIVE          = Consonant(PulmonicConsonant("p", PlaceOfArticulation.GLOTTAL, MannerOfArticulation.PLOSIVE, Phonation.VOICED, (), True))
IPA_VOICELESS_BILABIAL_NASAL        = Consonant(PulmonicConsonant("p", PlaceOfArticulation.BILABIAL, MannerOfArticulation.NASAL, Phonation.VOICELESS, (), True))
IPA_VOICELESS_LABIODENTAL_NASAL     = Consonant(PulmonicConsonant("p", PlaceOfArticulation.LABIODENTAL, MannerOfArticulation.NASAL, Phonation.VOICELESS, (), True))
IPA_VOICELESS_ALVEOLAR_NASAL        = Consonant(PulmonicConsonant("p", PlaceOfArticulation.ALVEOLAR, MannerOfArticulation.NASAL, Phonation.VOICELESS, (), True))
IPA_VOICELESS_RETROFLEX_NASAL       = Consonant(PulmonicConsonant("p", PlaceOfArticulation.RETROFLEX, MannerOfArticulation.NASAL, Phonation.VOICELESS, (), True))
IPA_VOICELESS_PALATAL_NASAL         = Consonant(PulmonicConsonant("p", PlaceOfArticulation.PALATAL, MannerOfArticulation.NASAL, Phonation.VOICELESS, (), True))
IPA_VOICELESS_VELAR_NASAL           = Consonant(PulmonicConsonant("p", PlaceOfArticulation.VELAR, MannerOfArticulation.NASAL, Phonation.VOICELESS, (), True))
IPA_VOICELESS_UVULAR_NASAL          = Consonant(PulmonicConsonant("p", PlaceOfArticulation.UVULAR, MannerOfArticulation.NASAL, Phonation.VOICELESS, (), True))
IPA_VOICELESS_BILABIAL_TRILL        = Consonant(PulmonicConsonant("p", PlaceOfArticulation.BILABIAL, MannerOfArticulation.TRILL, Phonation.VOICELESS, (), True))
IPA_VOICELESS_ALVEOLAR_TRILL        = Consonant(PulmonicConsonant("p", PlaceOfArticulation.ALVEOLAR, MannerOfArticulation.TRILL, Phonation.VOICELESS, (), True))
IPA_VOICELESS_UVULAR_TRILL          = Consonant(PulmonicConsonant("p", PlaceOfArticulation.UVULAR, MannerOfArticulation.TRILL, Phonation.VOICELESS, (), True))
IPA_VOICELESS_LABIODENTAL_TAP       = Consonant(PulmonicConsonant("p", PlaceOfArticulation.LABIODENTAL, MannerOfArticulation.TAP, Phonation.VOICELESS, (), True))


DEFAULT_PATTERN_WILDCARDS: dict[str, PhonemeGroup] = {
    "C" : PhonemeGroup.from_type("C", Consonant),
    "V" : PhonemeGroup.from_type("V", Vowel),
}