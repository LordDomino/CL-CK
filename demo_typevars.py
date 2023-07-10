from typing import TypeVar


class ObjectType1:
    def __init__(self) -> None:
        self.attribute_1 = 1


class ObjectType2:
    def __init__(self) -> None:
        self.attribute_2 = 2


C = TypeVar("C", ObjectType1, ObjectType2)

class Container:
    def __init__(self, objects: list[C]) -> None:
        self.objects: list[C] = objects



cont = Container([ObjectType1(), ObjectType2()])

object1 = cont.objects[0]
print(object1.attribute_1)