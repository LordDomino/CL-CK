from clck.ipa.IPA import *
from clck.generators.generators import SyllableGenerator
from clck.language.language import Language
from clck.fundamentals.phonology import PhonemicInventory
from clck.phonology.phonotactics import PhonotacticRule
from clck.phonology.phonotactics2 import Phonotactics
from clck.phonology.syllabics import (
    CodaShape,
    NucleusShape,
    OnsetShape,
    Syllable,
    SyllableStructure
)


inventory: PhonemicInventory = PhonemicInventory(
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

ph = Phonotactics((PhonotacticRule(),))

lang = Language(inventory)

generator: SyllableGenerator = SyllableGenerator.from_phonotactics(
    lang,
    inventory,
    SyllableStructure(
        OnsetShape("CC"),
        NucleusShape("V"),
        CodaShape("CC")
    ),
    ph
)

generator.generate(1)

syllable: Syllable = generator.get_recent_generation()[0]

print(syllable)