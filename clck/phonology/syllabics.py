from abc import ABC
from typing import TypeAlias, Union
from clck.common.structure import Structure
from clck.common.structure import Structurable
from clck.phonology.phonemes import Phoneme
from clck.utils import filter_none


SyllabicComponentT: TypeAlias = Union["SyllabicComponent", Phoneme]


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
        left_margin: Structurable[SyllabicComponentT],
        nucleus: Structurable[SyllabicComponentT],
        right_margin: Structurable[SyllabicComponentT]) -> None:
        super().__init__(filter_none(left_margin + nucleus + right_margin))
        self._nucleus = nucleus
        self._left_margin = left_margin
        self._right_margin = right_margin

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