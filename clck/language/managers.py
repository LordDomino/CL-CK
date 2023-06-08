from abc import ABC
from typing import Any, List

from ..phonology.articulation import PhonologicalProperty
from ..phonology.phonemes import Phoneme


class Manager(ABC):

    global_list: List[Any] = []

    def __init__(self) -> None:
        self.elements: List[Any] = []


    def register(self, *items: Any) -> None:
        self.elements.extend(items)
        self.__class__.global_register(*items)


    @classmethod
    def global_register(cls, *items: Any) -> None:
        cls.global_list.extend(items)



class PhonemesManager(Manager):

    global_list: List[Phoneme] = []
    """The global list of all phonemes across all `Language` instances."""


    def __init__(self) -> None:
        self.elements: List[Phoneme] = []


    def register(self, *phonemes: Phoneme) -> None:
        super().register(*phonemes)


    @classmethod
    def global_register(cls, *phonemes: Phoneme) -> None:
        super().global_register(*phonemes)



class PropertiesManager(Manager):

    global_list: List[PhonologicalProperty] = []

    def __init__(self) -> None:
        super().__init__()
        self.elements: List[PhonologicalProperty] = []

    
    def register(self, *items: Any) -> None:
        return super().register(*items)
    

    @classmethod
    def global_register(cls, *items: Any) -> None:
        return super().global_register(*items)
        
        

class MorphemesManager(Manager): ...
class VocabularyManager(Manager): ...