from abc import ABC
from typing import TypeVar
from clck.common.component import AnyBlueprint, ComponentBlueprint, FlexibleBlueprint
from clck.common.structure import PhonemeT, Structurable, Structure
from clck.phonology.phonemes import Phoneme


SyllabicComponentT = TypeVar("SyllabicComponentT", "SyllabicComponent", Phoneme)


class SyllabicComponent(Structure[SyllabicComponentT], ABC):
    """Class for `SyllabicComponent`.

    A syllabic component is any component that comprises a syllable,
    such as phonemes and consonant clusters. Syllabic components are the
    base components 
    """
    def __init__(self, components: Structurable[SyllabicComponentT]) -> None:
        super().__init__(components, _valid_types=(SyllabicComponent[SyllabicComponentT], Phoneme))

    def _init_ipa_transcript(self) -> str:
        t: str = ""
        for c in self._components:
            t += c.ipa_transcript
        return t

    @classmethod
    def get_default_blueprint(cls) -> ComponentBlueprint:
        return FlexibleBlueprint((SyllabicComponent[SyllabicComponentT], Phoneme))


SyllableMargin = AnyBlueprint(SyllabicComponent, Phoneme)


class Syllable(SyllabicComponent[SyllabicComponentT]):
    def __init__(self, components: Structurable[SyllabicComponentT]) -> None:
        super().__init__(components)
        self._left_margin = self._components[0]
        self._nucleus = Nucleus(self._components[1])
        self._right_margin = self._components[2]

        # if not self._blueprint.is_compatible_to(Syllable.get_default_blueprint()):
            # raise Exception(f"Cannot create a component of less than the elements required (Number of required components is 3 while given is only {len(components)})")

    @property
    def nucleus(self) -> "Nucleus":
        return self._nucleus
    
    @property
    def left_margin(self) -> SyllabicComponentT:
        return self._left_margin
    
    @property
    def right_margin(self) -> SyllabicComponentT:
        return self._right_margin
    
    @classmethod
    def get_default_blueprint(cls) -> ComponentBlueprint:
        return ComponentBlueprint(SyllableMargin, Nucleus, SyllableMargin)


class Nucleus(SyllabicComponent[Phoneme]):
    def __init__(self, components: Structurable[Phoneme]) -> None:
        super().__init__(components)

    @classmethod
    def get_default_blueprint(cls) -> ComponentBlueprint:
        return ComponentBlueprint(FlexibleBlueprint((Phoneme,)))


class Onset(SyllabicComponent[SyllabicComponentT]):
    def __init__(self, components: Structurable[SyllabicComponentT]) -> None:
        super().__init__(components)


class Coda(SyllabicComponent[SyllabicComponentT]):
    def __init__(self, components: Structurable[SyllabicComponentT]) -> None:
        super().__init__(components)


class Rime(SyllabicComponent[Nucleus | Coda[PhonemeT]]):
    def __init__(self, nucleus: Nucleus, coda: Coda[PhonemeT]) -> None:
        super().__init__((nucleus, coda))