from typing import Type

from clck.phonology.phonemes import Phoneme
from .phonemes import Cluster, Phoneme

from clck.phonology.syllables import SyllableComponent
from .syllables import SyllableComponent, SyllableShape


class Phonotactics:
    def __init__(self,
                 syllable_shape: SyllableShape,
                 phonemic_constraints: list["PhonemicConstraint"],
                 cluster_constraints: list["ClusterConstraint"]) -> None:
        self._syllable_shape: SyllableShape = syllable_shape
        self._phonemic_constraints: list[PhonemicConstraint] = phonemic_constraints
        self._cluster_constraints: list[ClusterConstraint] = cluster_constraints


    @property
    def syllable_shape(self) -> SyllableShape:
        return self._syllable_shape
    

    @property
    def phonemic_constraints(self) -> list["PhonemicConstraint"]:
        return self._phonemic_constraints
    

    @property
    def cluster_constraints(self) -> list["ClusterConstraint"]:
        return self._cluster_constraints
        


class PhonotacticRule:
    def __init__(self, priority: int, valid_locations: list[Type[SyllableComponent]]) -> None:
        self._priority: int = priority
        self._valid_locations: list[Type[SyllableComponent]] = valid_locations



class PhonemicConstraint(PhonotacticRule):
    def __init__(self, priority: int,
                 valid_locations: list[Type[SyllableComponent]],
                 phonemes: list[Phoneme]) -> None:
        super().__init__(priority, valid_locations)



class ClusterConstraint(PhonotacticRule):
    def __init__(self, priority: int,
                 valid_locations: list[Type[SyllableComponent]],
                 clusters: list[Cluster]) -> None:
        super().__init__(priority, valid_locations)



class ForbidPhonemeRule(PhonemicConstraint):
    def __init__(self, valid_locations: list[Type[SyllableComponent]],
                 phonemes: list[Phoneme]) -> None:
        super().__init__(1, valid_locations, phonemes)