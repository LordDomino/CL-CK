from typing import Generic
from clck.common.component import ComponentT
from clck.common.structure import Structure
from clck.phonology.phonemes import DummyConsonantPhoneme, DummyPhoneme, Phoneme


t = (1, 2, 3, 4, 5)

s1 = Structure((DummyPhoneme(), DummyConsonantPhoneme()))

class StructureIterable(Generic[*ComponentT]):
    def __init__(self, structurable: tuple[ComponentT, ...] = ()) -> None:
        super().__init__()

class TreeNodeEx(Generic[ComponentT]):
    def __init__(self, *subnodes: "TreeNodeEx[ComponentT]") -> None:
        self.subnodes = subnodes

    def eval(self) -> StructureIterable[ComponentT] | None:
        for s in self.subnodes:
            return s.eval()
        return None
    

class PhonemeTreeNode(TreeNodeEx[Phoneme]):
    def __init__(self, p: Phoneme) -> None:
        super().__init__()
        self.p = p

    def eval(self) -> StructureIterable[Phoneme]:
        return self.p

s2 = StructureIterable((DummyPhoneme(), DummyConsonantPhoneme()))
