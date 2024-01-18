from abc import ABC
from typing import TypeAlias
from clck.common.structure import Structurable, Structure
from clck.config import print_debug
from clck.phonology.phonemes import Phoneme
from clck.utils import filter_none


SyllabicComponentT: TypeAlias = "SyllabicComponent | Phoneme"


class SyllabicComponent(Structure, ABC):
    """Class for `SyllabicComponent`.

    A syllabic component is any component that comprises a syllable,
    such as phonemes and consonant clusters. Syllabic components are the
    base components 
    """
    def __init__(self, components: Structurable[SyllabicComponentT]) -> None:
        super().__init__(components, (SyllabicComponent, Phoneme))

    def _init_ipa_transcript(self) -> str:
        t: str = ""
        for c in self._components:
            t += c.ipa_transcript
        return t


class Syllable(SyllabicComponent):
    def __init__(self,
        left_margin: tuple[SyllabicComponent | Phoneme, ...],
        nucleus: tuple[SyllabicComponent | Phoneme, ...],
        right_margin: tuple[SyllabicComponent | Phoneme, ...]) -> None:
        super().__init__(filter_none(left_margin + nucleus + right_margin))
        self._nucleus = nucleus
        self._left_margin = left_margin
        self._right_margin = right_margin

    @staticmethod
    def from_structure(structure: Structure) -> "Syllable":
        size = len(structure.components)
        if size != 3:
            print_debug(f"Structure conversion warning: {structure} of component size {s} is incompatible to Syllable")
        
        lmargin = structure.components[0]
        nucleus = structure.components[1]
        rmargin = structure.components[2]

        return Syllable((lmargin,), nucleus, rmargin)

    @property
    def nucleus(self) -> tuple[SyllabicComponent | Phoneme, ...]:
        return self._nucleus
    
    @property
    def left_margin(self) -> tuple[SyllabicComponent | Phoneme, ...]:
        return self._left_margin
    
    @property
    def right_margin(self) -> tuple[SyllabicComponent | Phoneme, ...]:
        return self._right_margin


class Nucleus(SyllabicComponent):
    def __init__(self, components: tuple[SyllabicComponent | Phoneme, ...]) -> None:
        super().__init__(components)


class Onset(SyllabicComponent):
    def __init__(self, components: tuple[SyllabicComponent | Phoneme, ...]) -> None:
        super().__init__(components)


class Coda(SyllabicComponent):
    def __init__(self, components: tuple[SyllabicComponent | Phoneme, ...]) -> None:
        super().__init__(components)


class Rime(SyllabicComponent):
    def __init__(self, nucleus: Nucleus, coda: Coda) -> None:
        super().__init__((nucleus, coda))