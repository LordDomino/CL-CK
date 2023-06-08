from abc import abstractmethod
from typing import Sequence, Type

from .structures import *
from .phonemes import Phoneme
from .syllabics import PhonemeCluster, SyllabicComponent, SyllableShape


__all__: list[str] = [
    "Phonotactics",
    "PhonotacticRule",
    "PhonemicConstraint",
    "ClusterConstraint",
    "ForbidPhonemeRule"
]



class Phonotactics:
    """
    `Phonotactics` is a special container for storing phonotactic information
    such as `SyllableShape` and constraints.
    """
    def __init__(self,
            syllable_shape: SyllableShape,
            phoneme_constraints: Sequence["PhonemicConstraint"],
            cluster_constraints: Sequence["ClusterConstraint"]) -> None:
        self._syllable_shape: SyllableShape = syllable_shape
        self._phoneme_constraints: Sequence[PhonemicConstraint] = phoneme_constraints
        self._cluster_constraints: Sequence[ClusterConstraint] = cluster_constraints
        self._rules: Sequence[PhonotacticRule] = (
            list(self._phoneme_constraints)
            + list(self._cluster_constraints)
        )


    @property
    def syllable_shape(self) -> SyllableShape:
        return self._syllable_shape
    

    @property
    def phonemic_constraints(self) -> list["PhonemicConstraint"]:
        return list(self._phoneme_constraints)
    

    @property
    def cluster_constraints(self) -> list["ClusterConstraint"]:
        return list(self._cluster_constraints)
        

    @property
    def rules(self) -> Sequence["PhonotacticRule"]:
        return self._rules



class PhonotacticRule:
    """
    The `PhonotacticRule` is a class representing a real-world phonotactic rule.
    """
    def __init__(self, valid_structures: list[Type[SyllabicComponent]]) -> None:
        """
        Creates a `PhonotacticRule` object.
        
        Arguments:
        - `valid_structures` - the list of valid structures where this rule can
        apply.
        """
        self._valid_structures: list[Type[SyllabicComponent]] = valid_structures
    

    @property
    def valid_locations(self) -> list[Type[SyllabicComponent]]:
        """The list of valid structures where this rule can apply."""
        return self._valid_structures
    

    @abstractmethod
    def execute_rule(self, component: SyllabicComponent | Phoneme) -> bool:
        """
        Executes this rule to the given component and returns `True` if it
        does not violate the rule.
        """



class PhonemicConstraint(PhonotacticRule):
    def __init__(self, priority: int,
            valid_locations: list[Type[SyllabicComponent]],
            phonemes: list[Phoneme]) -> None:
        super().__init__(valid_locations)
        self._phonemes: list[Phoneme] = phonemes



class ClusterConstraint(PhonotacticRule):
    def __init__(self, priority: int,
            valid_locations: list[Type[SyllabicComponent]],
            clusters: list[PhonemeCluster]) -> None:
        super().__init__(valid_locations)



class ForbidPhonemeRule(PhonemicConstraint):
    def __init__(self, valid_locations: list[Type[SyllabicComponent]],
                 phonemes: list[Phoneme]) -> None:
        super().__init__(1, valid_locations, phonemes)

    
    def execute_rule(self, component: SyllabicComponent | Phoneme) -> bool:
        """
        Returns `True` if the given component is not on the blacklist of
        phonemes.
        """
        if component in self._phonemes:
            return False
        else:
            return True