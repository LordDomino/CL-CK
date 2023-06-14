from clck.ipa_phonemes import IPA_VOICED_BILABIAL_FRICATIVE
from clck.phonology.syllabics import Onset
from clck.phonology.phonotactics import BEFORE, OCCUR, PositionalRule


print(PositionalRule(None, 10.5, OCCUR, BEFORE).execute(None, None))
print(PositionalRule(None, 10.5, OCCUR, BEFORE).execute(None, (Onset(IPA_VOICED_BILABIAL_FRICATIVE),)))
print(PositionalRule(None, 10.5, OCCUR, BEFORE).execute(None, (Onset(IPA_VOICED_BILABIAL_FRICATIVE),), True))