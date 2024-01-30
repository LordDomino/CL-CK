from typing import Generic, TypeVar


OffspringT = TypeVar("OffspringT", bound="Offspring")


class Offspring: ...

class ParentA(Generic[OffspringT]):
    def __init__(self, offsprings: tuple[OffspringT, ...] | OffspringT) -> None:
        super().__init__()


class GenerationB(ParentA[OffspringT]):
    def __init__(self, son1: OffspringT) -> None:
        super().__init__(son1)