from clck.IPA import IPA_VOICELESS_LABIODENTAL_TAP
from clck.fundamentals.phonetics import PulmonicConsonant
from clck.fundamentals.phonology import Phoneme
from clck.phonology.articulatory_properties import MannerOfArticulation, Phonation, PlaceOfArticulation

# Attribute equivalence checking between two different instances that 
# contain the same attributes
if IPA_VOICELESS_LABIODENTAL_TAP == Phoneme(PulmonicConsonant("p", PlaceOfArticulation.LABIODENTAL, MannerOfArticulation.FLAP, Phonation.VOICELESS, (), True)):
    print("==")