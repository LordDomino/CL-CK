from .phonology.phonemes import (
  Phoneme,
  IPA_Phoneme_PulmonicConsonant,
  Vowel
)



# VOWELS
IPA_CLOSE_FRONT_UNROUNDED_VOWEL: Phoneme                  = Vowel("i", "front", "close", False)
IPA_CLOSE_FRONT_ROUNDED_VOWEL: Phoneme                    = Vowel("y", "front", "close", True)
IPA_CLOSE_CENTRAL_UNROUNDED_VOWEL: Phoneme                = Vowel("ɨ", "central", "close", False)
IPA_CLOSE_CENTRAL_ROUNDED_VOWEL: Phoneme                  = Vowel("ʉ", "central", "close", True)
IPA_CLOSE_BACK_UNROUNDED_VOWEL: Phoneme                   = Vowel("ɯ", "back", "close", False)
IPA_CLOSE_BACK_ROUNDED_VOWEL: Phoneme                     = Vowel("u", "back", "close", True)
IPA_NEARCLOSE_FRONT_UNROUNDED_VOWEL: Phoneme              = Vowel("ɪ", "front", "nearclose", False)
IPA_NEARCLOSE_FRONT_ROUNDED_VOWEL: Phoneme                = Vowel("ʏ", "front", "nearclose", True)
IPA_NEARCLOSE_BACK_ROUNDED_VOWEL: Phoneme                 = Vowel("ʊ", "back", "nearclose", True)
IPA_CLOSEMID_FRONT_UNROUNDED_VOWEL: Phoneme               = Vowel("e", "front", "closemid", False)
IPA_CLOSEMID_FRONT_ROUNDED_VOWEL: Phoneme                 = Vowel("ø", "front", "closemid", True)
IPA_CLOSEMID_CENTRAL_UNROUNDED_VOWEL: Phoneme             = Vowel("ɘ", "central", "closemid", False)
IPA_CLOSEMID_CENTRAL_ROUNDED_VOWEL: Phoneme               = Vowel("ɵ", "central", "closemid", True)
IPA_CLOSEMID_BACK_UNROUNDED_VOWEL: Phoneme                = Vowel("ɤ", "back", "closemid", False)
IPA_CLOSEMID_BACK_ROUNDED_VOWEL: Phoneme                  = Vowel("o", "back", "closemid", True)
IPA_MID_CENTRAL_VOWEL: Phoneme                            = Vowel("ə", "central", "mid", None)
IPA_OPENMID_FRONT_UNROUNDED_VOWEL: Phoneme                = Vowel("ɛ", "front", "openmid", False)
IPA_OPENMID_FRONT_ROUNDED_VOWEL: Phoneme                  = Vowel("œ", "front", "openmid", True)
IPA_OPENMID_CENTRAL_UNROUNDED_VOWEL: Phoneme              = Vowel("ɜ", "central", "openmid", False)
IPA_OPENMID_CENTRAL_ROUNDED_VOWEL: Phoneme                = Vowel("ɞ", "central", "openmid", True)
IPA_OPENMID_BACK_UNROUNDED_VOWEL: Phoneme                 = Vowel("ʌ", "back", "openmid", False)
IPA_OPENMID_BACK_ROUNDED_VOWEL: Phoneme                   = Vowel("ɔ", "back", "openmid", True)
IPA_NEAROPEN_FRONT_UNROUNDED_VOWEL: Phoneme               = Vowel("æ", "front", "nearopen", False)
IPA_NEAROPEN_CENTRAL_VOWEL: Phoneme                       = Vowel("ɐ", "central", "nearopen", None)
IPA_OPEN_FRONT_UNROUNDED_VOWEL: Phoneme                   = Vowel("a", "front", "open", False)
IPA_OPEN_FRONT_ROUNDED_VOWEL: Phoneme                     = Vowel("ɶ", "front", "open", True)
IPA_OPEN_BACK_UNROUNDED_VOWEL: Phoneme                    = Vowel("ɑ", "back", "open", False)
IPA_OPEN_BACK_ROUNDED_VOWEL: Phoneme                      = Vowel("ɒ", "back", "open", True)

# PULMONIC CONSONANT PLOSIVES
IPA_VOICELESS_BILABIAL_PLOSIVE: Phoneme                   = IPA_Phoneme_PulmonicConsonant("p", "bilabial", "plosive", False)
IPA_VOICED_BILABIAL_PLOSIVE: Phoneme                      = IPA_Phoneme_PulmonicConsonant("b", "bilabial", "plosive", True)
IPA_VOICELESS_ALVEOLAR_PLOSIVE: Phoneme                   = IPA_Phoneme_PulmonicConsonant("t", "alveolar", "plosive", False)
IPA_VOICED_ALVEOLAR_PLOSIVE: Phoneme                      = IPA_Phoneme_PulmonicConsonant("d", "alveolar", "plosive", True)
IPA_VOICELESS_RETROFLEX_PLOSIVE: Phoneme                  = IPA_Phoneme_PulmonicConsonant("ʈ", "retroflex", "plosive", False)
IPA_VOICED_RETROFLEX_PLOSIVE: Phoneme                     = IPA_Phoneme_PulmonicConsonant("ɖ", "retroflex", "plosive", True)
IPA_VOICELESS_PALATAL_PLOSIVE: Phoneme                    = IPA_Phoneme_PulmonicConsonant("c", "palatal", "plosive", False)
IPA_VOICED_PALATAL_PLOSIVE: Phoneme                       = IPA_Phoneme_PulmonicConsonant("ɟ", "palatal", "plosive", True)
IPA_VOICELESS_VELAR_PLOSIVE: Phoneme                      = IPA_Phoneme_PulmonicConsonant("k", "velar", "plosive", False)
IPA_VOICED_VELAR_PLOSIVE: Phoneme                         = IPA_Phoneme_PulmonicConsonant("ɡ", "velar", "plosive", True)
IPA_VOICELESS_UVULAR_PLOSIVE: Phoneme                     = IPA_Phoneme_PulmonicConsonant("q", "velar", "plosive", False)
IPA_VOICED_UVULAR_PLOSIVE: Phoneme                        = IPA_Phoneme_PulmonicConsonant("ɢ", "uvular", "plosive", True)
IPA_VOICELESS_GLOTTAL_PLOSIVE: Phoneme                    = IPA_Phoneme_PulmonicConsonant("ʔ", "glottal", "plosive", True)

# PULMONIC CONSONANT NASALS
IPA_VOICED_BILABIAL_NASAL: Phoneme                        = IPA_Phoneme_PulmonicConsonant("m", "bilabial", "nasal", True)
IPA_VOICED_LABIODENTAL_NASAL: Phoneme                     = IPA_Phoneme_PulmonicConsonant("ɱ", "labiodental", "nasal", True)
IPA_VOICED_ALVEOLAR_NASAL: Phoneme                        = IPA_Phoneme_PulmonicConsonant("n","alveolar", "nasal", True)
IPA_VOICED_RETROFLEX_NASAL: Phoneme                       = IPA_Phoneme_PulmonicConsonant("ɳ", "retroflex", "nasal", True)
IPA_VOICED_PALATAL_NASAL: Phoneme                         = IPA_Phoneme_PulmonicConsonant("ɲ", "palatal", "nasal", True)
IPA_VOICED_VELAR_NASAL: Phoneme                           = IPA_Phoneme_PulmonicConsonant("ŋ", "velar", "nasal", True)
IPA_VOICED_UVULAR_NASAL: Phoneme                          = IPA_Phoneme_PulmonicConsonant("ɴ", "uvular", "nasal", True)

# PULMONIC CONSONANT TRILLS
IPA_VOICED_BILABIAL_TRILL: Phoneme                        = IPA_Phoneme_PulmonicConsonant("ʙ", "bilabial", "trill", True)
IPA_VOICED_ALVEOLAR_TRILL: Phoneme                        = IPA_Phoneme_PulmonicConsonant("r", "alveolar", "trill", True)
IPA_VOICED_UVULAR_TRILL: Phoneme                          = IPA_Phoneme_PulmonicConsonant("ʀ", "uvular", "trill", True)

# PULMONIC CONSONANT TAPS OR FLAPS
IPA_VOICED_LABIODENTAL_TAPFLAP: Phoneme                   = IPA_Phoneme_PulmonicConsonant("ⱱ", "labiodental", "tap/flap", True)
IPA_VOICED_ALVEOLAR_TAPFLAP: Phoneme                      = IPA_Phoneme_PulmonicConsonant("ɾ", "alveolar", "tap/flap", True)
IPA_VOICED_RETROFLEX_TAPFLAP: Phoneme                     = IPA_Phoneme_PulmonicConsonant("ɽ", "retroflex", "tap/flap", True)

# PULMONIC CONSONANT NONSIBILANT FRICATIVES
IPA_VOICELESS_BILABIAL_FRICATIVE: Phoneme                 = IPA_Phoneme_PulmonicConsonant("ɸ", "bilabial", "fricative", False)
IPA_VOICED_BILABIAL_FRICATIVE: Phoneme                    = IPA_Phoneme_PulmonicConsonant("β", "bilabial", "fricative", True)
IPA_VOICELESS_LABIODENTAL_FRICATIVE: Phoneme              = IPA_Phoneme_PulmonicConsonant("f", "labiodental", "fricative", False)
IPA_VOICED_LABIODENTAL_FRICATIVE: Phoneme                 = IPA_Phoneme_PulmonicConsonant("v", "labiodental", "fricative", True)
IPA_VOICELESS_DENTAL_FRICATIVE: Phoneme                   = IPA_Phoneme_PulmonicConsonant("θ", "dental", "fricative", False)
IPA_VOICED_DENTAL_FRICATIVE: Phoneme                      = IPA_Phoneme_PulmonicConsonant("ð", "dental", "fricative", True)
IPA_VOICELESS_ALVEOLAR_FRICATIVE: Phoneme                 = IPA_Phoneme_PulmonicConsonant("s", "alveolar", "fricative", False)
IPA_VOICED_ALVEOLAR_FRICATIVE: Phoneme                    = IPA_Phoneme_PulmonicConsonant("z", "alveolar", "fricative", True)
IPA_VOICELESS_POSTALVEOLAR_FRICATIVE: Phoneme             = IPA_Phoneme_PulmonicConsonant("ʃ", "postalveolar", "fricative", False)
IPA_VOICED_POSTALVEOLAR_FRICATIVE: Phoneme                = IPA_Phoneme_PulmonicConsonant("ʒ", "postalveolar", "fricative", True)
IPA_VOICELESS_RETROFLEX_FRICATIVE: Phoneme                = IPA_Phoneme_PulmonicConsonant("ʂ", "retroflex", "fricative", False)
IPA_VOICED_RETROFLEX_FRICATIVE: Phoneme                   = IPA_Phoneme_PulmonicConsonant("ʐ", "retroflex", "fricative", True)
IPA_VOICELESS_PALATAL_FRICATIVE: Phoneme                  = IPA_Phoneme_PulmonicConsonant("ç", "palatal", "fricative", False)
IPA_VOICED_PALATAL_FRICATIVE: Phoneme                     = IPA_Phoneme_PulmonicConsonant("ʝ", "palatal", "fricative", True)
IPA_VOICELESS_VELAR_FRICATIVE: Phoneme                    = IPA_Phoneme_PulmonicConsonant("x", "velar", "fricative", False)
IPA_VOICED_VELAR_FRICATIVE: Phoneme                       = IPA_Phoneme_PulmonicConsonant("ɣ", "velar", "fricative", True)
IPA_VOICELESS_UVULAR_FRICATIVE: Phoneme                   = IPA_Phoneme_PulmonicConsonant("χ", "uvular", "fricative", False)
IPA_VOICED_UVULAR_FRICATIVE: Phoneme                      = IPA_Phoneme_PulmonicConsonant("ʁ", "uvular", "fricative", True)
IPA_VOICELESS_EPIGLOTTAL_FRICATIVE: Phoneme               = IPA_Phoneme_PulmonicConsonant("ħ", "pharyngeal", "fricative", False)
IPA_VOICED_EPIGLOTTAL_FRICATIVE: Phoneme                  = IPA_Phoneme_PulmonicConsonant("ʕ", "pharyngeal", "fricative", True)
IPA_VOICELESS_GLOTTAL_FRICATIVE: Phoneme                  = IPA_Phoneme_PulmonicConsonant("h", "glottal", "fricative", False)
IPA_VOICED_GLOTTAL_FRICATIVE: Phoneme                     = IPA_Phoneme_PulmonicConsonant("ɦ", "glottal", "fricative", True)

# PULMONIC CONSONANT LATERAL FRICATIVES
IPA_VOICELESS_ALVEOLAR_LATERALFRICATIVE: Phoneme          = IPA_Phoneme_PulmonicConsonant("ɬ", "alveolar", "lateral fricative", False)
IPA_VOICED_ALVEOLAR_LATERALFRICATIVE: Phoneme             = IPA_Phoneme_PulmonicConsonant("ɮ", "alveolar", "lateral fricative", True)

# PULMONIC CONSONANT APPROXIMANTS
IPA_VOICED_LABIODENTAL_APPROXIMANT: Phoneme               = IPA_Phoneme_PulmonicConsonant("ʋ", "labiodental", "approximant", True)
IPA_VOICED_ALVEOLAR_APPROXIMANT: Phoneme                  = IPA_Phoneme_PulmonicConsonant("ɹ", "alveolar", "approximant", True)
IPA_VOICED_RETROFLEX_APPROXIMANT: Phoneme                 = IPA_Phoneme_PulmonicConsonant("ɻ", "retroflex", "approximant", True)
IPA_VOICED_PALATAL_APPROXIMANT: Phoneme                   = IPA_Phoneme_PulmonicConsonant("j", "palatal", "approximant", True)
IPA_VOICED_VELAR_APPROXIMANT: Phoneme                     = IPA_Phoneme_PulmonicConsonant("ɰ", "velar", "approximant", True)

# PULMONIC CONSONANT LATERAL APPROXIMANTS
IPA_VOICED_ALVEOLAR_LATERALAPPROXIMANT: Phoneme           = IPA_Phoneme_PulmonicConsonant("l", "alveolar", "lateral approximant", True)
IPA_VOICED_RETROFLEX_LATERALAPPROXIMANT: Phoneme          = IPA_Phoneme_PulmonicConsonant("ɭ", "retroflex", "lateral approximant", True)
IPA_VOICED_PALATAL_LATERALAPPROXIMANT: Phoneme            = IPA_Phoneme_PulmonicConsonant("ʎ", "palatal", "lateral approximant", True)
IPA_VOICED_VELAR_LATERALAPPROXIMANT: Phoneme              = IPA_Phoneme_PulmonicConsonant("ʟ", "velar", "lateral approximant", True)