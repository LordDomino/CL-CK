import random
from typing import List

from ..config import printwarning

from ..language.language import Language
from ..phonology.containers import PhonologicalInventory
from ..phonology.phonemes import Consonant, Vowel
from ..phonology.phonotactics import (
    PhonemicConstraint,
    Phonotactics
)
from ..phonology.syllabics import Coda, CodaShape, Nucleus, NucleusShape, Onset, OnsetShape, SyllabicComponent, Syllable, SyllableShape



class SyllableGenerator:
    def __init__(self,
            language: Language,
            bank: PhonologicalInventory,
            shape: SyllableShape,
            phonemic_constraints: list[PhonemicConstraint]
            ) -> None:
        self._language: Language = language
        self._init_language()
        self._bank: PhonologicalInventory = bank
        self._shape: SyllableShape = shape
        self._phonemic_constraints: list[PhonemicConstraint] = phonemic_constraints

        # Internal variables
        self._recent_generation: list[Syllable] = []

    @classmethod
    def from_phonotactics(cls,
        language: Language,
        bank: PhonologicalInventory,
        shape: SyllableShape,
        phonotactics: Phonotactics) -> "SyllableGenerator":
        """
        Creates a `SyllableGenerator` object from a wrapped `Phonotactics`
        object of the constraints.
        """
        return SyllableGenerator(language,
            bank,
            shape,
            phonotactics.phonemic_constraints)

    def generate(self, size: int = 1, register_to_lang: bool = True) -> tuple[Syllable]:
        syllables: List[Syllable] = []
        
        for _ in range(size):
            syllables.append(self._generate_single())
        self._recent_generation = syllables
        
        if register_to_lang:
            self._language.register_structures(*syllables)
        
        return tuple(syllables)

    def get_recent_generation(self) -> list[Syllable]:
        return self._recent_generation
    

    # def _does_violate_rule(self, component: SyllabicComponent) -> bool:
    #     rules: Sequence[PhonotacticRule] = self._phonotactics.rules
    #     component_type = component.__class__
    #     applicable_rules: Sequence[PhonotacticRule] = []

    #     for rule in rules:
    #         for location in rule.valid_locations:
    #             if component_type == location:
    #                 applicable_rules.append(rule)

    #     for rule in applicable_rules:
    #         if component_type in (Onset, Nucleus, Coda):
    #             for phoneme in component.components:
    #                 if isinstance(phoneme, Phoneme):
    #                     if rule.execute_rule(phoneme) is False:
    #                         return True
        
    #     return False

    def _generate_single(self) -> Syllable:
        syllable: list[SyllabicComponent] = []

        onset: Onset | None

        if self._shape.onset_shape is not None:
            # Generate a random onset
            onset = self._generate_onset(self._shape.onset_shape)
            onset._components = onset.remove_component_duplicates(onset._components)
            syllable.append(onset)
        else:
            onset = None

        # Validate if generated onset is permissible
        # while self._does_violate_rule(onset):
        #     onset = self._generate_onset(self._shape.onset_shape)
        #     if self._does_violate_rule(onset) is False:
        #         break

        nucleus: Nucleus = self._generate_nucleus(self._shape.nucleus_shape)
        nucleus._components = nucleus.remove_component_duplicates(nucleus._components)

        # Validate if generated nucleus is permissible
        # while self._does_violate_rule(nucleus):
        #     nucleus = self._generate_nucleus(self._shape.nucleus_shape)
        #     if self._does_violate_rule(nucleus) is False:
        #         break

        if self._shape.coda_shape is not None:
            coda = self._generate_coda(self._shape.coda_shape)
            coda._components = coda.remove_component_duplicates(coda._components)
        else:
            coda = None

        # Validate if generated coda is permissible
        # while self._does_violate_rule(coda):
        #     coda = self._generate_coda(self._shape.coda_shape)
        #     if self._does_violate_rule(coda) is False:
        #         break

        return Syllable(onset, nucleus, coda)
    
    def _generate_coda(self, shape: CodaShape) -> Coda:
        phonemes: list[Consonant] = []

        # Traverse through each pattern label in the pattern
        for group in shape.pattern.phoneme_groups:
            broad_bank = self._bank.consonants

            # Get the actual bank of phonemes
            bank = list(set(broad_bank) & set(group.phonemes))
            choice: Consonant = random.choice(bank)
            phonemes.append(choice)

        return Coda(*phonemes)
    
    def _generate_nucleus(self, shape: NucleusShape) -> Nucleus:
        phonemes: list[Vowel] = []

        # Traverse through each pattern label in the pattern
        for group in shape.pattern.phoneme_groups:
            broad_bank = self._bank.vowels

            # Get the actual bank of phonemes
            bank = list(set(broad_bank) & set(group.phonemes))
            choice: Vowel = random.choice(bank)
            phonemes.append(choice)

        return Nucleus(*phonemes)

    def _generate_onset(self, shape: OnsetShape) -> Onset:
        phonemes: list[Consonant] = []

        # Traverse through each pattern label in the pattern
        for group in shape.pattern.phoneme_groups:
            broad_bank = self._bank.consonants

            # Get the actual bank of phonemes
            bank = list(set(broad_bank) & set(group.phonemes))
            if bank == []:
                printwarning(f"No phoneme from phoneme group \"{group.label}\" "
                    f"(based on pattern \"{self._shape.pattern_string}\") was "
                    f"generated. The current phonological inventory provides "
                    f"no existing phoneme/s of such type.")
            else:
                choice: Consonant = random.choice(bank)
                phonemes.append(choice)

        return Onset(*phonemes)

    def _init_language(self) -> None:
        self._language._syllable_generator = self # type: ignore