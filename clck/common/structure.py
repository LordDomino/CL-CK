from abc import ABC
from types import NoneType
from typing import TypeAlias, TypeVar, Union

from clck.common.component import Component, FlexibleBlueprint
from clck.common.component import ComponentBlueprint
from clck.common.component import ComponentT
from clck.exceptions import CLCKException
from clck.phonology.phonemes import ConsonantPhoneme
from clck.phonology.phonemes import DummyPhoneme
from clck.phonology.phonemes import Phoneme
from clck.phonology.phonemes import VowelPhoneme
from clck.utils import filter_none
from clck.utils import tuple_append


T = TypeVar("T")
PhonemeT = TypeVar("PhonemeT", bound=Phoneme)
ComponentTypes: TypeAlias = tuple[type[ComponentT], ...]
Structurable: TypeAlias = Union[ComponentT, "Structure", Phoneme]


class Structure(Component, ABC):
    """The class that represents all CLCK structures.

    A structure is a component that can contain other
    components.
    """

    def __init__(self, *components: ComponentT,
        _valid_types: ComponentTypes[ComponentT] = (Component,)) -> None:
        """Creates a new instance of `Structure` given the only valid
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
        try:
            self._components = filter_none(components)
            self._valid_types = tuple([*_valid_types])
            self._assert_components()
        except TypeError:
            raise CLCKException(f"{components} cannot be created to a structure")

        self._phonemes = self._get_phonemes()
        self._substructures = self._get_substructures()

        # Only then call the parent constructor after all necessary
        # attributes are initialized
        super().__init__()
        
        self._assert_blueprint_compatibility()

        self._size = len(self._phonemes)
        self._topmost_type = self.__class__

    def __str__(self) -> str:
        comps: list[str] = []
        for c in self._components:
            comps.append(c._formulang_transcript)

        return f"<{self.__class__.__name__} {{{'.'.join(comps)}}}>"

    def __repr__(self) -> str:
        comps: list[str] = []
        for c in self._components:
            comps.append(c._formulang_transcript)

        return f"<{self.__class__.__name__} {{{'.'.join(comps)}}}>"

    def _init_ipa_transcript(self) -> str:
        return f"/{self._output}/"

    def _init_formulang_transcript(self) -> str:
        strs: list[str] = []
        for c in self._components:
            strs.append(c.formulang_transcript)
        return f"{{{'.'.join(strs)}}}"

    def _init_output(self) -> str:
        comps: list[str] = []
        for c in self._phonemes:
            comps.append(c.output)

        return "".join(comps)

    def _init_romanization(self) -> str | None:
        return "_create_romanization() WIP"

    def _init_blueprint(self) -> ComponentBlueprint:
        return ComponentBlueprint(*self._components)

    @property
    def components(self) -> tuple[Component, ...]:
        """The components of this structure."""
        return self._components

    @property
    def output(self) -> str:
        return f"{self._output}"

    @property
    def phonemes(self) -> tuple[Phoneme, ...]:
        """The phones of this structure."""
        return tuple(self._phonemes)

    @property
    def size(self) -> int:
        """The number of phones of this structure."""
        return self._size

    @property
    def substructures(self) -> tuple["Structure", ...]:
        """The substructures of this structure."""
        return tuple(self._substructures)

    def get_phonemes_by_type(self,
            type: type[PhonemeT] = Phoneme) -> tuple[PhonemeT, ...]:
        """
        Returns a tuple of phones that are of the specified `Phone`
        type. If no argument is given, it returns all the phonemes of
        this structure.

        Parameters
        ----------
        - `type` - is the `Phone` subtype to find. Defaults to `Phone`.
        """
        rl: list[PhonemeT] = []
        for s in self._components:
            if isinstance(s, type):
                rl.append(s)
            else:
                if isinstance(s, Structure):
                    rl.extend(s.get_phonemes_by_type(type))
        return tuple(rl)

    def get_consonants(self) -> tuple[ConsonantPhoneme, ...]:
        """
        Returns all the consonants of this structure. This also returns
        dummy consonant phonemes that are used as placeholders in
        consonant-based structures and positions.
        """
        return tuple(self.get_phonemes_by_type(ConsonantPhoneme))

    def get_vowels(self) -> tuple[VowelPhoneme, ...]:
        """
        Returns all the vowels of this structure. This also returns
        dummy vowel phonemes that are used as placeholders in
        vowel-based structures and positions.
        """
        return tuple(self.get_phonemes_by_type(VowelPhoneme))

    def get_structures_by_type(self,
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
                rl.extend(s.get_structures_by_type(type))
        return tuple(rl)

    def remove_component_duplicates(self, bank: tuple[T]) -> tuple[T, ...]:
        return tuple([*set(bank)])

    def remove_phoneme_duplicates(self, bank: list[Phoneme]) -> list[Phoneme]:
        return [*set(bank)]

    def remove_structure_duplicates(self,
            bank: list["Structure"]) -> list["Structure"]:
        return [*set(bank)]

    @classmethod
    def get_default_blueprint(cls) -> ComponentBlueprint:
        return FlexibleBlueprint()

    def _append_dummies(self, to: tuple[ComponentT, ...]) -> tuple[ComponentT | DummyPhoneme, ...]:
        nl: list[ComponentT | DummyPhoneme] = [*to]
        for c in self._components:
            if isinstance(c, DummyPhoneme):
                nl.append(c)

        return tuple(nl)

    def _assert_blueprint_compatibility(self, bp: ComponentBlueprint | None = None) -> None:
        if bp:
            if bp.is_compatible_to(self.__class__.get_default_blueprint()):
                return
        else:
            if self._blueprint.is_compatible_to(self.__class__.get_default_blueprint()):
                return
        raise CLCKException("Cannot create structure because of blueprint incompatibility")

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
            for t in self._valid_types:
                if isinstance(c, t):
                    mistype = False
                    break
                elif isinstance(c, NoneType):
                    mistype = False
                    break
                else:
                    mistype = True
                    continue
            if mistype:
                raise TypeError(f"Component {c} is not of any type "
                    f"in allowed types: {self._valid_types}")

    def _classify_component(self, component: Component) -> None:
        """
        Checks the type of each component and assigns them to their
        respective collection.
        """
        if isinstance(component, Structure):
            self._substructures = tuple_append(self._substructures, component)
        elif isinstance(component, Phoneme):
            self._phonemes = tuple_append(self._phonemes, component)

    def _create_label(self) -> str:
        names: list[str] = []
        for p in self._phonemes:
            names.append(p.base_phone.name)

        return "_".join(names)

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