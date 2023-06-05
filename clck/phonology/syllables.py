from abc import ABC, abstractmethod
from typing import Type

from .phonemes import Consonant, Phoneme
from .phonemes import Vowel
from .structures import Structure



class SyllableShape:
    def __init__(self, onset: str, nucleus: str, coda: str) -> None:
        self._onset: str = onset
        self._nucleus: str = nucleus
        self._coda: str = coda
        self._pattern: str = "".join([self._onset, self._nucleus, self._coda]).upper()
        self._length: int = len(self._pattern)
        self._pattern_types: list[str] = list(set(self._pattern))


    @property
    def pattern(self) -> str:
        return self._pattern
    

    @property
    def length(self) -> int:
        return self._length
    

    @property
    def onset_shape(self) -> str:
        return self._onset
    

    @property
    def nucleus_shape(self) -> str:
        return self._nucleus


    @property
    def coda_shape(self) -> str:
        return self._coda


class SyllabicComponent(Structure, ABC):
    """
    Class for `SyllabicComponent`.
    A syllabic component is any component that comprises a syllable, such as
    phonemes and phoneme clusters.
    """
    @abstractmethod
    def __init__(self,
            _allowed_types: list[Type["SyllabicComponent | Phoneme"]],
            *components: "SyllabicComponent | Phoneme") -> None:
        super().__init__(_allowed_types, *components)
        self._components: tuple[SyllabicComponent | Phoneme, ...] = components


    def get_phonemes(self) -> list[Phoneme]:
        phonemes: list[Phoneme] = []
        for component in self._components:
            if isinstance(component, Phoneme):
                phonemes.append(component)
            else:
                component.get_phonemes()
        return phonemes


    def remove_duplicates(self) -> None:
        self._components = tuple([*set(self.components)])


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


class Syllable(Structure):
    def __init__(self, onset: Onset | None, nucleus: Nucleus,
        coda: Coda | None) -> None:
        super().__init__([SyllabicComponent, Phoneme], onset, nucleus, coda)
        self._onset: Onset | None = onset
        self._nucleus: Nucleus = nucleus
        self._coda: Coda | None = coda
        self._phonemes: tuple[Phoneme] = tuple(self.find_phonemes(Phoneme))
        self._rhyme: Rhyme = Rhyme(self._nucleus, self._coda)


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


    def _post_init(self, rhyme: Rhyme | None = None) -> None:
        if rhyme is not None: self._rhyme = rhyme