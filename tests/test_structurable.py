from clck.common.structure import Structure
from clck.phonology.phonemes import DummyPhoneme


s = Structure(DummyPhoneme())
s.components
print(s.blueprint.elements)