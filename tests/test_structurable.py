from clck.formulang.common import Formulang
from clck.formulang.parsing.parse_tree import TreeNode
from clck.phonology.phonemes import DummyPhoneme
from clck.phonology.syllabics import Nucleus, Syllable


syl = Syllable((DummyPhoneme(), Nucleus(DummyPhoneme())))
syl.components