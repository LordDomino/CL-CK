import random
from typing import Sequence

from ..language.language import Language
from ..phonology.containers import PhonologicalInventory
from ..phonology.phonemes import Consonant, Phoneme, Vowel
from ..phonology.phonotactics import (
    ClusterConstraint,
    PhonemicConstraint,
    PhonotacticRule,
    Phonotactics
)
from ..phonology.syllabics import Syllable
from ..phonology.syllabics import Coda, Nucleus, Onset, SyllabicComponent, SyllableShape



class SyllableGenerator:
    def __init__(self,
            language: Language,
            bank: PhonologicalInventory,
            shape: SyllableShape,
            phonemic_constraints: list[PhonemicConstraint],
            cluster_constraints: list[ClusterConstraint]) -> None:
        self._language: Language = language
        self._init_language()
        self._bank: PhonologicalInventory = bank
        self._shape: SyllableShape = shape
        self._phonemic_constraints: list[PhonemicConstraint] = phonemic_constraints
        self._cluster_constraints: list[ClusterConstraint] = cluster_constraints
        self._phonotactics: Phonotactics = Phonotactics(
            self._shape,
            self._phonemic_constraints,
            self._cluster_constraints
        )
        self._bank_consonants: tuple[Consonant] = self._bank.consonants
        self._bank_vowels: tuple[Vowel] = self._bank.vowels

        # Internal variables
        self._recent_generation: list[Syllable] = []


    @classmethod
    def from_phonotactics(cls,
        language: Language,
        bank: PhonologicalInventory,
        phonotactics: Phonotactics) -> "SyllableGenerator":
        """
        Creates a `SyllableGenerator` object from a wrapped `Phonotactics`
        object of the constraints.
        """
        return SyllableGenerator(language,
            bank,
            phonotactics.syllable_shape,
            phonotactics.phonemic_constraints,
            phonotactics.cluster_constraints)


    def generate(self, size: int = 1) -> list[Syllable]:
        syllable: list[Syllable] = []
        for _ in range(size):
            syllable.append(self._generate_single())
        self._recent_generation = syllable
        self._language.register_structures(*syllable)
        return syllable


    def get_recent_generation(self) -> list[Syllable]:
        return self._recent_generation
    

    def _does_violate_rule(self, component: SyllabicComponent) -> bool:
        rules: Sequence[PhonotacticRule] = self._phonotactics.rules
        component_type = component.__class__
        applicable_rules: Sequence[PhonotacticRule] = []

        for rule in rules:
            for location in rule.valid_locations:
                if component_type == location:
                    applicable_rules.append(rule)

        for rule in applicable_rules:
            if component_type in (Onset, Nucleus, Coda):
                for phoneme in component.components:
                    if isinstance(phoneme, Phoneme):
                        if rule.execute_rule(phoneme) is False:
                            return True
        
        return False


    def _generate_single(self) -> Syllable:
        # Generate a random onset
        onset: Onset = self._generate_onset(len(self._shape.onset_shape))

        # Validate if generated onset is permissible
        while self._does_violate_rule(onset):
            onset = self._generate_onset(len(self._shape.onset_shape))
            if self._does_violate_rule(onset) is False:
                break

        nucleus: Nucleus = self._generate_nucleus(len(self._shape.nucleus_shape))

        # Validate if generated nucleus is permissible
        while self._does_violate_rule(nucleus):
            nucleus = self._generate_nucleus(len(self._shape.nucleus_shape))
            if self._does_violate_rule(nucleus) is False:
                break

        coda: Coda = self._generate_coda(len(self._shape.coda_shape))

        # Validate if generated coda is permissible
        while self._does_violate_rule(coda):
            coda = self._generate_coda(len(self._shape.coda_shape))
            if self._does_violate_rule(coda) is False:
                break

        onset.remove_duplicates()
        nucleus.remove_duplicates()
        coda.remove_duplicates()

        return Syllable(onset, nucleus, coda)
    

    def _generate_coda(self, size: int) -> Coda:
        phonemes: list[Consonant] = []
        for _ in range(size):
            choice: Consonant = random.choice(self._bank.consonants)
            phonemes.append(choice)
        return Coda(*phonemes)
    

    def _generate_nucleus(self, size: int) -> Nucleus:
        phonemes: list[Vowel] = []
        for _ in range(size):
            choice: Vowel = random.choice(self._bank.vowels)
            phonemes.append(choice)
        return Nucleus(*phonemes)


    def _generate_onset(self, size: int) -> Onset:
        # shape: SyllableShape = self._shape
        # onset_shape: str = shape.onset_shape
        phonemes: list[Consonant] = []
        for _ in range(size):
            choice: Consonant = random.choice(self._bank.consonants)
            phonemes.append(choice)
        return Onset(*phonemes)


    def _init_language(self) -> None:
        self._language._syllable_generator = self # type: ignore