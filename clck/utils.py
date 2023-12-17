from typing import Any


def strip_whitespace(s: str) -> str:
    """Returns the version of the given string `s` with all its
    whitespaces removed.

    Parameters
    ----------
    s : str
        the given string

    Returns
    -------
    str
        the version of the given string without all its whitespaces
    """
    return "".join(s.split())


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