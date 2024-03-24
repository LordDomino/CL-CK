from clck.common.structure import Structure
from clck.phonetics.phones import DummyPhone
from clck.phonology.phonemes import DummyPhoneme, Phoneme
from clck.phonology.syllabics import Onset, Syllable


structure = Structure((Syllable((Phoneme(DummyPhone()), DummyPhoneme(), DummyPhoneme(), DummyPhoneme())),
    DummyPhoneme(),
    Onset((DummyPhoneme(),)),
    Structure((Phoneme(DummyPhone()), DummyPhoneme()))))