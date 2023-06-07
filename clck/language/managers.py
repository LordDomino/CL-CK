

from abc import ABC, abstractmethod
from typing import Any, List

from ..phonology.containers import PhonemeGroup
from ..phonology.phonemes import Phoneme


class Manager(ABC):
    def __init__(self) -> None:
        self.elements: List[Any] = []


    @abstractmethod
    def register(self, *items: Any) -> None:
        pass


    @staticmethod
    @abstractmethod
    def global_register(*items: Any) -> None:
        pass



class PhonemesManager(Manager):

    global_phonemes: List[Phoneme] = []
    """The global list of all phonemes across all `Language` instances."""


    def __init__(self) -> None:
        self.list: List[Phoneme] = []


    def register(self, *phonemes: Phoneme) -> None:
        """
        Appens the given phonemes to this specific `PhonemeManager`'s index.

        Parameters
        ----------
        - `phonemes` - the phonemes instances to be appended.
        """
        self.list.extend(phonemes)
        PhonemesManager.global_register(*phonemes)


    @staticmethod
    def global_register(*phonemes: Phoneme) -> None:
        """
        Appends the given phonemes to the global index of phonemes.

        Parameters
        ----------
        - `phonemes` - the phoneme instances to be appended.
        """
        PhonemesManager.global_phonemes.extend(phonemes)


class PhonemeGroupsManager(Manager):

    global_phonemegroups: List[PhonemeGroup] = []
    """The global list of all phoneme groups across all `Language` instances."""


    def __init__(self) -> None:
        super().__init__()
        self.list: List[PhonemeGroup] = []


    def register(self, *phoneme_groups: PhonemeGroup) -> None:
        self.list.extend(phoneme_groups)
        PhonemeGroupsManager.global_register(*phoneme_groups)

    @staticmethod
    def global_register(*phoneme_groups: PhonemeGroup) -> None:
        PhonemeGroupsManager.global_phonemegroups.extend(phoneme_groups)

class PropertiesManager(Manager): ...
class MorphemesManager(Manager): ...
class VocabularyManager(Manager): ...