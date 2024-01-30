from clck.common.component import ComponentBlueprint
from clck.common.structure import Structure
from clck.phonology.phonemes import DummyPhoneme, VowelPhoneme
from clck.phonology.syllabics import Nucleus, Syllable

s = Structure(
    (
        DummyPhoneme(), Structure(
            (
                DummyPhoneme(),
            )
        ), DummyPhoneme()
    ),
    _bp=ComponentBlueprint(DummyPhoneme, DummyPhoneme(), DummyPhoneme)
)
print(s)