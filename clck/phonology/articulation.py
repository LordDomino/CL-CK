from abc import ABC, abstractmethod
from typing import Any



class PhonologicalProperty(ABC):

    properties: list["PhonologicalProperty"] = []
    property_names: list[str] = []
    _id: int = 1
    
    @abstractmethod
    def __init__(self, name: str) -> None:
        super().__init__()
        self._name: str = name
        self._id: int = self.__class__._id
        
        self.__class__._increment_class_vars()
        self.__class__.properties.append(self)
        self.__class__.property_names.append(self._name)

    def __str__(self) -> str:
        return (f"{self.__class__.__name__} property (id={self._id}) "
            f"\"{self.name.capitalize()}\"")

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} (id={self._id}) \"{self._name}\">"

    @property
    @abstractmethod
    def value(self) -> Any: pass

    @property
    def name(self) -> str:
        return self._name
    
    @property
    def id(self) -> Any:
        return self._id

    @classmethod
    def _increment_class_vars(cls) -> None:
        cls._id += 1