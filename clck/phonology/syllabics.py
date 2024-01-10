from abc import ABC
from clck.common.structure import Structure
from clck.phonology.phonemes import Phoneme


class SyllabicComponent(Structure, ABC):
    """Class for `SyllabicComponent`.

    A syllabic component is any component that comprises a syllable,
    such as phonemes and phoneme clusters.
    """
    def __init__(self, components: tuple["SyllabicComponent | Phoneme", ...]) -> None:
        super().__init__((SyllabicComponent, Phoneme), components)

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
        super().__init__(Structure.filter_none(left_margin + nucleus + right_margin))
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