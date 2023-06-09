from abc import ABC, abstractmethod
from typing import List, Tuple, Type
from .exceptions import InvalidLabelError

from clck.phonology.phonemes import Consonant, Vowel

from .containers import PhonemeGroup, PhonemeGroupsManager

from .phonemes import Consonant, Phoneme
from .phonemes import Vowel
from .structures import Structure


__all__ = [
    "Syllable",
    "Onset",
    "Nucleus",
    "Coda",
    "Rhyme",
    "ConsonantCluster",
    "PhonemeCluster",
    "VowelCluster",
    "Diphthong",
    "Triphthong",
]



class Pattern:
    def __init__(self, string: str) -> None:
        self._check_pattern_validity(string)
        self._string: str = string
        self._symbols: list[str] = [*self._generate_symbols()]
        self._phoneme_groups: list[PhonemeGroup] = self._get_phoneme_groups()
        self._phonemes: list[Phoneme] = list(set(self._get_phonemes()))

    
    @property
    def pattern_string(self):
        return self._string


    @property
    def phoneme_groups(self) -> tuple[PhonemeGroup]:
        """The tuple of PhonemeGroup instances used in this pattern."""
        return tuple(self._phoneme_groups)


    @property
    def phonemes(self) -> tuple[Phoneme]:
        return tuple(self._phonemes)


    @property
    def string(self) -> str:
        return self._string


    @property
    def symbols(self) -> list[str]:
        return self._symbols


    def _check_pattern_validity(self, string: str) -> bool:
        for char in string:
            if char not in PhonemeGroupsManager.labels:
                raise ValueError(f"Unknown pattern label \"{char}\" in pattern "
                    f"string \"{string}\"")
        return True
    

    def _generate_symbols(self) -> tuple[str]:
        l: list[str] = []
        for char in self._string:
            l.append(char)
        return tuple(l)


    def _get_phoneme_groups(self) -> list[PhonemeGroup]:
        g: list[PhonemeGroup] = []
        for symbol in self._symbols:
            for phoneme_group in PhonemeGroupsManager.global_list:
                if symbol == phoneme_group.label:
                    g.append(phoneme_group)
                    break
        return g


    def _get_phonemes(self) -> list[Phoneme]:
        l: list[Phoneme] = []
        for pg in self._phoneme_groups:
            l.extend(pg.phonemes)
        return l




class Shape:
    def __init__(self, _comps_type: Type[Consonant | Vowel],
            pattern_string: str) -> None:
        self._comps_type: Type[Consonant] | Type[Vowel] = _comps_type
        self._pattern: Pattern = Pattern(pattern_string)
        self._pattern_string: str = self._pattern.string
        self._length: int = len(self._pattern.symbols)

        try:
            self._check_phoneme_types()
        except TypeError as e:
            raise InvalidLabelError(f"Invalid phoneme type {e.args[1]}. "
                f"Expected only {self._comps_type.__name__} for type "
                f"{self.__class__.__name__}")


    @property
    def length(self) -> int:
        return self._length


    @property
    def pattern(self) -> Pattern:
        return self._pattern
    

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
        super().__init__(Consonant, pattern)



class NucleusShape(Shape):
    def __init__(self, pattern: str) -> None:
        super().__init__(Vowel, pattern)



class CodaShape(Shape):
    def __init__(self, pattern: str) -> None:
        super().__init__(Consonant, pattern)



class SyllableShape:
    def __init__(self, onset: OnsetShape | None, nucleus: NucleusShape,
            coda: CodaShape | None) -> None:
        self._onset: OnsetShape | None = onset
        self._nucleus: NucleusShape = nucleus
        self._coda: CodaShape | None = coda

        shapes: list[str] = []

        if onset is not None:
            shapes.append(onset.pattern.string)
        if coda is not None:
            shapes.append(coda.pattern.string)
        shapes.append(nucleus.pattern.string)

        self._pattern: str = "".join(shapes)


    @property
    def pattern(self) -> str:
        return self._pattern
    

    @property
    def onset_shape(self) -> OnsetShape | None:
        return self._onset
    

    @property
    def nucleus_shape(self) -> NucleusShape:
        return self._nucleus


    @property
    def coda_shape(self) -> CodaShape | None:
        return self._coda


    def get_onc_lengths(self) -> Tuple[int, int, int]:
        if self._onset is None:
            o = 0
        else:
            o = self._onset.length

        if self._coda is None:
            c = 0
        else:
            c = self._coda.length

        return (o, self._nucleus.length, c)



class SyllabicComponent(Structure, ABC):
    """
    Class for `SyllabicComponent`.
    A syllabic component is any component that comprises a syllable, such as
    phonemes and phoneme clusters.
    """
    @abstractmethod
    def __init__(self,
            _allowed_types: List[Type["SyllabicComponent | Phoneme"]],
            *components: "SyllabicComponent | Phoneme") -> None:
        super().__init__(_allowed_types, *components)


    def get_phonemes(self) -> list[Phoneme]:
        phonemes: list[Phoneme] = []
        for component in self._components:
            if isinstance(component, Phoneme):
                phonemes.append(component)
            elif isinstance(component, SyllabicComponent):
                component.get_phonemes()
        return phonemes


    def remove_duplicates(self) -> None:
        self._components = [*set(self._components)]


    def _create_transcript(self) -> str:
        t: str = ""
        for c in self._components:
            if isinstance(c, Phoneme):
                t += c.transcript
            else:
                t += c._create_transcript()
        return t



class Onset(SyllabicComponent):
    def __init__(self, *components: "SyllabicComponent | Consonant") -> None:
        super().__init__([SyllabicComponent, Consonant], *components)



class Nucleus(SyllabicComponent):
    def __init__(self, *components: SyllabicComponent | Vowel) -> None:
        super().__init__([SyllabicComponent, Vowel], *components)



class PhonemeCluster(SyllabicComponent):
    def __init__(self, allowed_type: Type[Phoneme],
            *components: Phoneme) -> None:
        """
        Creates a new instance of `Cluster`.
        
        Arguments
        - `component_type` is the type of the components.
        - `phonemes` are the component phonemes of this cluster.
        
        Raises
        - `TypeError` if any element in `phonemes` is not of the given type,
        `component_type`.
        
        A cluster logically exists as a group of at least two phoneme
        components. Thus, note that during instantiation of the instance, the
        constructor checks if the number of given phonemes are not below two.
        """
        super().__init__(list([allowed_type]), *components)
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
        Checks if the number of phonemes in the cluster is less than two.
        
        Raises
        - `ValueError` if the number of clusters is less than two.
        """
        if len(self.phonemes) < 2:
            raise ValueError(f"Cannot create {self.__class__.__name__} with "
                f"less than 2 items. Insufficient amount of items "
                f"({len(self._phonemes)}).")
        else:
            return True



class ConsonantCluster(PhonemeCluster):
    """
    Class for `ConsonantCluster`, a special type of phoneme cluster to enclose
    multiple consonants.
    """
    def __init__(self, *consonants: Phoneme) -> None:
        super().__init__(Consonant, *consonants)



class VowelCluster(PhonemeCluster):
    """
    Class for `VowelCluster`, a special type of phoneme cluster to enclose
    multiple vowels.
    """
    def __init__(self, *vowels: Vowel) -> None:
        super().__init__(Vowel, *vowels)



class Diphthong(VowelCluster):
    """
    Class for `Diphthong` objects.
    A diphthong is a combination of two vowels.
    """
    def __init__(self, vowel_1: Vowel, vowel_2: Vowel) -> None:
        super().__init__(vowel_1, vowel_2)



class Triphthong(VowelCluster):
    """
    Class for `Triphthong` objects.
    A triphthong is a combination of three vowels.
    """
    def __init__(self, vowel_1: Vowel, vowel_2: Vowel, vowel_3: Vowel) -> None:
        super().__init__(vowel_1, vowel_2, vowel_3)



class Coda(SyllabicComponent):
    def __init__(self, *components: SyllabicComponent | Consonant) -> None:
        super().__init__([Consonant], *components)



class Rhyme(SyllabicComponent):
    def __init__(self, nucleus: Nucleus, coda: Coda | None) -> None:
        if coda is None:
            super().__init__([Nucleus, Coda], nucleus)
        else:
            super().__init__([Nucleus, Coda], nucleus, coda)
        self._nucleus: Nucleus = nucleus
        self._coda: Coda | None = coda


    @property
    def nucleus(self) -> Nucleus:
        """The nucleus component of this object."""
        return self._nucleus


    @property
    def coda(self) -> Coda | None:
        """The coda component of this object."""
        return self._coda


    def _create_transcript(self) -> str:
        t: str = ""
        for c in self._phonemes:
            t += c.symbol
        return f"/{t}/"


class Syllable(Structure):
    def __init__(self, onset: Onset | None, nucleus: Nucleus,
        coda: Coda | None) -> None:
        super().__init__([SyllabicComponent, Phoneme], onset, nucleus, coda)
        self._phonemes: tuple[Phoneme] = tuple(self.find_phonemes(Phoneme))
        self._onset: Onset | None = onset
        self._nucleus: Nucleus = nucleus
        self._coda: Coda | None = coda
        self._rhyme: Rhyme = self._generate_rhyme(nucleus, coda)
        self._transcript: str = self._create_transcript()


    @classmethod
    def from_nucleus_only(cls, nucleus: Nucleus) -> "Syllable":
        s = Syllable(None, nucleus, None)
        return s


    @classmethod
    def from_onset_and_rhyme(cls, onset: Onset, rhyme: Rhyme) -> "Syllable":
        s = Syllable(onset, rhyme.nucleus, rhyme.coda)
        s._post_init(rhyme=rhyme)
        return s


    @property
    def phonemes(self) -> tuple[Phoneme]:
        return self._phonemes


    @property
    def rhyme(self) -> Rhyme | None:
        return self._rhyme


    def _create_transcript(self) -> str:
        t: str = ""
        for p in self._phonemes:
            t += p.symbol
        return f"/{t}/"


    def _generate_rhyme(self, nucleus: Nucleus, coda: Coda | None) -> Rhyme:
        rhyme = Rhyme(nucleus, coda)
        self.add_substructure(rhyme)
        return rhyme


    def _post_init(self, rhyme: Rhyme | None = None) -> None:
        if rhyme is not None: self._rhyme = rhyme