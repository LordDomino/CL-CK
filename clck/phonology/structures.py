from abc import ABC, abstractmethod
from types import NoneType
from typing import Any, Collection, TypeVar

from clck.util import tuple_append, tuple_extend

from .component import Component
from .phonemes import Phoneme

T = TypeVar("T")

class Structure(Component, ABC):

    @abstractmethod
    def __init__(self, _allowed_types: tuple[type, ...],
            components: tuple[Component, ...]) -> None:
        """
        Creates a new instance of `Structure`.
        
        Parameters
        ----------
        - `_allowed_types` are the permitted types of components.
        - `components` are the components.

        Raises
        ------
        - `TypeError` if any element in `components` is not of the allowed types
        in `_allowed_types`.
        """
        self._assert_components(components, _allowed_types)
        self._allowed_types: tuple[type[Component]] = _allowed_types
        self._components: tuple[Component] = self._filter_none(components)
        self._phonemes: tuple[Phoneme] = self.find_phonemes()
        self._substructures: tuple[Structure] = self._get_substructures()
        
        super().__init__()  # Only then call the parent constructor after all necessary attributes are initialized
        
        self._size: int = len(self._phonemes)
        self._label: str = self._create_label()

    @abstractmethod
    def _create_transcript(self) -> str:
        """Creates the IPA transcript for this object."""
        pass

    def __str__(self) -> str:
        return f"<{self.__class__.__name__} {self._output}>"

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} {self._output}>"

    @property
    def components(self) -> tuple[Component, ...]:
        """The components of this structure."""
        return tuple(self._components)

    @property
    def label(self) -> str:
        """The label string for this structure."""
        return self._label  

    @property
    def phonemes(self) -> tuple[Phoneme, ...]:
        return tuple(self._phonemes)

    @property
    def size(self) -> int:
        """The number of phonemes of this structure."""
        return self._size

    @property
    def substructures(self) -> tuple["Structure", ...]:
        """The substructures of this structure."""
        return tuple(self._substructures)

    def add_components(self, *components: Component) -> None:
        """
        Adds components to this structure.

        Arguments
        - `components` - the components to add.
        """
        self._assert_components(components, self._allowed_types)
        self._components = tuple_extend(self._components, components)
        for component in components:
            self._classify_component(component)
    
    def add_substructure(self, substructure: "Structure") -> None:
        self._assert_components(tuple([substructure]), self._allowed_types)
        self._substructures = tuple_append(self._substructures, substructure)

    def find_phonemes(self, type: type[Phoneme] = Phoneme) -> tuple[Phoneme]:
        """
        Returns a list of phonemes that are of the specified `Phoneme` subtype.

        Arguments
        - `type` - is the `Phoneme` subtype.
        """
        rl: list[Phoneme] = []
        for s in self._components:
            if isinstance(s, type):
                rl.append(s)
            else:
                if isinstance(s, Structure):
                    rl.extend(s.find_phonemes(type))

        return tuple(rl)

    def find_substructures(self, type: type["Structure"]) -> list["Structure"]:
        """
        Returns a list of substructures of the given `Structure` subtype.

        Parameters
        ----------
        - `type` is any of the `Structure` subtype.
        """
        rl: list[Structure] = []
        for s in self._substructures:
            if isinstance(s, type):
                rl.append(s)
            else:
                rl.extend(s.find_substructures(type))
        rl = self.remove_structure_duplicates(rl)

        return rl
    
    def remove_component_duplicates(self,
            bank: tuple[T]) -> tuple[T]:
        return tuple([*set(bank)])
    
    def remove_phoneme_duplicates(self, bank: list[Phoneme]) -> list[Phoneme]:
        return [*set(bank)]

    def remove_structure_duplicates(self,
            bank: list["Structure"]) -> list["Structure"]:
        return [*set(bank)]

    def _assert_components(self, components: tuple[Component, ...],
        allowed_types: Collection[type]) -> bool:
        """
        Checks if the components are of the given types in `_component_types`.

        Arguments
        - `components` - is the tuple of components to assert.
        - `component_types` - is the list of permitted types of components.
        
        Returns
        - `True` if all the components are of the given types.
        
        Raises
        - `TypeError` if any of the components are not of the given types.
        """
        for c in components:
            mistype: bool = False
            for t in allowed_types:
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
                    f"in {allowed_types}")

        return True

    def _classify_component(self, component: Component) -> None:
        if isinstance(component, Structure):
            self._substructures = tuple_append(self._substructures, component)
        elif isinstance(component, Phoneme):
            self._phonemes = tuple_append(self._phonemes, component)

    def _create_label(self) -> str:
        names: list[str] = []
        for p in self._phonemes:
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

    def _filter_none(self, collection: tuple[Any, ...]) -> tuple[Any]:
        rl: list[Any] = []
        for c in collection:
            if c is not None: # type: ignore
                rl.append(c)

        return tuple(rl)

    def _get_substructures(self) -> tuple["Structure"]:
        rl: list[Structure] = []
        for c in self._components:
            if isinstance(c, Structure):
                rl.append(c)
        
        return tuple(rl)