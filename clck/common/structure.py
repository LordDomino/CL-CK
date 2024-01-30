from abc import ABC
from types import NoneType
from typing import Generic, TypeAlias, TypeVar, Union

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
Structurable: TypeAlias = Union[tuple[ComponentT, ...], "Structure[ComponentT]", ComponentT]


class Structure(Component, ABC, Generic[ComponentT]):
    """The class that represents all CLCK structures.

    A structure is a component that can contain other
    components.
    """
    def __init__(self, structurable: Structurable[ComponentT] = (),
        _valid_types: tuple[type[Component], ...] = (Component,),
        _bp: ComponentBlueprint | None = None) -> None:
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
            _c = self._derive_components(structurable)
            self._components = filter_none(_c)
            self._valid_types = tuple([*_valid_types])
            self._assert_components()
        except TypeError:
            raise CLCKException(f"{structurable} cannot be created to a structure")

        self._phonemes = self._get_phonemes()
        self._substructures = self._get_substructures()
        self._size = len(self._phonemes)
        self._topmost_type = self.__class__

        # Only then call the parent constructor after all necessary
        # attributes are initialized
        super().__init__(self._init_default_bp(_bp))
        try:
            self._assert_blueprint_compatibility()
        except:
            self._try_blueprints(self._components)

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

    @property
    def components(self) -> tuple[ComponentT, ...]:
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
    def substructures(self) -> tuple["Structure[ComponentT]", ...]:
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
        """Returns all the vowels of this structure. This also returns
        dummy vowel phonemes that are used as placeholders in
        vowel-based structures and positions.
        """
        return tuple(self.get_phonemes_by_type(VowelPhoneme))

    def get_structures_by_type(self,
            type: type["Structure[ComponentT]"]) -> tuple["Structure[ComponentT]", ...]:
        """
        Returns a tuple of all found structures that are of the given
        `Structure` subtype.

        Parameters
        ----------
        - `type` - is the `Structure` subtype to find.
        """
        rl: list[Structure[ComponentT]] = []
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
            bank: list["Structure[ComponentT]"]) -> list["Structure[ComponentT]"]:
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

    def _assert_blueprint_compatibility(self) -> None:
        bp_default = self._default_blueprint
        match bp_default:
            case FlexibleBlueprint():
                if bp_default.limit_size == 0:
                    pass
                elif self._size > bp_default.limit_size:
                    print(f"Warning: Class \"{self.__class__.__name__}\" has flexible blueprint size of {bp_default.size} but instance size is {self._size}")
            case _:

                if self._size > bp_default.size:
                    print(f"Warning: Class \"{self.__class__.__name__}\" has blueprint size of {bp_default.size} but instance size is {self._size}")

        if self._blueprint.is_compatible_to(self._default_blueprint):
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
                elif c == ():
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

    def _derive_components(self, structurable: Structurable[ComponentT]) -> tuple[ComponentT, ...]:
        match structurable:
            case tuple():
                return structurable
            case Phoneme():
                return (structurable,)
            case Structure():
                return structurable.components

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

    def _get_substructures(self) -> tuple["Structure[ComponentT]", ...]:
        """
        Returns a tuple of all children structures parented to this
        structure.
        """
        rl: list[Structure[ComponentT]] = []
        for c in self._components:
            if isinstance(c, Structure):
                rl.append(c)

        return tuple(rl)

    def _init_output(self) -> str:
        comps: list[str] = []
        for c in self._phonemes:
            comps.append(c.output)

        return "".join(comps)

    def _init_ipa_transcript(self) -> str:
        return f"/{self._init_output()}/"

    def _init_formulang_transcript(self) -> str:
        strs: list[str] = []
        for c in self._components:
            strs.append(c.formulang_transcript)
        return f"{{{'.'.join(strs)}}}"
    
    def _init_romanization(self) -> str:
        return super()._init_romanization()

    def _init_default_bp(self, _bp: ComponentBlueprint | None = None, *args: object, **kwargs: object) -> ComponentBlueprint:
        if _bp:
            return _bp
        else:
            return self.__class__.get_default_blueprint()
        
    def _init_blueprint(self, *args: object, **kwargs: object) -> ComponentBlueprint:
        return ComponentBlueprint(*self._components)
    
    def _try_blueprints(self, c: tuple[ComponentT, ...]) -> None:
        _components = c
        _bps = self._default_blueprint.elements
        _n: list[ComponentT] = []
        for _c, _bp in zip(_components, _bps):
            if _c.blueprint.is_compatible_to(ComponentBlueprint(_bp)):
                _n.append(_c)
                continue
            elif isinstance(_bp, type) and issubclass(_bp, Structure):
                try:
                    _nc = _bp((_c,))
                    _n.append(_nc)
                except:
                    raise Exception("Cannot reconstruct")
        self._components = tuple(_n)


class EmptyStructure(Structure[ComponentT]):
    def __init__(self) -> None:
        """Creates a new `EmptyStructure` instance, containing no
        components. This can be used as an alternative representative to
        the `NoneType`.
        """
        super().__init__()

    def __repr__(self) -> str:
        return "<EmptyStructure>"
    
    def __str__(self) -> str:
        return "<EmptyStructure>"