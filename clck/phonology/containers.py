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
