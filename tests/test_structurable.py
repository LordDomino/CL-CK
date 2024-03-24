from clck.phonology.phonemes import DummyPhoneme
from clck.phonology.syllabics import Nucleus, Syllable


syl = Syllable((DummyPhoneme(), Nucleus((DummyPhoneme(),))))
syl.components