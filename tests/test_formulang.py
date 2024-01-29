from clck.common.component import Component, ComponentBlueprint
from clck.common.structure import Structure
from clck.phonology.phonemes import DummyPhoneme, VowelPhoneme

s = Structure((DummyPhoneme(), DummyPhoneme()), _bp=ComponentBlueprint(Component, VowelPhoneme))