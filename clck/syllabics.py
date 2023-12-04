from abc import ABC, abstractmethod
from types import NoneType
from typing import TypeVar

from clck.component import Component
from clck.phonology import ConsonantPhoneme, DummyPhoneme, Phoneme, VowelPhoneme
from clck.containers import PhonemeGroup, PhonemeGroupsManager
from clck.utils import tuple_append, tuple_extend


__all__ = [
    "Syllable",
    "Onset",
    "Nucleus",
    "Coda",
    "Rime",
    "ConsonantCluster",
    "PhonemeCluster",
    "VowelCluster",
    "Diphthong",
    "Triphthong",
]

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
        self._valid_comp_types = tuple([*_valid_comp_types])
        self._components = self._filter_none(components)
        self._assert_components()

        self._phonemes = self._get_phonemes()
        self._substructures = self._get_substructures()
        self._consonants = self.get_consonants()
        self._vowels = self.get_vowels()

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
    def consonants(self) -> tuple[ConsonantPhoneme, ...]:
        """The consonants of this structure."""
        return tuple(self._consonants)

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
    
    @property
    def vowels(self) -> tuple[VowelPhoneme, ...]:
        """The vowels of this structure."""
        return tuple(self._vowels)

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

    def get_consonants(self) -> tuple[ConsonantPhoneme, ...]:
        """
        Returns all the consonants of this structure. This also returns
        dummy consonant phonemes that are used as placeholders in
        consonant-based structures and positions.
        """
        consonants: list[ConsonantPhoneme] = []
        for component in self._components:
            if isinstance(component, ConsonantPhoneme):
                consonants.append(component)
            else:
                if isinstance(component, SyllabicComponent):
                    consonants.extend(component.get_consonants())
        return tuple(consonants)
    
    def get_vowels(self) -> tuple[VowelPhoneme, ...]:
        """
        Returns all the vowels of this structure. This also returns
        dummy vowel phonemes that are used as placeholders in
        vowel-based structures and positions.
        """
        vowels: list[VowelPhoneme] = []
        for component in self._components:
            if isinstance(component, VowelPhoneme):
                vowels.append(component)
            else:
                if isinstance(component, SyllabicComponent):
                    vowels.extend(component.get_vowels())
        return tuple(vowels)

    def get_phonemes_by_type(self,
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
                    rl.extend(s.get_phonemes_by_type(type))

        return tuple(rl)

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

    def _append_dummies(self, to: tuple[T, ...]) -> tuple[T | DummyPhoneme, ...]:
        nl: list[T | DummyPhoneme] = [*to]
        for c in self._components:
            if isinstance(c, DummyPhoneme):
                nl.append(c)

        return tuple(nl)

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
            self._phonemes = tuple_append(self._phonemes, component)

    def _create_label(self) -> str:
        names: list[str] = []
        for p in self._phonemes:
            names.append(p.base_phone.name)

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


class Pattern:
    def __init__(self, string: str) -> None:
        self._string: str = string
        self._symbols: list[str] = [*self._generate_symbols()]
        self._check_pattern_validity(self._symbols)  # all initialized symbols should be present in PhonemeGroupsManager.labels
        self._phoneme_groups: tuple[PhonemeGroup, ...] = self._get_phoneme_groups()
        self._phonemes: tuple[Phoneme, ...] = tuple(set(self._get_phonemes()))

    @property
    def phonemes(self) -> tuple[Phoneme, ...]:
        """The tuple of all recognized `Phoneme`s in this pattern."""
        return tuple(self._phonemes)

    @property
    def phoneme_groups(self) -> tuple[PhonemeGroup, ...]:
        """The tuple of all recognized `PhonemeGroup`s in this pattern."""
        return tuple(self._phoneme_groups)

    @property
    def string(self) -> str:
        """The string representation of this pattern."""
        return self._string

    @property
    def symbols(self) -> list[str]:
        """The list of all recognized labels in this pattern."""
        return self._symbols

    def _check_pattern_validity(self, labels: list[str]) -> bool:
        """Checks the existence of each character used in this pattern by
        comparing it to the list of all registered `PhonemeGroup` labels in
        `PhonemeGroupsManager.labels`.
        
        Returns
        -------
            `True` if all the characters in the pattern string are present
            in `PhonemeGroupsManager.labels`.
            
        Raises
        ------
            `ValueError` if any character in the pattern string is not in
            `PhonemeGroupsManager.labels`.
        """
        for char in labels:
            if char not in PhonemeGroupsManager.labels:
                raise ValueError(f"Unknown pattern label \"{char}\" in pattern "
                    f"string \"{labels}\"")
        
        return True 

    def _generate_symbols(self) -> tuple[str, ...]:
        """Returns a tuple of all the recognized `PhonemeGroup` labels."""
        l: list[str] = []
        for char in self._string:
            l.append(char)
        
        return tuple(l)

    def _get_phonemes(self) -> tuple[Phoneme, ...]:
        """Returns the tuple of all recognized `Phoneme`s in this pattern."""
        l: list[Phoneme] = []
        for pg in self._phoneme_groups:
            l.extend(pg.phonemes)
        
        return tuple(l)

    def _get_phoneme_groups(self) -> tuple[PhonemeGroup, ...]:
        g: list[PhonemeGroup] = []
        for symbol in self._symbols:
            for phoneme_group in PhonemeGroupsManager.global_list:
                if symbol == phoneme_group.label:
                    g.append(phoneme_group)
                    break
        
        return tuple(g)


class Shape:
    def __init__(self, _comps_type: type[ConsonantPhoneme | VowelPhoneme],
            pattern_strings: str) -> None:
        self._comps_type: type[ConsonantPhoneme | VowelPhoneme] = _comps_type
        self._pattern: Pattern = Pattern(pattern_strings)
        self._pattern_string: str = self._pattern.string
        self._length: int = len(self._pattern.symbols)

        self._check_phoneme_types()

    @property
    def length(self) -> int:
        return self._length

    @property
    def pattern(self) -> Pattern:
        return self._pattern

    @property
    def pattern_string(self) -> str:
        return self._pattern_string
    
    def _check_phoneme_types(self) -> bool:
        for phoneme in self._pattern.phonemes:
            if not isinstance(phoneme, self._comps_type):
                raise TypeError(f"Phoneme object {phoneme.__repr__()} "
                    f"must be of type {self._comps_type.__name__} specified "
                    f"for {self.__class__.__name__}",
                    phoneme.__class__.__name__)
        return True


class OnsetShape(Shape):
    def __init__(self, pattern: str) -> None:
        super().__init__(ConsonantPhoneme, pattern)


class NucleusShape(Shape):
    def __init__(self, pattern: str) -> None:
        super().__init__(VowelPhoneme, pattern)


class CodaShape(Shape):
    def __init__(self, pattern: str) -> None:
        super().__init__(ConsonantPhoneme, pattern)


class SyllableStructure:
    def __init__(self, onset: OnsetShape | None, nucleus: NucleusShape,
            coda: CodaShape | None) -> None:
        self._onset_shape: OnsetShape | None = onset
        self._nucleus_shape: NucleusShape = nucleus
        self._coda_shape: CodaShape | None = coda
        self._pattern_string: str = self._create_pattern_string()        

    @property
    def pattern_string(self) -> str:
        """The combined pattern string of the onset, nucleus, and coda
        shapes."""
        return self._pattern_string

    @property
    def onset_shape(self) -> OnsetShape | None:
        """The onset shape of this instance. Returns `None` if this syllable
        shape permits no onsets."""
        return self._onset_shape
    
    @property
    def nucleus_shape(self) -> NucleusShape:
        """The nucleus shape of this instance."""
        return self._nucleus_shape

    @property
    def coda_shape(self) -> CodaShape | None:
        """The coda shape of this instance. Returns `None` if this syllable
        shape permits no codas."""
        return self._coda_shape

    def get_onc_lengths(self) -> tuple[int, int, int]:
        """
        Returns a tuple of the length of the onset shape, nucleus shape, and
        coda shape.
        """
        o: int
        c: int

        if self._onset_shape is None:
            o = 0
        else:
            o = self._onset_shape.length

        if self._coda_shape is None:
            c = 0
        else:
            c = self._coda_shape.length

        return (o, self._nucleus_shape.length, c)  

    def _create_pattern_string(self) -> str:
        shapes: list[str] = []

        if self._onset_shape is not None:
            shapes.append(self._onset_shape.pattern.string)

        shapes.append(self._nucleus_shape.pattern.string)

        if self._coda_shape is not None:
            shapes.append(self._coda_shape.pattern.string)

        return "".join(shapes)


class SyllabicComponent(Structure, ABC):
    """
    Class for `SyllabicComponent`.

    A syllabic component is any component that comprises a syllable, such as
    phonemes and phoneme clusters.
    """
    @abstractmethod
    def __init__(self,
            _allowed_types: tuple[type["SyllabicComponent | Phoneme"], ...],
            *components: "SyllabicComponent | Phoneme") -> None:
        super().__init__(_allowed_types, components)
        self._components: tuple[SyllabicComponent | Phoneme, ...] = components

    def get_phonemes(self) -> list[Phoneme]:
        phonemes: list[Phoneme] = []
        for component in self._components:
            if isinstance(component, Phoneme):
                phonemes.append(component)
            else:
                component.get_phonemes()
        return phonemes

    def _create_transcript(self) -> str:
        t: str = ""
        for c in self._components:
            if isinstance(c, Phoneme):
                t += c.transcript
            else:
                t += c._create_transcript()
        return t


class Onset(SyllabicComponent):
    def __init__(self, *components: ConsonantPhoneme) -> None:
        super().__init__((ConsonantPhoneme, ConsonantCluster), *components)
        self._consonants = self._append_dummies(self._consonants)

        if len(components) > 1:
            self.add_substructure(ConsonantCluster(*components))


class Nucleus(SyllabicComponent):
    def __init__(self, *components: VowelPhoneme) -> None:
        super().__init__((VowelPhoneme, VowelCluster), *components)
        self._vowels = self._append_dummies(self._vowels)

        if len(components) == 2:
            self.add_substructure(Diphthong(components[0], components[1]))
        elif len(components) == 3:
            self.add_substructure(Triphthong(components[0], components[1],
                components[2]))
        elif len(components) > 3:
            self.add_substructure(VowelCluster(*components))


class Coda(SyllabicComponent):
    def __init__(self, *components: ConsonantPhoneme) -> None:
        super().__init__((ConsonantPhoneme,), *components)
        self._consonants = self._append_dummies(self._consonants)

        if len(components) > 1:
            self.add_substructure(ConsonantCluster(*components))


class PhonemeCluster(SyllabicComponent):
    def __init__(self, allowed_type: type[Phoneme],
            *components: Phoneme) -> None:
        """
        Creates a new `Cluster` instance given the only allowed types
        and initial components.
        
        Parameters
        ----------
        - `component_type`: the only allowed type of the components
        - `phonemes`: the initial component phonemes of this cluster
        
        Raises
        ------
        - `TypeError` if any element in `phonemes` is not of the given type,
        `component_type`.
        
        A cluster logically exists as a group of at least two phoneme
        components. Thus, note that during instantiation of the
        instance, the constructor checks if the number of given phonemes
        are not below two.
        """
        super().__init__((allowed_type,), *components)
        self._phonemes: tuple[Phoneme, ...] = components
        self._output: str = self._create_output()
        self._check_cluster_size()

    def __str__(self) -> str:
        return (f"{self.__class__.__name__} \033[1m{self._output}\033[0m "
            f"of phonemes {self._phonemes}")

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} {self._output}>"

    @property
    def phonemes(self) -> tuple[Phoneme, ...]:
        """The component phonemes of this cluster."""
        return self._phonemes

    @property
    def symbol(self) -> str:
        """The final string representation of this cluster."""
        return self._output

    def _check_cluster_size(self) -> bool:
        """
        Checks if the number of phonemes in the cluster is less than
        two.
        
        Raises
        ------
        - `ValueError` if the number of clusters is less than two.
        """
        if len(self.phonemes) < 2:
            raise ValueError(f"Cannot create {self.__class__.__name__} with "
                f"less than 2 components. Insufficient amount of items."
                f"({len(self._phonemes)}).")
        else:
            return True


class ConsonantCluster(PhonemeCluster):
    """
    Class for `ConsonantCluster`, a special type of phoneme cluster to
    enclose multiple consonants.
    """
    def __init__(self, *consonants: ConsonantPhoneme) -> None:
        super().__init__(ConsonantPhoneme, *consonants)


class VowelCluster(PhonemeCluster):
    """
    Class for `VowelCluster`, a special type of phoneme cluster to
    enclose multiple vowels.
    """
    def __init__(self, *vowels: VowelPhoneme) -> None:
        super().__init__(VowelPhoneme, *vowels)


class Diphthong(VowelCluster):
    """
    Class for `Diphthong` objects.
    A diphthong is a combination of two vowels.
    """
    def __init__(self, vowel_1: VowelPhoneme, vowel_2: VowelPhoneme) -> None:
        super().__init__(vowel_1, vowel_2)


class Triphthong(VowelCluster):
    """
    Class for `Triphthong` objects.
    A triphthong is a combination of three vowels.
    """
    def __init__(self, vowel_1: VowelPhoneme, vowel_2: VowelPhoneme,
            vowel_3: VowelPhoneme) -> None:
        super().__init__(vowel_1, vowel_2, vowel_3)


class Rime(SyllabicComponent):
    def __init__(self, nucleus: Nucleus, coda: Coda | None) -> None:
        if coda is None:
            super().__init__((Nucleus, Coda), nucleus)
        else:
            super().__init__((Nucleus, Coda), nucleus, coda)
        self._nucleus: Nucleus = nucleus
        self._coda: Coda | None = coda

    @property
    def nucleus(self) -> Nucleus:
        """The nucleus component of this rime."""
        return self._nucleus

    @property
    def coda(self) -> Coda | None:
        """The coda component of this rime."""
        return self._coda

    def _create_transcript(self) -> str:
        t: str = ""
        for c in self._phonemes:
            t += c.symbol
        return f"/{t}/"


class Syllable(Structure):
    def __init__(self, onset: Onset | None, nucleus: Nucleus,
        coda: Coda | None) -> None:
        """
        Creates a new `Syllable` instance from the given onset, nucleus,
        and coda components.

        Parameters
        ----------
        - `onset`: the onset component of this syllable
        - `nucleus`: the nucleus component of this syllable
        - `coda`: the coda component of this syllable
        """
        super().__init__((SyllabicComponent, Phoneme),
            self._filter_none((onset, nucleus, coda)))
        self._phonemes: tuple[Phoneme, ...] = tuple(
            self.get_phonemes_by_type(Phoneme))
        self._onset: Onset | None = onset
        self._nucleus: Nucleus = nucleus
        self._coda: Coda | None = coda
        self._rime: Rime = self._generate_rime()

    @classmethod
    def from_nucleus_only(cls, nucleus: Nucleus) -> "Syllable":
        """
        Creates a new `Syllable` instance with only a given nucleus
        component.

        Parameters
        ----------
        - `nucleus`: the nucleus component of this syllable
        """
        s = Syllable(None, nucleus, None)
        return s

    @classmethod
    def from_onset_and_rime(cls, onset: Onset, rime: Rime) -> "Syllable":
        """
        Creates a new `Syllable` instance from a given onset and rime
        components.

        Parameters
        ----------
        - `onset`: the onset component of this syllable
        - `rime`: the rime component of this syllable, containing both
            the nucleus and coda
        """
        s = Syllable(onset, rime.nucleus, rime.coda)
        s._post_init(rime=rime)
        return s

    @property
    def coda(self) -> Coda | None:
        return self._coda

    @property
    def nucleus(self) -> Nucleus:
        return self._nucleus

    @property
    def onset(self) -> Onset | None:
        return self._onset

    @property
    def phones(self) -> tuple[Phoneme, ...]:
        return self._phonemes

    @property
    def rime(self) -> Rime:
        """
        The rime of this syllable. The rime either contains both
        the nucleus and a coda, or the nucleus only if there is no
        existing coda.
        """
        return self._rime

    def _create_transcript(self) -> str:
        t: str = ""
        for p in self._phonemes:
            t += p.symbol
        return f"/{t}/"

    def _generate_rime(self) -> Rime:
        """
        Returns the rime of this syllable. The rime either contains
        both the nucleus and a coda, or the nucleus only if there is no
        existing coda.
        """
        rime = Rime(self._nucleus, self._coda)
        self.add_substructure(rime)
        return rime

    def _post_init(self, rime: Rime | None = None) -> None:
        if rime is not None: self._rime = rime