from clck.phonology.phonotactics import ClusterConstraint, ForbidPhonemeRule, Phonotactics
from clck.phonology.syllables import Coda, Onset, SyllableShape
from clck.generators.syllable_generator import SyllableGenerator
from clck.phonemes import *
from clck.phonology.phonemes import Cluster, PhonologicalInventory



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
    SyllableShape("C", "VV", "CC"),
    [ForbidPhonemeRule([Onset, Coda], [IPA_VOICELESS_BILABIAL_PLOSIVE])],
    [ClusterConstraint(1, [Coda], [Cluster(IPA_CLOSE_BACK_ROUNDED_VOWEL)])]
)

generator: SyllableGenerator = SyllableGenerator.from_phonotactics(inventory, ph)
generator.generate(50)

for syllable in generator.get_recent_generation():
    print(syllable, syllable.phonemes)