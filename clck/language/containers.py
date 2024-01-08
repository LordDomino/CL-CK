from typing import List, Type

from clck.articulation import PhonologicalProperty
from clck.language.managers import Manager
from clck.phonetics.phones import *
from clck.phonology.phonemes import Phoneme


class PhonemeGroupsManager(Manager):

    global_list: List["PhonemeGroup"] = []
    """
    The global list of all phoneme groups across all `Language`
    instances.
    """

    labels: List[str] = []

    @classmethod  
    def global_register(cls, *phoneme_groups: "PhonemeGroup") -> None:
        for pg in phoneme_groups:
            PhonemeGroupsManager.labels.append(pg.label)
        return super().global_register(*phoneme_groups)


class PhonemeGroup:
    def __init__(self, label: str, *phonemes: Phoneme) -> None:
        self._label: str = label
        self._phonemes: tuple[Phoneme, ...] = phonemes

        PhonemeGroupsManager.global_register(self)

    @classmethod
    def from_type(cls, label: str, phoneme_type: Type[Phoneme]) -> "PhonemeGroup":
        phonemes: list[Phoneme] = []

        for phoneme in Phoneme.DEFAULT_IPA_PHONEMES:
            if isinstance(phoneme, phoneme_type):
                phonemes.append(phoneme)

        return PhonemeGroup(label, *phonemes)
    
    @classmethod
    def from_property(cls, label: str, *property_names: str) -> "PhonemeGroup":
        phonemes: list[Phoneme] = []

        for name in property_names:
            cls._check_prop_name_existence(name)

        for phoneme in Phoneme.DEFAULT_IPA_PHONEMES:
            if all(name in phoneme.base_phone.articulatory_property_names
                for name in property_names): 
                phonemes.append(phoneme)

        return PhonemeGroup(label, *phonemes)

    def __repr__(self) -> str:
        phonemes: list[str] = []
        for phoneme in self._phonemes:
            phonemes.append(phoneme.symbol)
        return f"<PhonemeGroup \"{self._label}\" ({' '.join(phonemes)})>"

    def __str__(self) -> str:
        phonemes: list[str] = []
        for phoneme in self._phonemes:
            phonemes.append(phoneme.ipa_transcript)
        return f"PhonemeGroup \"{self._label}\" containing phonemes {', '.join(phonemes)}"

    @property
    def label(self) -> str:
        return self._label

    @property
    def phonemes(self) -> tuple[Phoneme, ...]:
        return self._phonemes
    
    @staticmethod
    def _check_prop_name_existence(name: str) -> bool:
        if name not in PhonologicalProperty.property_names:
            raise ValueError(f"Property name \"{name}\" does not exist")
        return True

