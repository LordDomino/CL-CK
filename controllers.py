"""CL-CK controllers.
"""

import re
import random
from errors import *
from typing import Any
from datatypes import *

__all__ = [
    "random_generate",
    "Ruleset",
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


class Ruleset:
    def __init__(self) -> None:
        self._parent_generator: Generator = None

    def execute(self):
        """Executes the ruleset."""
        if self._parent_generator == None:
            raise ClCkControllerError("Ruleset cannot execute without parent generator")


class Generator:
    """A generator object to generate from a given set of inventories."""

    String_Label = str

    def __init__(self, *inventory: Inventory) -> None:
        self._inventory_list = inventory
        self._ruleset_list: list[Ruleset] = []
        self._generations: dict[list] = None
        self._generation_index: int = 0

    def generate(self, generation_label: str = None) -> dict:
        """Generate a list from the set of given inventories. Returns a list of
        all the generated outputs from different inventories. All generated
        instances are stored and can be accessed via :method:`get_generation()`.
        
        - :param:`generation_label` -- string to label generation instance

        An element will be randomly chosen from each inventory and will be
        returned in the list.
        """

        # Format generation label to only all caps and alphanumeric characters
        if generation_label != None:
            generation_label = generation_label.upper()
            generation_label = re.sub(r'[^a-zA-Z0-9]', '_', generation_label)

            labels = []

            for key in self._generations.keys():
                labels.append(key.partition("_generation")[0])

            if generation_label in labels:
                raise NameError(f"Label \'{generation_label}\' already exists in dictionary!")

        generated_list = []
        
        if self._generations == None:
            self._generations = {}
            for _inv in self._inventory_list:
                generated_list.append(random.choices(_inv.elements, _inv.weights)[0])
        else:
            for _inv in self._inventory_list:
                generated_list.append(random.choices(_inv.elements, _inv.weights)[0])
        
        if generation_label == None:
            self._generations.update({f"_generation{self._generation_index:003}": generated_list})
        else:
            self._generations.update({f"{generation_label}_generation{self._generation_index:003}": generated_list})
        self._generation_index += 1

        return(self._generations)
    
    def fresh_generate(self) -> list:
        """Generates a list from the set of given inventories. Returns a list of
        all the generated outputs from different inventories."""

    def add_ruleset(self, ruleset: Any, index: int = None) -> None:
        """Add the :class:`Ruleset` into the ruleset list of the current
        :class:`Generator` object.

        - :param:`ruleset` -- a :class:`Ruleset` instance to be appended to the
            ruleset list.
        - :param:`index` -- index to place the ruleset before or after.

        INDEXING
            The integer value to be passed is the index where :class:`ruleset`
            will be added. Its integer sign determines if :class:`ruleset` will
            be added before (if the sign is negative) or after (if the sign is
            positive).

            EXAMPLES
            
            >>> Generator().add_ruleset(ruleset = foo, index = -1)
                
                Ruleset :class:`foo` will be added before index :class:`1`

            >>> Generator().add_ruleset(ruleset = bar, index = 5)

                Ruleset :class:`bar` will be added after index :class:`5`
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
        """Adds :class:`Inventory` into the inventory list of the current
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

    def get_generation(self, index: String_Label | int, return_as_dict: bool = False) -> list | dict:
        values = None
        
        if isinstance(index, str):
            for gen_index in self._generations.keys():
                label_parts = gen_index.partition("_generation")
                if index == label_parts[0]:
                    values = self._generations[gen_index]
                    break

        elif isinstance(index, int):
            gen_index_int = f"_generation{index:003}"

            for gen_index in self._generations.keys():
                if gen_index_int in gen_index:
                    values = self._generations[gen_index]
                    break

        if values == None:
            raise KeyError(f"No label clue such as \"{index}\" found in dictionary!")

        if return_as_dict is False:
            return(values)
        elif return_as_dict is True:
            return({f"{gen_index}": values})


class MorphemeGenerator(Generator):
    """Generates morphemes from a given set of inventories."""
    def __init__(self, *inventory: Inventory) -> None:
        super().__init__(*inventory)


if __name__ == "__main__":
    gen2 = MorphemeGenerator(Inventory(["fee"]), Inventory(["foo"]))
    gen2.generate()
    gen2.generate("First Gen")
    gen2.generate("First en")
    gen2.generate()
    gen2.generate("First ")
    gen2.generate("Firt")
    gen2.generate("Firs")
    print(gen2._generations)
