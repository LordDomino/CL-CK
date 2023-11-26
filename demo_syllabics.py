from clck.IPA import IPA_VOICED_BILABIAL_PLOSIVE, IPA_VOICED_GLOTTAL_PLOSIVE, IPA_VOICELESS_ALVEOLAR_NASAL
from clck.fundamentals.phonology import DummyConsonant, DummyVowel, PhonemicInventory
from clck.fundamentals.syllabics import Coda, Nucleus, Onset, Syllable
from clck.generators.generators import SyllableGenerator


syllable = Syllable(
    Onset(DummyConsonant(), DummyConsonant()),
    Nucleus(DummyVowel()),
    Coda(IPA_VOICED_GLOTTAL_PLOSIVE)
)

generator = SyllableGenerator(PhonemicInventory(
    IPA_VOICED_GLOTTAL_PLOSIVE,
    IPA_VOICED_BILABIAL_PLOSIVE,
    IPA_VOICELESS_ALVEOLAR_NASAL
    ))

print(generator.generate("(C)(C)(C)", 1))