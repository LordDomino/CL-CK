from typing import Generic, TypeVar


OffspringT = TypeVar("OffspringT", bound="Offspring")


class Offspring: ...

class Roman(Offspring, Generic[OffspringT]):
    def __init__(self, offsprings: tuple[OffspringT, ...] | OffspringT) -> None:
        super().__init__()


class French(Roman[OffspringT]):
    def __init__(self, offsprings: tuple[OffspringT, ...] | OffspringT) -> None:
        super().__init__(offsprings)


class Italian(Roman[OffspringT]):
    def __init__(self, son1: OffspringT, son2: OffspringT) -> None:
        super().__init__((son1, son2))


class DefaultOffspring(Offspring): ...


g = Italian(French(DefaultOffspring()), French(French(DefaultOffspring())))