from clck.articulatory_properties import MannerOfArticulation
from clck.articulatory_properties import Phonation
from clck.articulatory_properties import PlaceOfArticulation
from clck.containers import PhonemeGroup
from clck.phonetics import PulmonicConsonantPhone
from clck.phonology import ConsonantPhoneme
from clck.phonology import VowelPhoneme


IPA_VOICED_BILABIAL_PLOSIVE     = ConsonantPhoneme(PulmonicConsonantPhone("\u0062", PlaceOfArticulation.BILABIAL, MannerOfArticulation.PLOSIVE, Phonation.VOICED, (), True))
IPA_VOICELESS_BILABIAL_PLOSIVE  = ConsonantPhoneme(PulmonicConsonantPhone("\u0070", PlaceOfArticulation.BILABIAL, MannerOfArticulation.PLOSIVE, Phonation.VOICELESS, (), True))
IPA_VOICED_ALVEOLAR_PLOSIVE     = ConsonantPhoneme(PulmonicConsonantPhone("\u0064", PlaceOfArticulation.ALVEOLAR, MannerOfArticulation.PLOSIVE, Phonation.VOICED, (), True))
IPA_VOICELESS_ALVEOLAR_PLOSIVE  = ConsonantPhoneme(PulmonicConsonantPhone("\u0074", PlaceOfArticulation.ALVEOLAR, MannerOfArticulation.PLOSIVE, Phonation.VOICELESS, (), True))
IPA_VOICED_RETROFLEX_PLOSIVE    = ConsonantPhoneme(PulmonicConsonantPhone("\u0256", PlaceOfArticulation.RETROFLEX, MannerOfArticulation.PLOSIVE, Phonation.VOICED, (), True))
IPA_VOICELESS_RETROFLEX_PLOSIVE = ConsonantPhoneme(PulmonicConsonantPhone("\u0288", PlaceOfArticulation.RETROFLEX, MannerOfArticulation.PLOSIVE, Phonation.VOICELESS, (), True))
IPA_VOICED_PALATAL_PLOSIVE      = ConsonantPhoneme(PulmonicConsonantPhone("\u025f", PlaceOfArticulation.PALATAL, MannerOfArticulation.PLOSIVE, Phonation.VOICED, (), True))
IPA_VOICELESS_PALATAL_PLOSIVE   = ConsonantPhoneme(PulmonicConsonantPhone("\u0063", PlaceOfArticulation.PALATAL, MannerOfArticulation.PLOSIVE, Phonation.VOICELESS, (), True))
IPA_VOICED_VELAR_PLOSIVE        = ConsonantPhoneme(PulmonicConsonantPhone("\u0261", PlaceOfArticulation.VELAR, MannerOfArticulation.PLOSIVE, Phonation.VOICED, (), True))
IPA_VOICELESS_VELAR_PLOSIVE     = ConsonantPhoneme(PulmonicConsonantPhone("\u006b", PlaceOfArticulation.VELAR, MannerOfArticulation.PLOSIVE, Phonation.VOICELESS, (), True))
IPA_VOICED_UVULAR_PLOSIVE       = ConsonantPhoneme(PulmonicConsonantPhone("\u0262", PlaceOfArticulation.UVULAR, MannerOfArticulation.PLOSIVE, Phonation.VOICED, (), True))
IPA_VOICELESS_UVULAR_PLOSIVE    = ConsonantPhoneme(PulmonicConsonantPhone("\u0071", PlaceOfArticulation.UVULAR, MannerOfArticulation.PLOSIVE, Phonation.VOICELESS, (), True))
IPA_VOICED_GLOTTAL_PLOSIVE      = ConsonantPhoneme(PulmonicConsonantPhone("\u0294", PlaceOfArticulation.GLOTTAL, MannerOfArticulation.PLOSIVE, Phonation.VOICED, (), True))
IPA_VOICED_BILABIAL_NASAL       = ConsonantPhoneme(PulmonicConsonantPhone("\u006d", PlaceOfArticulation.BILABIAL, MannerOfArticulation.NASAL, Phonation.VOICELESS, (), True))
IPA_VOICED_LABIODENTAL_NASAL    = ConsonantPhoneme(PulmonicConsonantPhone("\u0271", PlaceOfArticulation.LABIODENTAL, MannerOfArticulation.NASAL, Phonation.VOICELESS, (), True))
IPA_VOICED_ALVEOLAR_NASAL       = ConsonantPhoneme(PulmonicConsonantPhone("\u006e", PlaceOfArticulation.ALVEOLAR, MannerOfArticulation.NASAL, Phonation.VOICELESS, (), True))
IPA_VOICED_RETROFLEX_NASAL      = ConsonantPhoneme(PulmonicConsonantPhone("\u0273", PlaceOfArticulation.RETROFLEX, MannerOfArticulation.NASAL, Phonation.VOICELESS, (), True))
IPA_VOICED_PALATAL_NASAL        = ConsonantPhoneme(PulmonicConsonantPhone("\u0272", PlaceOfArticulation.PALATAL, MannerOfArticulation.NASAL, Phonation.VOICELESS, (), True))
IPA_VOICED_VELAR_NASAL          = ConsonantPhoneme(PulmonicConsonantPhone("\u014b", PlaceOfArticulation.VELAR, MannerOfArticulation.NASAL, Phonation.VOICELESS, (), True))
IPA_VOICED_UVULAR_NASAL         = ConsonantPhoneme(PulmonicConsonantPhone("\u0274", PlaceOfArticulation.UVULAR, MannerOfArticulation.NASAL, Phonation.VOICELESS, (), True))
IPA_VOICED_BILABIAL_TRILL       = ConsonantPhoneme(PulmonicConsonantPhone("\u0299", PlaceOfArticulation.BILABIAL, MannerOfArticulation.TRILL, Phonation.VOICELESS, (), True))
IPA_VOICED_ALVEOLAR_TRILL       = ConsonantPhoneme(PulmonicConsonantPhone("\u0072", PlaceOfArticulation.ALVEOLAR, MannerOfArticulation.TRILL, Phonation.VOICELESS, (), True))
IPA_VOICED_UVULAR_TRILL         = ConsonantPhoneme(PulmonicConsonantPhone("\u0280", PlaceOfArticulation.UVULAR, MannerOfArticulation.TRILL, Phonation.VOICELESS, (), True))
IPA_VOICED_LABIODENTAL_FLAP     = ConsonantPhoneme(PulmonicConsonantPhone("\u2c71", PlaceOfArticulation.LABIODENTAL, MannerOfArticulation.FLAP, Phonation.VOICELESS, (), True))

DEFAULT_PATTERN_WILDCARDS: dict[str, PhonemeGroup] = {
    "C" : PhonemeGroup.from_type("C", ConsonantPhoneme),
    "V" : PhonemeGroup.from_type("V", VowelPhoneme),
}