from typing import Type

import clck.ipa_phonemes as ipa_phonemes

from .phonemes import *


class PhonologicalInventory:
    def __init__(self, *phonemes: Phoneme) -> None:
        self._phonemes: tuple[Phoneme] = phonemes
        self._consonants: tuple[Consonant] = self._get_consonants()
        self._vowels: tuple[Vowel] = self._get_vowels()
    

    @property
    def consonants(self) -> tuple[Consonant]:
        return self._consonants


    @property
    def phonemes(self) -> tuple[Phoneme]:
        return self._phonemes


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



class PhonemeGroup:

    groups: list["PhonemeGroup"] = []

    def __init__(self, label: str, *phonemes: Phoneme) -> None:
        self._label: str = label
        self._phonemes: tuple[Phoneme] = phonemes

        PhonemeGroup.groups.append(self)


    @staticmethod
    def from_type(label: str, phoneme_type: Type[Phoneme]) -> "PhonemeGroup":
        phonemes: list[Phoneme] = []

        for phoneme in ipa_phonemes.DEFAULT_IPA_PHONEMES:
            if isinstance(phoneme, phoneme_type):
                phonemes.append(phoneme)

        return PhonemeGroup(label, *phonemes)
    

    @staticmethod
    def from_property(label: str, articulatory_property_name: str) -> "PhonemeGroup":
        phonemes: list[Phoneme] = []

        for phoneme in ipa_phonemes.DEFAULT_IPA_PHONEMES:
            if articulatory_property_name in phoneme._property_names:
                phonemes.append(phoneme)

        return PhonemeGroup(label, *phonemes)


DEFAULT_PATTERN_WILDCARDS: dict[str, PhonemeGroup] = {
    "C" : PhonemeGroup.from_type("C", Consonant),
    "V" : PhonemeGroup.from_type("V", Vowel),
    "N" : PhonemeGroup.from_property("N", "nasal"),
    "A" : PhonemeGroup.from_property("A", "approximant"),
    "S" : PhonemeGroup.from_property("S", "stop")
}