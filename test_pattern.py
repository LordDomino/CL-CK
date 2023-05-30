from clck.phonemes import *
from clck.phonology import PhonologicalInventory



inventory: PhonologicalInventory = PhonologicalInventory(
    IPA_VOICELESS_BILABIAL_PLOSIVE,
    IPA_VOICELESS_ALVEOLAR_PLOSIVE,
    IPA_VOICELESS_VELAR_PLOSIVE,
    IPA_VOICED_BILABIAL_NASAL,
    IPA_VOICED_ALVEOLAR_NASAL,
    IPA_VOICELESS_ALVEOLAR_FRICATIVE,
    IPA_VOICED_ALVEOLAR_LATERALAPPROXIMANT,
    IPA_CLOSE_FRONT_UNROUNDED_VOWEL
)

for phoneme in inventory.phonemes:
    print(phoneme.get_name())