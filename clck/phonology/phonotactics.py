from abc import abstractmethod
from typing import Sequence, Type

from .containers import *
from .phonemes import Phoneme
from .syllables import SyllableComponent, SyllableShape



__all__: list[str] = [
    "Phonotactics",
    "PhonotacticRule",
    "PhonemicConstraint",
    "ClusterConstraint",
    "ForbidPhonemeRule"
]



class Phonotactics:
    def __init__(self, syllable_shape: SyllableShape,
            phonemic_constraints: Sequence["PhonemicConstraint"],
            cluster_constraints: Sequence["ClusterConstraint"]) -> None:
        self._syllable_shape: SyllableShape = syllable_shape
        self._phonemic_constraints: Sequence[PhonemicConstraint] = phonemic_constraints
        self._cluster_constraints: Sequence[ClusterConstraint] = cluster_constraints
        self._rules: Sequence[PhonotacticRule] = (
            list(self._phonemic_constraints)
            + list(self._cluster_constraints)
        )


    @property
    def syllable_shape(self) -> SyllableShape:
        return self._syllable_shape
    

    @property
    def phonemic_constraints(self) -> list["PhonemicConstraint"]:
        return list(self._phonemic_constraints)
    

    @property
    def cluster_constraints(self) -> list["ClusterConstraint"]:
        return list(self._cluster_constraints)
        

    @property
    def rules(self) -> Sequence["PhonotacticRule"]:
        return self._rules


class PhonotacticRule:
    def __init__(self, priority: int, valid_locations: list[Type[SyllableComponent]]) -> None:
        self._priority: int = priority
        self._valid_locations: list[Type[SyllableComponent]] = valid_locations


    @property
    def priority(self) -> int:
        return self._priority
    

    @property
    def valid_locations(self) -> list[Type[SyllableComponent]]:
        return self._valid_locations
    

    @abstractmethod
    def execute_rule(self, component: Phoneme) -> bool: ...


class PhonemicConstraint(PhonotacticRule):
    def __init__(self, priority: int,
            valid_locations: list[Type[SyllableComponent]],
            phonemes: list[Phoneme]) -> None:
        super().__init__(priority, valid_locations)
        self._phonemes: list[Phoneme] = phonemes


class ClusterConstraint(PhonotacticRule):
    def __init__(self, priority: int,
            valid_locations: list[Type[SyllableComponent]],
            clusters: list[Cluster]) -> None:
        super().__init__(priority, valid_locations)



class ForbidPhonemeRule(PhonemicConstraint):
    def __init__(self, valid_locations: list[Type[SyllableComponent]],
                 phonemes: list[Phoneme]) -> None:
        super().__init__(1, valid_locations, phonemes)

    
    def execute_rule(self, component: Phoneme) -> bool:
        """
        Returns True if the given phoneme is not on the blacklist of
        phonemes."""
        if component in self._phonemes:
            return False
        else:
            return True