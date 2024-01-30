from clck.ipa.IPA import IPA_VOICED_ALVEOLAR_NASAL
from clck.phonology.phonemes import DummyPhoneme
from clck.phonology.syllabics import Coda, Nucleus, Rime, Syllable


s = Syllable((IPA_VOICED_ALVEOLAR_NASAL, Rime(Nucleus(DummyPhoneme()), Coda(DummyPhoneme()))))
s.components
print(s.blueprint.elements)

a = tuple((((((1 , 4), (5, 5))))))