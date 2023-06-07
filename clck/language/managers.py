

from abc import ABC, abstractmethod
from typing import Any, List

from ..phonology.articulation import PhonologicalProperty

from ..phonology.containers import PhonemeGroup
from ..phonology.phonemes import Phoneme


class Manager(ABC):

    global_list: List[Any] = []

    def __init__(self) -> None:
        self.elements: List[Any] = []


    @abstractmethod
    def register(self, *items: Any) -> None:
        self._register(*items)


    @classmethod
    @abstractmethod
    def global_register(cls, *items: Any) -> None:
        cls._global_register(*items)


    def _register(self, *items: Any) -> None:
        self.elements.extend(items)
        self.__class__.global_list


    @classmethod
    def _global_register(cls, *items: Any) -> None:
        cls.global_list.extend(items)



class PhonemesManager(Manager):

    global_list: List[Phoneme] = []
    """The global list of all phonemes across all `Language` instances."""


    def __init__(self) -> None:
        self.elements: List[Phoneme] = []


    def register(self, *phonemes: Phoneme) -> None:
        """
        Appens the given phonemes to this specific `PhonemeManager`'s index.

        Parameters
        ----------
        - `phonemes` - the phonemes instances to be appended.
        """
        self.elements.extend(phonemes)
        PhonemesManager.global_register(*phonemes)


    @classmethod
    def global_register(cls, *phonemes: Phoneme) -> None:
        """
        Appends the given phonemes to the global index of phonemes.

        Parameters
        ----------
        - `phonemes` - the phoneme instances to be appended.
        """
        PhonemesManager.global_list.extend(phonemes)


class PhonemeGroupsManager(Manager):

    global_list: List[PhonemeGroup] = []
    """The global list of all phoneme groups across all `Language` instances."""


    def __init__(self) -> None:
        super().__init__()
        self.elements: List[PhonemeGroup] = []


    def register(self, *phoneme_groups: PhonemeGroup) -> None:
        self.elements.extend(phoneme_groups)
        PhonemeGroupsManager.global_register(*phoneme_groups)

    @classmethod
    def global_register(cls, *phoneme_groups: PhonemeGroup) -> None:
        PhonemeGroupsManager.global_list.extend(phoneme_groups)

class PropertiesManager(Manager):
    def __init__(self) -> None:
        super().__init__()
        self.elements: List[PhonologicalProperty] = []

    
    def register(self, *property: PhonologicalProperty) -> None:
        self.elements.extend


    @classmethod
    def global_register(cls, *property: PhonologicalProperty) -> None: ...
        

class MorphemesManager(Manager): ...
class VocabularyManager(Manager): ...