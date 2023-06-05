from typing import Any, List

from ..phonology.structures import Structure


class Language:
    def __init__(self) -> None:
        self._structures: List[Structure] = []
        self._syllable_generator: Any | None = None


    def register_structures(self, *structures: Structure) -> None:
        self._structures.extend(structures)