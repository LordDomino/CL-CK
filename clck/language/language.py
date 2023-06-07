from typing import List, Tuple

import clck.generators.generators as generators

from .managers import Manager, PhonemeGroupsManager, PhonemesManager
from ..phonology.containers import PhonologicalInventory
from ..phonology.structures import Structure


class Language:
    def __init__(self, inventory: PhonologicalInventory) -> None:
        self._inventory: PhonologicalInventory = inventory
        self._structures: List[Structure] = []
        self._syllable_generator: generators.SyllableGenerator
        self._phonological_inventory: PhonologicalInventory | None = None
        
        # Manager classes
        self._phoneme_manager: PhonemesManager = PhonemesManager()
        self._phonemegroups_manager: PhonemeGroupsManager = PhonemeGroupsManager()

        self._managers: Tuple[Manager, ...] = (
            self._phoneme_manager,
            self._phonemegroups_manager,
        )

        self._phoneme_manager.register(*self._inventory.phonemes)


    def get_managers(self) -> tuple[Manager]:
        return self._managers


    def register_structures(self, *structures: Structure) -> None:
        self._structures.extend(structures)