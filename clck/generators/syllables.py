from ..phonology.syllables import SyllableShape
from ..phonology.phonemes import Phoneme


class SyllableGenerator:
    def __init__(self,
                 bank: list[Phoneme] | tuple[Phoneme],
                 shape: SyllableShape,
                 count: int = 1) -> None:
        self._bank: list[Phoneme] = list(bank)
        self._shape: SyllableShape = shape
        self._count: int = count