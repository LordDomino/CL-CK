from typing import Generic, TypeVar


OffspringT = TypeVar("OffspringT", bound="Offspring")


class Offspring: ...

class Roman(Offspring, Generic[OffspringT]):
    def __init__(self, offsprings: tuple[OffspringT, ...] | OffspringT) -> None:
        super().__init__()


class French(Roman[OffspringT]):
    def __init__(self, offsprings: tuple[OffspringT, ...] | OffspringT) -> None:
        super().__init__(offsprings)


class Italian(Roman[French[OffspringT] | "Italian[OffspringT]"]):
    def __init__(self, son1: French[OffspringT], son2: "Italian[OffspringT]") -> None:
        super().__init__((son1, son2))


g = Italian(French(Offspring()))