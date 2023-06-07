from abc import ABC
from typing import Any, List

from ..phonology.containers import PhonemeGroup
from ..phonology.articulation import PhonologicalProperty
from ..phonology.phonemes import Phoneme


class Manager(ABC):

    global_list: List[Any] = []

    def __init__(self) -> None:
        self.elements: List[Any] = []


    def register(self, *items: Any) -> None:
        self.elements.extend(items)
        self.__class__.global_register(items)


    @classmethod
    def global_register(cls, *items: Any) -> None:
        cls.global_list.extend(items)



class PhonemesManager(Manager):

    global_list: List[Phoneme] = []
    """The global list of all phonemes across all `Language` instances."""


    def __init__(self) -> None:
        self.elements: List[Phoneme] = []


    def register(self, *phonemes: Phoneme) -> None:
        return super().register(*phonemes)



class PhonemeGroupsManager(Manager):

    global_list: List[PhonemeGroup] = []
    """The global list of all phoneme groups across all `Language` instances."""
    manager: "PhonemeGroupsManager | None" = None

    def __init__(self) -> None:
        super().__init__()
        if PhonemeGroupsManager.manager == None:
            PhonemeGroupsManager.manager = self

    
    def register(self, *phoneme_groups: PhonemeGroup) -> None:
        return super().register(*phoneme_groups)



class PropertiesManager(Manager):
    def __init__(self) -> None:
        super().__init__()
        self.elements: List[PhonologicalProperty] = []
        
        

class MorphemesManager(Manager): ...
class VocabularyManager(Manager): ...