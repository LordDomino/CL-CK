from typing import List, Tuple, Type

import clck.generators as generators
from clck.phonology import PhonemicInventory
from clck.managers import Manager, PhonemesManager
from clck.containers import PhonemeGroupsManager
from clck.syllabics import Structure


class Language:
    def __init__(self, inventory: PhonemicInventory) -> None:
        self._inventory: PhonemicInventory = inventory
        self._structures: List[Structure] = []
        self._syllable_generator: generators.SyllableGenerator
        self._phonological_inventory: PhonemicInventory | None = None
        
        # Manager classes
        self._phonemes_manager: PhonemesManager = PhonemesManager()
        self._phonemegroups_manager = PhonemeGroupsManager

        self._managers: Tuple[Manager | Type[Manager], ...] = (
            self._phonemes_manager,
            self._phonemegroups_manager,
        )

        self._phonemes_manager.register(*self._inventory.phonemes)


    def get_managers(self) -> tuple[Manager | Type[Manager], ...]:
        return self._managers


    def register_structures(self, *structures: Structure) -> None:
        self._structures.extend(structures)