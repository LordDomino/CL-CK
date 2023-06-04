from clck import *
from clck.generators.syllable_generator import SyllableGenerator
from clck.phonology.containers import PhonologicalInventory
from clck.phonology.structures import *



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

ons = Onset(IPA_VOICED_ALVEOLAR_PLOSIVE)
nuc = Nucleus(IPA_CLOSE_BACK_UNROUNDED_VOWEL)
cod = Coda(IPA_VOICED_ALVEOLAR_LATERALFRICATIVE)
rhy = Rhyme(nuc, cod)

s: Syllable = Syllable.from_onset_and_rhyme(ons, rhy)

print(s.find_phonemes(NonpulmonicConsonant))