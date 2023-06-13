from .articulation import *

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

# # Broad places of articulation for pulmonic consonants
# LABIAL              = Place("labial", (1, 3))
# CORONAL             = Place("coronal", (4, 9))
# DORSAL              = Place("dorsal", (10, 12))
# LARYNGEAL           = Place("laryngeal", (13, 14))

# Specific places of articulation for pulmonic consonants, defined in the IPA chart
BILABIAL = Place("bilabial", 1)
LABIODENTAL = Place("labiodental", 2)
LINGUOLABIAL = Place("linguolabial", (3, 4)) # this is not an official IPA place of articulation
DENTAL = Place("dental", 5)
ALVEOLAR = Place("alveolar", 6)
POSTALVEOLAR = Place("postalveolar", 7)
RETROFLEX = Place("retroflex", 8)
PALATAL = Place("palatal", (9, 10))
VELAR = Place("velar", 11)
UVULAR = Place("uvular", 12)
PHARYNGEAL = Place("pharyngeal", 13)
GLOTTAL = Place("glottal", 14)

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
CLOSE = Height("close", 0)
NEARCLOSE = Height("near-close", 1)
CLOSEMID = Height("close-mid", 2)
MID = Height("mid", 3)
OPENMID = Height("open-mid", 4)
NEAROPEN = Height("near-open", 5)
OPEN = Height("open", 6)

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