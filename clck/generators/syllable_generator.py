import random

from ..phonology.phonotactics import ClusterConstraint, PhonemicConstraint, Phonotactics

from ..phonology.syllables import Syllable, SyllableShape
from ..phonology.phonemes import Consonant, Phoneme, PhonologicalInventory, Vowel


class SyllableGenerator:
    def __init__(self,
                 bank: PhonologicalInventory,
                 shape: SyllableShape,
                 phonemic_constraints: list[PhonemicConstraint],
                 cluster_constraints: list[ClusterConstraint]) -> None:
        self._bank: PhonologicalInventory = bank
        self._shape: SyllableShape = shape
        self._phonemic_constraints: list[PhonemicConstraint] = phonemic_constraints
        self._cluster_constriants: list[ClusterConstraint] = cluster_constraints
        self._bank_consonants: tuple[Consonant] = self._bank.consonants
        self._bank_vowels: tuple[Vowel] = self._bank.vowels

        # Internal variables
        self._recent_generation: list[Syllable] = []


    @classmethod
    def from_phonotactics(cls,
                          bank: PhonologicalInventory,
                          phonotactics: Phonotactics) -> "SyllableGenerator":
        return SyllableGenerator(bank,
                                 phonotactics.syllable_shape,
                                 phonotactics.phonemic_constraints,
                                 phonotactics.cluster_constraints)
    
    def generate(self, size: int = 1) -> list[Syllable]:
        generation: list[Syllable] = []
        for _ in range(size):
            phoneme_list: list[Phoneme] = []
            for type in self._shape.pattern:
                phoneme: Consonant | Vowel
                if type.upper() == "C":
                    phoneme = random.choice(self._bank_consonants)
                else:
                    phoneme = random.choice(self._bank_vowels)
                phoneme_list.append(phoneme)
            generation.append(Syllable(*phoneme_list))
        self._recent_generation = generation
        return generation
    

    def get_recent_generation(self) -> list[Syllable]:
        return self._recent_generation