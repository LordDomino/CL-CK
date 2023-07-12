
from clck.ipa_phonemes import IPA_VOICELESS_DENTAL_FRICATIVE
from clck.fundamentals.phonemes import DummyPhoneme
from clck.phonology.structure_evaluator import StructureEvaluator
from clck.phonology.syllabics import Onset


StructureEvaluator(Onset(IPA_VOICELESS_DENTAL_FRICATIVE, DummyPhoneme(), DummyPhoneme()))