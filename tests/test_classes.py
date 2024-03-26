"""Testing file for class-related features and functionality. This is
primarily created for fixing the type hinting issues with the new
ComponentBlueprint system.
"""

from typing import Union
from typing import Generic, TypeVar


StructurableT = TypeVar("StructurableT", bound=Union["Phoneme", "Structure"])
SyllabicStructureT = TypeVar("SyllabicStructureT", bound=Union["Phoneme", "SyllableComponent"])

class Component:
    def __init__(self) -> None:
        pass

class Phoneme(Component):
    def __init__(self) -> None:
        super().__init__()

class DummyPhoneme(Phoneme):
    def __init__(self) -> None:
        super().__init__()

class Vowel(Phoneme):
    def __init__(self) -> None:
        super().__init__()

class Structure(Component, Generic[StructurableT]): # Can contain phonemes or itself
    def __init__(self, *c: StructurableT) -> None:
        super().__init__()
        self.c = c

class SyllableComponent(Structure[SyllabicStructureT]):
    def __init__(self, *c: SyllabicStructureT) -> None:
        super().__init__(*c)

class Syllable(SyllableComponent[SyllabicStructureT]):
    def __init__(self, *c: SyllabicStructureT) -> None:
        super().__init__(*c)


s = Structure(Vowel(), Phoneme(), Structure(Phoneme()))
syl = Syllable(Syllable(Vowel(), Phoneme()))


class A: ...
class B: ...

class C(A, B): ...

l: list[B] = [C()]