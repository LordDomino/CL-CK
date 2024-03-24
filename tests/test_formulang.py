from clck.common.component import ComponentBlueprint
from clck.common.structure import Structure
from clck.formulang.common import Formulang
from clck.ipa.IPA import IPA_VOICED_ALVEOLAR_PLOSIVE
from clck.phonology.phonemes import DummyPhoneme

s = Structure(
    (IPA_VOICED_ALVEOLAR_PLOSIVE,),
    _bp=ComponentBlueprint(DummyPhoneme, DummyPhoneme(), DummyPhoneme)
)

s2 = Formulang.generate("abc")

print(s2.base_phone)