from typing import Any


def tuple_append(t: tuple[Any, ...], item: Any) -> tuple[Any, ...]:
    """
    Provides a functionality to append items to a tuple.
    """
    return tuple([*t, item])


def tuple_extend(t: tuple[Any, ...], collection: list[Any] | tuple[Any, ...]) -> tuple[Any, ...]:
    """
    Provides a functionality to extend a collection to a tuple.
    """
    return tuple([*t, *collection])