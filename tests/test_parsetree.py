from clck.formulang.parsing.parse_tree import PhonemeNode, TreeNode
from clck.phonology.phonemes import DummyPhoneme
from clck.phonology.syllabics import Syllable


t = TreeNode((DummyPhoneme(),), 1)
a = t._subnodes