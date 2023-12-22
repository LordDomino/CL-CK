from typing import Any, TypeVar


T = TypeVar("T")


def clean_collection(c: list[T]) -> tuple[T, ...]:
    """Returns the version of the given collection of either a list or
    tuple without all `None` or empty string elements.

    Parameters
    ----------
    c : list[T] | tuple[T, ...]
        the list or tuple to remove all `None` or empty string elements
        from

    Returns
    -------
    tuple[T, ...]
        the tuple version of the given list or tuple without all its
        `None` or empty string elements
    """
    temp: list[T] = []
    for e in c:
        if e != "":
            temp.append(e)
    return tuple(temp)


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