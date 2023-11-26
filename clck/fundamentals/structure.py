from abc import ABC, abstractmethod
from types import NoneType
from typing import TypeVar

from clck.fundamentals.component import Component
from clck.fundamentals.phonology import Dummy, Phoneme
from clck.utils import tuple_append, tuple_extend


T = TypeVar("T")


class Structure(Component, ABC):
    """
    The class that represents all linguistic structures.

    A linguistic structure is a component that can contain other
    components.
    """

    @abstractmethod
    def __init__(self, _valid_comp_types: tuple[type[Component], ...],
            components: tuple[Component, ...]) -> None:
        """
        Creates a new instance of `Structure` given the only valid
        component types that this can contain and its initial
        components.

        New components or substructures can be added to this instance
        using the `add_components()` and `add_substructure()` methods.
        
        Parameters
        ----------
        - `_valid_comp_types` - the permitted types of components that
            this structure can contain
        - `components` - this structure's initial components
        
        Raises
        ------
        - `TypeError` if any element in `components` is not any of the
        allowed types in `_valid_comp_types`.
        """
        super().__init__()
        self._valid_comp_types = tuple([*_valid_comp_types, Dummy])
        self._components = self._filter_none(components)
        self._assert_components()

        self._phonemes = self._get_phonemes()
        self._substructures = self._get_substructures()

        # Only then call the parent constructor after all necessary
        # attributes are initialized
        super()._create_base_properties()

        self._size = len(self._phonemes)
        self._topmost_type = self.__class__

    def __str__(self) -> str:
        return f"<{self.__class__.__name__} {self._output}>"

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} {self._output}>"

    @abstractmethod
    def _create_transcript(self) -> str:
        super()._create_transcript()

    @property
    def components(self) -> tuple[Component, ...]:
        """The components of this structure."""
        return tuple(self._components)

    @property
    def phonemes(self) -> tuple[Phoneme, ...]:
        """The phones of this structure."""
        return tuple(self._phones)

    @property
    def size(self) -> int:
        """The number of phones of this structure."""
        return self._size

    @property
    def substructures(self) -> tuple["Structure", ...]:
        """The substructures of this structure."""
        return tuple(self._substructures)

    def add_components(self, *components: Component) -> None:
        """
        Adds components to this structure.

        Parameters
        ----------
        - `components` - the components to add.
        """
        self._assert_components()
        self._components = tuple_extend(self._components, components)
        for component in components:
            self._classify_component(component)

    def add_substructure(self, substructure: "Structure") -> None:
        """
        Adds a structure to this one.

        Parameters
        ----------
        - `substructure`: the structure to be parented (added) to this
            structure.
        """
        self._assert_components()
        self._substructures = tuple_append(self._substructures, substructure)

    def find_phones_of_type(self,
            type: type[Phoneme] = Phoneme) -> tuple[Phoneme, ...]:
        """
        Returns a tuple of phones that are of the specified `Phone`
        type. If no argument is given, it returns all the phonemes of
        this structure.

        Parameters
        ----------
        - `type` - is the `Phone` subtype to find. Defaults to `Phone`.
        """
        rl: list[Phoneme] = []
        for s in self._components:
            if isinstance(s, type):
                rl.append(s)
            else:
                if isinstance(s, Structure):
                    rl.extend(s.find_phones_of_type(type))

        return tuple(rl)

    def find_structures_of_type(self,
            type: type["Structure"]) -> tuple["Structure", ...]:
        """
        Returns a tuple of all found structures that are of the given
        `Structure` subtype.

        Parameters
        ----------
        - `type` - is the `Structure` subtype to find.
        """
        rl: list[Structure] = []
        for s in self._substructures:
            if isinstance(s, type):
                rl.append(s)
            else:
                rl.extend(s.find_structures_of_type(type))

        return tuple(rl)

    def remove_component_duplicates(self, bank: tuple[T]) -> tuple[T, ...]:
        return tuple([*set(bank)])

    def remove_phoneme_duplicates(self, bank: list[Phoneme]) -> list[Phoneme]:
        return [*set(bank)]

    def remove_structure_duplicates(self,
            bank: list["Structure"]) -> list["Structure"]:
        return [*set(bank)]

    def _assert_components(self) -> None:
        """
        Runs checker functions that validates the components of this
        structure. This raises an exception if one of the checker
        functions fails.
        """

        # Run the following checker functions
        self._check_component_types_validity()

    def _check_component_types_validity(self) -> None:
        """
        Checks if the components are of the given types in
        `_valid_comp_types`.
        
        Raises
        ------
        - `TypeError` if any of the components are not of the given
            types in `_valid_comp_types`.
        """
        for c in self._components:
            mistype: bool = False
            for t in self._valid_comp_types:
                if isinstance(c, t):
                    mistype = False
                    break
                elif isinstance(c, NoneType):
                    mistype = False
                    break
                else:
                    mistype = True
            if mistype:
                raise TypeError(f"Component {c} is not of any type "
                    f"in allowed types: {self._valid_comp_types}")

    def _classify_component(self, component: Component) -> None:
        """
        Checks the type of each component and assigns them to their
        respective collection.
        """
        if isinstance(component, Structure):
            self._substructures = tuple_append(self._substructures, component)
        elif isinstance(component, Phoneme):
            self._phones = tuple_append(self._phones, component)

    def _create_label(self) -> str:
        names: list[str] = []
        for p in self._phones:
            names.append(p.name)

        return "_".join(names)

    def _create_output(self) -> str:
        output: str = ""
        for s in self._components:
            if isinstance(s, Structure):
                output += s._create_output()
            elif isinstance(s, Phoneme):
                output += s.symbol

        return output

    def _filter_none(self,
            collection: tuple[T | NoneType, ...]) -> tuple[T, ...]:
        """
        Returns a modified version of the given collection in which all
        `None` or `NoneType` values are removed.
        """
        rl: list[T] = []
        for c in collection:
            if c is not None:
                rl.append(c)

        return tuple(rl)

    def _get_phonemes(self) -> tuple[Phoneme, ...]:
        """
        Returns a tuple of all found phones within the hierarchy of this
        structure.
        """
        rl: list[Phoneme] = []
        for s in self._components:
            if isinstance(s, Phoneme):
                rl.append(s)
            else:
                if isinstance(s, Structure):
                    rl.extend(s._get_phonemes())

        return tuple(rl)

    def _get_substructures(self) -> tuple["Structure", ...]:
        """
        Returns a tuple of all children structures parented to this
        structure.
        """
        rl: list[Structure] = []
        for c in self._components:
            if isinstance(c, Structure):
                rl.append(c)

        return tuple(rl)