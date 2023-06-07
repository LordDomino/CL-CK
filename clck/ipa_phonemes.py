from .phonology.articulatory_properties import *
from .phonology.phonemes import Phoneme, PulmonicConsonant, Vowel



# VOWELS
IPA_CLOSE_FRONT_UNROUNDED_VOWEL           = Vowel("i", FRONT, CLOSE, UNROUNDED)
IPA_CLOSE_FRONT_ROUNDED_VOWEL             = Vowel("y", FRONT, CLOSE, ROUNDED)
IPA_CLOSE_CENTRAL_UNROUNDED_VOWEL         = Vowel("ɨ", CENTRAL, CLOSE, UNROUNDED)
IPA_CLOSE_CENTRAL_ROUNDED_VOWEL           = Vowel("ʉ", CENTRAL, CLOSE, ROUNDED)
IPA_CLOSE_BACK_UNROUNDED_VOWEL            = Vowel("ɯ", BACK, CLOSE, UNROUNDED)
IPA_CLOSE_BACK_ROUNDED_VOWEL              = Vowel("u", BACK, CLOSE, ROUNDED)
IPA_NEARCLOSE_FRONT_UNROUNDED_VOWEL       = Vowel("ɪ", FRONT, NEARCLOSE, UNROUNDED)
IPA_NEARCLOSE_FRONT_ROUNDED_VOWEL         = Vowel("ʏ", FRONT, NEARCLOSE, ROUNDED)
IPA_NEARCLOSE_BACK_ROUNDED_VOWEL          = Vowel("ʊ", BACK, NEARCLOSE, ROUNDED)
IPA_CLOSEMID_FRONT_UNROUNDED_VOWEL        = Vowel("e", FRONT, CLOSEMID, UNROUNDED)
IPA_CLOSEMID_FRONT_ROUNDED_VOWEL          = Vowel("ø", FRONT, CLOSEMID, ROUNDED)
IPA_CLOSEMID_CENTRAL_UNROUNDED_VOWEL      = Vowel("ɘ", CENTRAL, CLOSEMID, UNROUNDED)
IPA_CLOSEMID_CENTRAL_ROUNDED_VOWEL        = Vowel("ɵ", CENTRAL, CLOSEMID, ROUNDED)
IPA_CLOSEMID_BACK_UNROUNDED_VOWEL         = Vowel("ɤ", BACK, CLOSEMID, UNROUNDED)
IPA_CLOSEMID_BACK_ROUNDED_VOWEL           = Vowel("o", BACK, CLOSEMID, ROUNDED)
IPA_MID_CENTRAL_VOWEL                     = Vowel("ə", CENTRAL, MID, NEUTRAL_ROUNDEDNESS)
IPA_OPENMID_FRONT_UNROUNDED_VOWEL         = Vowel("ɛ", FRONT, OPENMID, UNROUNDED)
IPA_OPENMID_FRONT_ROUNDED_VOWEL           = Vowel("œ", FRONT, OPENMID, ROUNDED)
IPA_OPENMID_CENTRAL_UNROUNDED_VOWEL       = Vowel("ɜ", CENTRAL, OPENMID, UNROUNDED)
IPA_OPENMID_CENTRAL_ROUNDED_VOWEL         = Vowel("ɞ", CENTRAL, OPENMID, ROUNDED)
IPA_OPENMID_BACK_UNROUNDED_VOWEL          = Vowel("ʌ", BACK, OPENMID, UNROUNDED)
IPA_OPENMID_BACK_ROUNDED_VOWEL            = Vowel("ɔ", BACK, OPENMID, ROUNDED)
IPA_NEAROPEN_FRONT_UNROUNDED_VOWEL        = Vowel("æ", FRONT, NEAROPEN, UNROUNDED)
IPA_NEAROPEN_CENTRAL_VOWEL                = Vowel("ɐ", CENTRAL, NEAROPEN, NEUTRAL_ROUNDEDNESS)
IPA_OPEN_FRONT_UNROUNDED_VOWEL            = Vowel("a", FRONT, OPEN, UNROUNDED)
IPA_OPEN_FRONT_ROUNDED_VOWEL              = Vowel("ɶ", FRONT, OPEN, ROUNDED)
IPA_OPEN_BACK_UNROUNDED_VOWEL             = Vowel("ɑ", BACK, OPEN, UNROUNDED)
IPA_OPEN_BACK_ROUNDED_VOWEL               = Vowel("ɒ", BACK, OPEN, ROUNDED)

# PULMONIC CONSONANT PLOSIVES
IPA_VOICELESS_BILABIAL_PLOSIVE            = PulmonicConsonant("p", BILABIAL, PLOSIVE, VOICELESS)
IPA_VOICED_BILABIAL_PLOSIVE               = PulmonicConsonant("b", BILABIAL, PLOSIVE, VOICED)
IPA_VOICELESS_ALVEOLAR_PLOSIVE            = PulmonicConsonant("t", ALVEOLAR, PLOSIVE, VOICELESS)
IPA_VOICED_ALVEOLAR_PLOSIVE               = PulmonicConsonant("d", ALVEOLAR, PLOSIVE, VOICED)
IPA_VOICELESS_RETROFLEX_PLOSIVE           = PulmonicConsonant("ʈ", RETROFLEX, PLOSIVE, VOICELESS)
IPA_VOICED_RETROFLEX_PLOSIVE              = PulmonicConsonant("ɖ", RETROFLEX, PLOSIVE, VOICED)
IPA_VOICELESS_PALATAL_PLOSIVE             = PulmonicConsonant("c", PALATAL, PLOSIVE, VOICELESS)
IPA_VOICED_PALATAL_PLOSIVE                = PulmonicConsonant("ɟ", PALATAL, PLOSIVE, VOICED)
IPA_VOICELESS_VELAR_PLOSIVE               = PulmonicConsonant("k", VELAR, PLOSIVE, VOICELESS)
IPA_VOICED_VELAR_PLOSIVE                  = PulmonicConsonant("ɡ", VELAR, PLOSIVE, VOICED)
IPA_VOICELESS_UVULAR_PLOSIVE              = PulmonicConsonant("q", VELAR, PLOSIVE, VOICELESS)
IPA_VOICED_UVULAR_PLOSIVE                 = PulmonicConsonant("ɢ", UVULAR, PLOSIVE, VOICED)
IPA_VOICELESS_GLOTTAL_PLOSIVE             = PulmonicConsonant("ʔ", GLOTTAL, PLOSIVE, VOICED)

# PULMONIC CONSONANT NASALS
IPA_VOICED_BILABIAL_NASAL                 = PulmonicConsonant("m", BILABIAL, NASAL, VOICED)
IPA_VOICED_LABIODENTAL_NASAL              = PulmonicConsonant("ɱ", LABIODENTAL, NASAL, VOICED)
IPA_VOICED_ALVEOLAR_NASAL                 = PulmonicConsonant("n", ALVEOLAR, NASAL, VOICED)
IPA_VOICED_RETROFLEX_NASAL                = PulmonicConsonant("ɳ", RETROFLEX, NASAL, VOICED)
IPA_VOICED_PALATAL_NASAL                  = PulmonicConsonant("ɲ", PALATAL, NASAL, VOICED)
IPA_VOICED_VELAR_NASAL                    = PulmonicConsonant("ŋ", VELAR, NASAL, VOICED)
IPA_VOICED_UVULAR_NASAL                   = PulmonicConsonant("ɴ", UVULAR, NASAL, VOICED)

# PULMONIC CONSONANT TRILLS
IPA_VOICED_BILABIAL_TRILL                 = PulmonicConsonant("ʙ", BILABIAL, TRILL, VOICED)
IPA_VOICED_ALVEOLAR_TRILL                 = PulmonicConsonant("r", ALVEOLAR, TRILL, VOICED)
IPA_VOICED_UVULAR_TRILL                   = PulmonicConsonant("ʀ", UVULAR, TRILL, VOICED)

# PULMONIC CONSONANT TAPS OR FLAPS
IPA_VOICED_LABIODENTAL_TAPFLAP            = PulmonicConsonant("ⱱ", LABIODENTAL, TAP, VOICED)
IPA_VOICED_ALVEOLAR_TAPFLAP               = PulmonicConsonant("ɾ", ALVEOLAR, TAP, VOICED)
IPA_VOICED_RETROFLEX_TAPFLAP              = PulmonicConsonant("ɽ", RETROFLEX, TAP, VOICED)

# PULMONIC CONSONANT NONSIBILANT FRICATIVES
IPA_VOICELESS_BILABIAL_FRICATIVE          = PulmonicConsonant("ɸ", BILABIAL, FRICATIVE, VOICELESS)
IPA_VOICED_BILABIAL_FRICATIVE             = PulmonicConsonant("β", BILABIAL, FRICATIVE, VOICED)
IPA_VOICELESS_LABIODENTAL_FRICATIVE       = PulmonicConsonant("f", LABIODENTAL, FRICATIVE, VOICELESS)
IPA_VOICED_LABIODENTAL_FRICATIVE          = PulmonicConsonant("v", LABIODENTAL, FRICATIVE, VOICED)
IPA_VOICELESS_DENTAL_FRICATIVE            = PulmonicConsonant("θ", DENTAL, FRICATIVE, VOICELESS)
IPA_VOICED_DENTAL_FRICATIVE               = PulmonicConsonant("ð", DENTAL, FRICATIVE, VOICED)
IPA_VOICELESS_ALVEOLAR_FRICATIVE          = PulmonicConsonant("s", ALVEOLAR, FRICATIVE, VOICELESS)
IPA_VOICED_ALVEOLAR_FRICATIVE             = PulmonicConsonant("z", ALVEOLAR, FRICATIVE, VOICED)
IPA_VOICELESS_POSTALVEOLAR_FRICATIVE      = PulmonicConsonant("ʃ", POSTALVEOLAR, FRICATIVE, VOICELESS)
IPA_VOICED_POSTALVEOLAR_FRICATIVE         = PulmonicConsonant("ʒ", POSTALVEOLAR, FRICATIVE, VOICED)
IPA_VOICELESS_RETROFLEX_FRICATIVE         = PulmonicConsonant("ʂ", RETROFLEX, FRICATIVE, VOICELESS)
IPA_VOICED_RETROFLEX_FRICATIVE            = PulmonicConsonant("ʐ", RETROFLEX, FRICATIVE, VOICED)
IPA_VOICELESS_PALATAL_FRICATIVE           = PulmonicConsonant("ç", PALATAL, FRICATIVE, VOICELESS)
IPA_VOICED_PALATAL_FRICATIVE              = PulmonicConsonant("ʝ", PALATAL, FRICATIVE, VOICED)
IPA_VOICELESS_VELAR_FRICATIVE             = PulmonicConsonant("x", VELAR, FRICATIVE, VOICELESS)
IPA_VOICED_VELAR_FRICATIVE                = PulmonicConsonant("ɣ", VELAR, FRICATIVE, VOICED)
IPA_VOICELESS_UVULAR_FRICATIVE            = PulmonicConsonant("χ", UVULAR, FRICATIVE, VOICELESS)
IPA_VOICED_UVULAR_FRICATIVE               = PulmonicConsonant("ʁ", UVULAR, FRICATIVE, VOICED)
IPA_VOICELESS_EPIGLOTTAL_FRICATIVE        = PulmonicConsonant("ħ", PHARYNGEAL, FRICATIVE, VOICELESS)
IPA_VOICED_EPIGLOTTAL_FRICATIVE           = PulmonicConsonant("ʕ", PHARYNGEAL, FRICATIVE, VOICED)
IPA_VOICELESS_GLOTTAL_FRICATIVE           = PulmonicConsonant("h", GLOTTAL, FRICATIVE, VOICELESS)
IPA_VOICED_GLOTTAL_FRICATIVE              = PulmonicConsonant("ɦ", GLOTTAL, FRICATIVE, VOICED)

# PULMONIC CONSONANT LATERAL FRICATIVES
IPA_VOICELESS_ALVEOLAR_LATERALFRICATIVE   = PulmonicConsonant("ɬ", ALVEOLAR, LATERAL_FRICATIVE, VOICELESS)
IPA_VOICED_ALVEOLAR_LATERALFRICATIVE      = PulmonicConsonant("ɮ", ALVEOLAR, LATERAL_FRICATIVE, VOICED)

# PULMONIC CONSONANT APPROXIMANTS
IPA_VOICED_LABIODENTAL_APPROXIMANT        = PulmonicConsonant("ʋ", LABIODENTAL, APPROXIMANT, VOICED)
IPA_VOICED_ALVEOLAR_APPROXIMANT           = PulmonicConsonant("ɹ", ALVEOLAR, APPROXIMANT, VOICED)
IPA_VOICED_RETROFLEX_APPROXIMANT          = PulmonicConsonant("ɻ", RETROFLEX, APPROXIMANT, VOICED)
IPA_VOICED_PALATAL_APPROXIMANT            = PulmonicConsonant("j", PALATAL, APPROXIMANT, VOICED)
IPA_VOICED_VELAR_APPROXIMANT              = PulmonicConsonant("ɰ", VELAR, APPROXIMANT, VOICED)

# PULMONIC CONSONANT LATERAL APPROXIMANTS
IPA_VOICED_ALVEOLAR_LATERALAPPROXIMANT    = PulmonicConsonant("l", ALVEOLAR, LATERAL_APPROXIMANT, VOICED)
IPA_VOICED_RETROFLEX_LATERALAPPROXIMANT   = PulmonicConsonant("ɭ", RETROFLEX, LATERAL_APPROXIMANT, VOICED)
IPA_VOICED_PALATAL_LATERALAPPROXIMANT     = PulmonicConsonant("ʎ", PALATAL, LATERAL_APPROXIMANT, VOICED)
IPA_VOICED_VELAR_LATERALAPPROXIMANT       = PulmonicConsonant("ʟ", VELAR, LATERAL_APPROXIMANT, VOICED)


DEFAULT_IPA_PHONEMES: tuple[Phoneme, ...] = (
    IPA_CLOSE_FRONT_UNROUNDED_VOWEL,
    IPA_CLOSE_FRONT_ROUNDED_VOWEL,
    IPA_CLOSE_CENTRAL_UNROUNDED_VOWEL,
    IPA_CLOSE_CENTRAL_ROUNDED_VOWEL,
    IPA_CLOSE_BACK_UNROUNDED_VOWEL,
    IPA_CLOSE_BACK_ROUNDED_VOWEL,
    IPA_NEARCLOSE_FRONT_UNROUNDED_VOWEL,
    IPA_NEARCLOSE_FRONT_ROUNDED_VOWEL,
    IPA_NEARCLOSE_BACK_ROUNDED_VOWEL,
    IPA_CLOSEMID_FRONT_UNROUNDED_VOWEL,
    IPA_CLOSEMID_FRONT_ROUNDED_VOWEL,
    IPA_CLOSEMID_CENTRAL_UNROUNDED_VOWEL,
    IPA_CLOSEMID_CENTRAL_ROUNDED_VOWEL,
    IPA_CLOSEMID_BACK_UNROUNDED_VOWEL,
    IPA_CLOSEMID_BACK_ROUNDED_VOWEL,
    IPA_MID_CENTRAL_VOWEL,
    IPA_OPENMID_FRONT_UNROUNDED_VOWEL,
    IPA_OPENMID_FRONT_ROUNDED_VOWEL,
    IPA_OPENMID_CENTRAL_UNROUNDED_VOWEL,
    IPA_OPENMID_CENTRAL_ROUNDED_VOWEL,
    IPA_OPENMID_BACK_UNROUNDED_VOWEL,
    IPA_OPENMID_BACK_ROUNDED_VOWEL,
    IPA_NEAROPEN_FRONT_UNROUNDED_VOWEL,
    IPA_NEAROPEN_CENTRAL_VOWEL,
    IPA_OPEN_FRONT_UNROUNDED_VOWEL,
    IPA_OPEN_FRONT_ROUNDED_VOWEL,
    IPA_OPEN_BACK_UNROUNDED_VOWEL,
    IPA_OPEN_BACK_ROUNDED_VOWEL,
    IPA_VOICELESS_BILABIAL_PLOSIVE,
    IPA_VOICED_BILABIAL_PLOSIVE,
    IPA_VOICELESS_ALVEOLAR_PLOSIVE,
    IPA_VOICED_ALVEOLAR_PLOSIVE,
    IPA_VOICELESS_RETROFLEX_PLOSIVE,
    IPA_VOICED_RETROFLEX_PLOSIVE,
    IPA_VOICELESS_PALATAL_PLOSIVE,
    IPA_VOICED_PALATAL_PLOSIVE,
    IPA_VOICELESS_VELAR_PLOSIVE,
    IPA_VOICED_VELAR_PLOSIVE,
    IPA_VOICELESS_UVULAR_PLOSIVE,
    IPA_VOICED_UVULAR_PLOSIVE,
    IPA_VOICELESS_GLOTTAL_PLOSIVE,
    IPA_VOICED_BILABIAL_NASAL,
    IPA_VOICED_LABIODENTAL_NASAL,
    IPA_VOICED_ALVEOLAR_NASAL,
    IPA_VOICED_RETROFLEX_NASAL,
    IPA_VOICED_PALATAL_NASAL,
    IPA_VOICED_VELAR_NASAL,
    IPA_VOICED_UVULAR_NASAL,
    IPA_VOICED_BILABIAL_TRILL,
    IPA_VOICED_ALVEOLAR_TRILL,
    IPA_VOICED_UVULAR_TRILL,
    IPA_VOICED_LABIODENTAL_TAPFLAP,
    IPA_VOICED_ALVEOLAR_TAPFLAP,
    IPA_VOICED_RETROFLEX_TAPFLAP,
    IPA_VOICELESS_BILABIAL_FRICATIVE,
    IPA_VOICED_BILABIAL_FRICATIVE,
    IPA_VOICELESS_LABIODENTAL_FRICATIVE,
    IPA_VOICED_LABIODENTAL_FRICATIVE,
    IPA_VOICELESS_DENTAL_FRICATIVE,
    IPA_VOICED_DENTAL_FRICATIVE,
    IPA_VOICELESS_ALVEOLAR_FRICATIVE,
    IPA_VOICED_ALVEOLAR_FRICATIVE,
    IPA_VOICELESS_POSTALVEOLAR_FRICATIVE,
    IPA_VOICED_POSTALVEOLAR_FRICATIVE,
    IPA_VOICELESS_RETROFLEX_FRICATIVE,
    IPA_VOICED_RETROFLEX_FRICATIVE,
    IPA_VOICELESS_PALATAL_FRICATIVE,
    IPA_VOICED_PALATAL_FRICATIVE,
    IPA_VOICELESS_VELAR_FRICATIVE,
    IPA_VOICED_VELAR_FRICATIVE,
    IPA_VOICELESS_UVULAR_FRICATIVE,
    IPA_VOICED_UVULAR_FRICATIVE,
    IPA_VOICELESS_EPIGLOTTAL_FRICATIVE,
    IPA_VOICED_EPIGLOTTAL_FRICATIVE,
    IPA_VOICELESS_GLOTTAL_FRICATIVE,
    IPA_VOICED_GLOTTAL_FRICATIVE,
    IPA_VOICELESS_ALVEOLAR_LATERALFRICATIVE,
    IPA_VOICED_ALVEOLAR_LATERALFRICATIVE,
    IPA_VOICED_LABIODENTAL_APPROXIMANT,
    IPA_VOICED_ALVEOLAR_APPROXIMANT,
    IPA_VOICED_RETROFLEX_APPROXIMANT,
    IPA_VOICED_PALATAL_APPROXIMANT,
    IPA_VOICED_VELAR_APPROXIMANT,
    IPA_VOICED_ALVEOLAR_LATERALAPPROXIMANT,
    IPA_VOICED_RETROFLEX_LATERALAPPROXIMANT,
    IPA_VOICED_PALATAL_LATERALAPPROXIMANT,
    IPA_VOICED_VELAR_LATERALAPPROXIMANT,
)
