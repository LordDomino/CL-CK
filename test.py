from clck.generators.syllable_generator import SyllableGenerator
from clck import *
from clck.phonology.containers import *



inventory: PhonologicalInventory = PhonologicalInventory(
    IPA_VOICELESS_BILABIAL_PLOSIVE,
    IPA_VOICELESS_ALVEOLAR_PLOSIVE,
    IPA_VOICELESS_VELAR_PLOSIVE,
    IPA_VOICED_BILABIAL_NASAL,
    IPA_VOICED_ALVEOLAR_NASAL,
    IPA_VOICELESS_ALVEOLAR_FRICATIVE,
    IPA_VOICED_ALVEOLAR_LATERALAPPROXIMANT,
    IPA_CLOSE_FRONT_UNROUNDED_VOWEL,
    IPA_CLOSEMID_FRONT_UNROUNDED_VOWEL,
    IPA_OPEN_FRONT_UNROUNDED_VOWEL,
    IPA_CLOSEMID_BACK_ROUNDED_VOWEL,
    IPA_CLOSE_BACK_ROUNDED_VOWEL
)

ph = Phonotactics(
    SyllableShape("C", "V", "C"),
    [ForbidPhonemeRule([Onset, Coda], [IPA_VOICELESS_BILABIAL_PLOSIVE])],
    []
)

generator: SyllableGenerator = SyllableGenerator.from_phonotactics(inventory, ph)
generator.generate(5)

for gen in generator.get_recent_generation():
    print(gen.phonemes)