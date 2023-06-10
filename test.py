from clck.generators.generators import SyllableGenerator
from clck.ipa_phonemes import *
from clck.language.language import Language
from clck.phonology.containers import PhonologicalInventory
from clck.phonology.phonemes import Consonant
from clck.phonology.phonotactics import ForbidPhonemeRule, Phonotactics
from clck.phonology.syllabics import Coda, CodaShape, NucleusShape, Onset, OnsetShape, Rhyme, SyllableShape, VowelCluster


inventory: PhonologicalInventory = PhonologicalInventory(
    # Consonants
    IPA_VOICELESS_BILABIAL_PLOSIVE,
    IPA_VOICELESS_ALVEOLAR_PLOSIVE,
    IPA_VOICELESS_VELAR_PLOSIVE,
    IPA_VOICED_BILABIAL_NASAL,
    IPA_VOICED_ALVEOLAR_NASAL,
    IPA_VOICELESS_ALVEOLAR_FRICATIVE,
    IPA_VOICED_ALVEOLAR_LATERALAPPROXIMANT,

    # Vowels
    IPA_CLOSE_FRONT_UNROUNDED_VOWEL,
    IPA_CLOSEMID_FRONT_UNROUNDED_VOWEL,
    IPA_OPEN_FRONT_UNROUNDED_VOWEL,
    IPA_CLOSEMID_BACK_ROUNDED_VOWEL,
    IPA_CLOSE_BACK_ROUNDED_VOWEL
)

ph = Phonotactics(
    SyllableShape(
        OnsetShape("C"),
        NucleusShape("VV"),
        CodaShape("C")
    ),
    [ForbidPhonemeRule([Onset, Coda], [IPA_VOICELESS_BILABIAL_PLOSIVE])],
    []
)

lang = Language(inventory)

generator: SyllableGenerator = SyllableGenerator.from_phonotactics(lang, inventory, ph)
generator.generate(100)

for g in generator.get_recent_generation():
    print(g, g.components)