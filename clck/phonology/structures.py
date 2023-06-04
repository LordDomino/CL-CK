from abc import ABC, abstractmethod
from typing import Any, Type

from .phonemes import Consonant, Phoneme, Vowel



class Structure(ABC):
    @abstractmethod
    def __init__(self, _allowed_types: list[type], *components: Any) -> None:
        """
        Creates a new instance of `Structure`.
        
        Arguments
        - `_component_types` are the permitted types of components.
        - `components` are the components.

        Raises
        - `TypeError` if any element in `components` is not of the allowed types
        in `_component_types`.
        """
        self._assert_components(tuple(components), _allowed_types)
        self._allowed_types: tuple[type] = tuple(_allowed_types)
        self._components: tuple[Structure | Phoneme, ...] = components
        self._substructures: tuple[Structure] = self._get_substructures()
        self._size: int = len(components)
        self._output: str = self._create_output()

    
    def __str__(self) -> str:
        return (f"{self.__class__.__name__} \033[1m{self._output}\033[0m of "
            f"components {self._components}")


    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} {self._output}>"


    @property
    def components(self) -> tuple[Any, ...]:
        return self._components


    @property
    def size(self) -> int:
        """The number of components of this structure."""
        return self._size
    

    @property
    def output(self) -> str:
        return self._output


    def find_phonemes(self, type: Type[Phoneme]) -> list[Phoneme]:
        rl: list[Phoneme] = []
        for s in self._components:
            if isinstance(s, type):
                rl.append(s)
            else:
                if isinstance(s, Structure):
                    rl.extend(s.find_phonemes(type))
        return rl


    def find_substructures(self, type: Type["Structure"]) -> list["Structure"]:
        rl: list[Structure] = []
        for s in self._substructures:
            if isinstance(s, type):
                rl.append(s)
            else:
                rl.extend(s.find_substructures(type))
        return rl


    def _assert_components(self, components: tuple[Any, ...],
        allowed_types: list[type]) -> bool:
        """
        Checks if the components are of the given types in `_component_types`.

        Arguments
        - `components` - the tuple of components to assert
        - `component_types` - the permitted types of components
        
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
                else:
                    mistype = True
            if mistype:
                raise TypeError(f"Component {c} is not of any type "
                    f"in {allowed_types}")

        return True


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


    def _get_substructures(self) -> tuple["Structure"]:
        rl: list[Structure] = []
        for c in self._components:
            if isinstance(c, Structure):
                rl.append(c)
        
        return tuple(rl)



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
        compoenents. Thus, note that during instantiation of the instance, the
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
    

    # def _create_output(self) -> str:
    #     """
    #     Creates the final string representation for this cluster based on its
    #     component phonemes.
    #     """
    #     phonemes: list[str] = []
    #     for p in self._phonemes:
    #         phonemes.append(p())
    #     return "".join(phonemes)


    def _check_cluster_size(self) -> bool:
        """Checks if the number of phonemes in the cluster is less than two."""
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



class Onset(SyllabicComponent):
    def __init__(self, *components: "SyllabicComponent | Consonant") -> None:
        super().__init__([SyllabicComponent, Consonant], *components)



class Nucleus(SyllabicComponent):
    def __init__(self, *components: SyllabicComponent | Vowel) -> None:
        super().__init__([SyllabicComponent, Vowel], *components)



class Coda(SyllabicComponent):
    def __init__(self, *components: SyllabicComponent | Consonant) -> None:
        super().__init__([Consonant], *components)



class Rhyme(SyllabicComponent):
    def __init__(self, nucleus: Nucleus, coda: Coda) -> None:
        super().__init__([Nucleus, Coda], nucleus, coda)
        self._nucleus: Nucleus = nucleus
        self._coda: Coda = coda


    @property
    def nucleus(self) -> Nucleus:
        return self._nucleus
    

    @property
    def coda(self) -> Coda:
        return self._coda



class Syllable(Structure):
    def __init__(self, onset: Onset, nucleus: Nucleus, coda: Coda) -> None:
        super().__init__([SyllabicComponent, Phoneme],
            onset, nucleus, coda)
        self._onset: Onset = onset
        self._nucleus: Nucleus = nucleus
        self._coda: Coda = coda
        self._phonemes: tuple[Phoneme] = tuple(self.find_phonemes(Phoneme))
        self._rhyme: Rhyme = Rhyme(self._nucleus, self._coda)


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


    def generate_rhyme(self) -> Rhyme | None:
        return Rhyme(self._nucleus, self._coda)


    def _post_init(self, rhyme: Rhyme | None = None) -> None:
        if rhyme is not None: self._rhyme = rhyme