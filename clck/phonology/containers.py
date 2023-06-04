from abc import ABC, abstractmethod
from typing import Type
from clck.phonology.phonemes import Phoneme, Vowel
from .phonemes import *



class PhonologicalInventory:
    def __init__(self, *phonemes: Phoneme) -> None:
        self._phonemes: tuple[Phoneme] = phonemes
        self._consonants: tuple[Consonant] = self._get_consonants()
        self._vowels: tuple[Vowel] = self._get_vowels()


    @property
    def phonemes(self) -> tuple[Phoneme]:
        return self._phonemes
    

    @property
    def consonants(self) -> tuple[Consonant]:
        return self._consonants


    @property
    def vowels(self) -> tuple[Vowel]:
        return self._vowels
    

    def _get_consonants(self) -> tuple[Consonant]:
        consonants: list[Consonant] = []
        for phoneme in self._phonemes:
            if isinstance(phoneme, Consonant):
                consonants.append(phoneme)
        return tuple(consonants)
    

    def _get_vowels(self) -> tuple[Vowel]:
        vowels: list[Vowel] = []
        for phoneme in self._phonemes:
            if isinstance(phoneme, Vowel):
                vowels.append(phoneme)
        return tuple(vowels)



class Cluster(ABC):
    @abstractmethod
    def __init__(self, assert_type: Type[Phoneme], *phonemes: Phoneme) -> None:
        self._phonemes: tuple[Phoneme] = phonemes
        self._assert_items(assert_type)
        self._symbol: str = self._create_symbol()


    def __str__(self) -> str:
        return f"{self.__class__.__name__} \033[1m{self._symbol}\033[0m of phonemes {self._phonemes}"


    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} {self._symbol}>"
    



    @property
    def phonemes(self) -> tuple[Phoneme]:
        return self._phonemes
    

    @property
    def symbol(self) -> str:
        return self._symbol


    def _create_symbol(self) -> str:
        phonemes: list[str] = []
        for phoneme in self._phonemes:
            phonemes.append(phoneme())
        return "".join(phonemes)
    

    def _assert_items(self, assert_type: Type[Phoneme]) -> bool:
        self._check_cluster_size()
        self._check_types(assert_type)
        return True

    def _check_types(self, assert_type: Type[Phoneme]) -> bool:
        for item in self._phonemes:
            if not isinstance(item, assert_type):
                raise TypeError(f"Cannot create {self.__class__.__name__} because {item.__repr__()} is not of type {assert_type.__name__}")
        return True


    def _check_cluster_size(self) -> bool:
        if len(self._phonemes) < 2:
            raise ValueError(f"Cannot create {self.__class__.__name__} with less than 2 items. Insufficient amount of items ({len(self._phonemes)}).")
        else:
            return True



class ConsonantCluster(Cluster):
    def __init__(self, *consonants: Consonant) -> None:
        super().__init__(Consonant, *consonants)
        


class VowelCluster(Cluster):
    def __init__(self, *vowels: Vowel) -> None:
        super().__init__(Vowel, *vowels)



class Diphthong(VowelCluster):
    def __init__(self, vowel_1: Vowel, vowel_2: Vowel) -> None:
        super().__init__(vowel_1, vowel_2)