from typing import Any


def tuple_append(t: tuple[Any, ...], item: Any) -> tuple[Any]:
    return tuple([*t, item])


def tuple_extend(t: tuple[Any, ...], collection: list[Any] | tuple[Any]) -> tuple[Any]:
    return tuple([*t, *collection])