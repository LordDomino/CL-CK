from clck.fundamentals.phonemes import DummyPhoneme
from clck.ipa_phonemes import DUMMY_PHONEME, IPA_VOICELESS_DENTAL_FRICATIVE
from clck.phonology.structure_evaluator import StructureEvaluator
from clck.phonology.syllabics import *


evaluator = StructureEvaluator(Coda(IPA_VOICELESS_DENTAL_FRICATIVE, IPA_VOICELESS_DENTAL_FRICATIVE, DUMMY_PHONEME, DummyPhoneme()))

print(evaluator.structure)