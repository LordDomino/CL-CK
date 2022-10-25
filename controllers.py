"""CL-CK controllers.
"""

import random
from typing import Any
from datatypes import *

__all__ = [
    "random_generate",
    "Generator",
    "MorphemeGenerator",
]

def random_generate(*inventory: Inventory) -> list[str]:
    """Randomly generates an element per Inventory from a set of given
    :class:`Inventory` instances.
    """
    _returnlist: list = []
    for _i in inventory:
        _returnlist.append(random.choices(_i, weights=_i.weights)[0])
    return _returnlist


class Generator():
    """A generator object to generate from a given set of inventories."""
    def __init__(self, *inventory: Inventory) -> None:
        self._inventory_list = inventory
        self._ruleset_list: list = []

    def generate(self) -> Any:
        """Generate from a set of given inventories."""
    
    def fresh_generate(self) -> Any:...

    def add_ruleset(self, ruleset: Any, index: int = None) -> None:
        """Add the :class:`Ruleset` into the ruleset list of the current
        :class:`Generator` object.

        - :class:`ruleset` -- a :class:`Ruleset` instance to be appended to the
            ruleset list.
        - :class:`index` -- index to place the ruleset before or after.

        INDEXING
            The integer value to be passed is the index where :class:`ruleset`
            will be added. Its integer sign determines if :class:`ruleset` will
            be added before (if the sign is negative) or after (if the sign is
            positive).

            Examples:
            >>> .add_ruleset(ruleset = foo, index = -1)
                
                Ruleset :class:`foo` will be added before index :class:`1`.

            >>> .add_ruleset(ruleset = bar, index = 5)

                Ruleset :class:`bar` will be added after index :class:`5`.
        """
        if index == None:
            if len(self._ruleset_list) == 0:
                index = 0
            elif len(self._ruleset_list) > 0:
                index = len(self._ruleset_list) - 1
        elif isinstance(index, int):
            if index/-1 == -index:
                self._ruleset_list.insert(index+1, ruleset)
            elif index/-1 == index:
                self._ruleset_list.insert(index, ruleset)

    def set_ruleset(self, new_ruleset: Ruleset, index: int) -> None:
        """Replace a ruleset with new :class:`Ruleset` on index in the list of
        all rulesets.
        """
        self._ruleset_list[index] = new_ruleset

    def add_inventory(self, inventory: Inventory, index: str = "+") -> None:
        """Add :class:`Inventory` into the inventory list of the current
        :class:`Generator` object.

        - :class:`inventory` -- an :class:`Inventory` instance to be appended to
            the inventory list.
        - :class:`index` -- index to place the ruleset before or after.

        INDEXING
            The integer value to be passed is the index where :class:`inventory`
            will be added. Its integer sign determines if :class:`inventory`
            will be added before (if the sign is negative) or after (if the sign
            is positive).

            Examples:
            >>> .add_inventory(inventory = foo, index = -6)
                
                Inventory :class:`foo` will be added before index :class:`-6`.

            >>> .add_inventory(inventory = bar, index = 5)

                Inventory :class:`bar` will be added after index :class:`5`.
        """
        if index == None:
            if len(self._inventory_list) == 0:
                index = 0
            elif len(self._inventory_list) > 0:
                index = len(self._inventory_list) - 1
        elif isinstance(index, int):
            if index/-1 == -index:
                self._inventory_list.insert(index+1, inventory)
            elif index/-1 == index:
                self._inventory_list.insert(index, inventory)


class MorphemeGenerator(Generator):
    """Generates morphemes from a given set of inventories."""
    def __init__(self, *inventory: Inventory) -> None:
        super().__init__()
        self.inventory_list = inventory