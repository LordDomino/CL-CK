from abc import ABC, abstractmethod
from types import NoneType
from typing import Any, Collection, List, Type

from .phonemes import Phoneme



class Structure(ABC):


    @abstractmethod
    def __init__(self, _allowed_types: Collection[type], *components: Any) -> None:
        """
        Creates a new instance of `Structure`.
        
        Parameters
        ---------
        - `_allowed_types` are the permitted types of components.
        - `components` are the components.

        Raises
        ------
        - `TypeError` if any element in `components` is not of the allowed types
        in `_allowed_types`.
        """
        self._assert_components(tuple(components), _allowed_types)
        self._allowed_types: tuple[type] = tuple(_allowed_types)
        self._components: List[Structure | Phoneme] = self._filter_none(components)
        self._phonemes: tuple[Phoneme] = tuple(self.find_phonemes(Phoneme))
        self._size: int = len(self._phonemes)
        self._substructures: tuple[Structure] = self._get_substructures()
        self._label: str = self._create_label()
        self._output: str = self._create_output()
        self._transcript: str = self._create_transcript()

    
    @abstractmethod
    def _create_transcript(self) -> str: pass

    
    def __str__(self) -> str:
        return (f"{self.__class__.__name__} \033[1m{self._output}\033[0m of "
            f"components {self._components}")


    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} {self._output}>"


    @property
    def components(self) -> List["Structure | Phoneme"]:
        """The components of this structure."""
        return self._components


    @property
    def label(self) -> str:
        """The label string for this structure."""
        return self._label
    

    @property
    def output(self) -> str:
        """The final string representation of this structure."""
        return self._output
    

    @property
    def size(self) -> int:
        """The number of components of this structure."""
        return self._size
    

    @property
    def substructures(self) -> tuple["Structure", ...]:
        """The substructures of this structure."""
        return self._substructures


    @property
    def transcript(self) -> str:
        return self._transcript


    def add_components(self, *components: "Structure | Phoneme") -> None:
        """
        Adds components to this structure.

        Arguments
        - `components` - the components to add.
        """
        self._assert_components(components, self._allowed_types)
        self._components = [*self._components, *components]
        for component in components:
            self._classify_component(component)

    
    def add_substructure(self, substructure: "Structure") -> None:
        self._assert_components(tuple([substructure]), self._allowed_types)
        self._substructures = tuple([*self._substructures, substructure])


    def find_phonemes(self, type: Type[Phoneme]) -> list[Phoneme]:
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
        return rl


    def find_substructures(self, type: Type["Structure"]) -> list["Structure"]:
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
        return rl


    def _assert_components(self, components: tuple[Any, ...],
        allowed_types: Collection[type]) -> bool:
        """
        Checks if the components are of the given types in `_component_types`.

        Arguments
        - `components` - is the tuple of components to assert.
        - `component_types` - is the list of permitted types of components.
        
        Returns
        - `True` if the components are of the given types.
        
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


    def _classify_component(self, component: "Structure | Phoneme") -> None:
        if isinstance(component, Structure):
            self._substructures = tuple([*self._substructures, component])
        else:
            self._phonemes = tuple([*self._phonemes, component])


    def _create_label(self) -> str:
        names: list[str] = []
        for p in self._phonemes:
            names.append(p.name)
        return "_".join(names)


    def _create_output(self) -> str:
        """
        Creates the output string of this structure.
        
        Returns
        - The output string of this structure.
        """
        output: str = ""
        for s in self._components:
            if isinstance(s, Structure):
                output += s._create_output()
            else:
                output += s.symbol
        return output


    def _filter_none(self, collection: Collection[Any]) -> list[Any]:
        rl: list[Any] = []
        for c in collection:
            if c is not None:
                rl.append(c)
        return rl


    def _get_substructures(self) -> tuple["Structure"]:
        rl: list[Structure] = []
        for c in self._components:
            if isinstance(c, Structure):
                rl.append(c)
        
        return tuple(rl)