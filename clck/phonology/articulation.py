from abc import ABC, abstractmethod
from typing import Any


__all__ = [
    "PhonologicalProperty", "ArticulatoryProperty", "Voicing",
    "ConsonantalProperty", "VocalicProperty", "Manner", "Place", "AirflowType",
    "AirstreamMechanism", "Height", "Backness", "Roundedness",
]



class PhonologicalProperty(ABC):

    properties: list["PhonologicalProperty"] = []
    _id: int = 1
    
    @abstractmethod
    def __init__(self, name: str) -> None:
        super().__init__()
        self._name: str = name
        self._id: int = self.__class__._id
        
        self.__class__._increment_class_vars()
        self.__class__.properties.append(self)


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



class ArticulatoryProperty(PhonologicalProperty):
    def __init__(self, name: str) -> None:
        super().__init__(name)



class Voicing(ArticulatoryProperty):
    def __init__(self, name: str, value: int) -> None:
        self._value: int = value
        super().__init__(name)

    
    @property
    def value(self) -> int:
        return self._value



class ConsonantalProperty(ArticulatoryProperty):
    def __init__(self, name: str) -> None:
        super().__init__(name)



class VocalicProperty(ArticulatoryProperty):
    def __init__(self, name: str) -> None:
        super().__init__(name)



class Manner(ConsonantalProperty):
    def __init__(self, name: str, value: int) -> None:
        self._value: int = value
        super().__init__(name)


    @property
    def value(self) -> int:
        return self._value



class Place(ConsonantalProperty):
    def __init__(self, name: str, range: tuple[int, int] | int) -> None:
        if isinstance(range, tuple):
            self._min: int = range[0]
            self._max: int = range[1]
        else:
            self._min: int = range
            self._max: int = range
        super().__init__(name)


    @property
    def value(self) -> tuple[int, ...]:
        return tuple(range(self._min, self._max + 1))



class AirflowType: ...



class AirstreamMechanism(ConsonantalProperty):
    def __init__(self, name: str, value: float, airflow: AirflowType) -> None:
        self._value: float = value
        self._airflow: AirflowType = airflow
        super().__init__(name)

    
    @property
    def value(self) -> float:
        return self._value



class Height(VocalicProperty):
    def __init__(self, name: str, value: float) -> None:
        self._value: float = value
        super().__init__(name)


    @property
    def value(self) -> float:
        return self._value    



class Backness(VocalicProperty):
    def __init__(self, name: str, value: float) -> None:
        self._value: float = value
        super().__init__(name)


    @property
    def value(self) -> float:
        return self._value


class Roundedness(VocalicProperty):
    def __init__(self, name: str, value: float) -> None:
        self._value: float = value
        super().__init__(name)


    @property
    def value(self) -> float:
        return self._value



