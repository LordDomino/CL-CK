from abc import ABC
from clck.common.structure import Structure
from clck.phonology.phonemes import DummyPhoneme, Phoneme, VowelPhoneme


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
    def __init__(self, components: tuple[SyllabicComponent | Phoneme, ...]) -> None:
        super().__init__(components)


class Nucleus(SyllabicComponent):
    def __init__(self, components: tuple[SyllabicComponent | Phoneme, ...]) -> None:
        super().__init__(components)


class Onset(SyllabicComponent):
    def __init__(self, components: tuple[SyllabicComponent | Phoneme, ...]) -> None:
        super().__init__(components)


class Coda(SyllabicComponent):
    def __init__(self, components: tuple[SyllabicComponent | Phoneme, ...]) -> None:
        super().__init__(components)