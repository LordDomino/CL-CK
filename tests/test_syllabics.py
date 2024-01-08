from clck.ipa.IPA import IPA_VOICED_BILABIAL_PLOSIVE, IPA_VOICED_GLOTTAL_PLOSIVE, IPA_VOICED_ALVEOLAR_NASAL
from clck.phonology.phonemes import DummyConsonantPhoneme, DummyVowelPhoneme, PhonemicInventory
from clck.phonology.syllabics import Coda, Nucleus, Onset, Syllable
from clck.language.generators import SyllableGenerator


syllable = Syllable(
    Onset(DummyConsonantPhoneme(), DummyConsonantPhoneme()),
    Nucleus(DummyVowelPhoneme()),
    Coda(IPA_VOICED_GLOTTAL_PLOSIVE)
)

generator = SyllableGenerator(PhonemicInventory(
    IPA_VOICED_GLOTTAL_PLOSIVE,
    IPA_VOICED_BILABIAL_PLOSIVE,
    IPA_VOICED_ALVEOLAR_NASAL
))

print(generator.generate("(C)(C)(C)", 1))