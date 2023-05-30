from .phonemes import Phoneme


class SyllableShape:
    def __init__(self,
                 pattern: str,
                 pattern_assignments: dict[str, list[Phoneme]] | None = None) -> None:
        self._pattern: str = pattern
        self._length: int = len(self._pattern)
        self._pattern_assignments: dict[str, list[Phoneme]] | None = pattern_assignments


    @classmethod
    def from_args(cls, *types: str) -> "SyllableShape":
        return SyllableShape("".join(types))