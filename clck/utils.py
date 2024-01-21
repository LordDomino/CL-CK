from typing import TypeVar


T = TypeVar("T")


def clean_collection(c: list[T] | tuple[T, ...]) -> tuple[T, ...]:
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
        if e:
            temp.append(e)
    return tuple(temp)


def filter_none(collection: list[T] | tuple[T, ...]) -> tuple[T, ...]:
    """Returns a modified version of the given collection in which all
    `None` or `NoneType` values are removed.
    """
    rl: list[T] = []
    for c in collection:
        if c is not None:
            rl.append(c)
    return tuple(rl)


def get_classes(collection: list[T] | tuple[T, ...]) -> tuple[type, ...]:
    rl: list[type] = []
    for c in collection:
        rl.append(c.__class__)
    return tuple(rl)


def get_types(collection: list[T] | tuple[T, ...]) -> tuple[type, ...]:
    """Returns all the found types of all the elements in the
    collection.

    Parameters
    ----------
    collection : list[T] | tuple[T, ...]
        the given list or tuple

    Returns
    -------
    tuple[type, ...]
        the tuple of all types found in the given list or tuple
    """
    types: list[type] = []
    for o in collection:
        types.append(o.__class__)
    return tuple(types)

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


def tuple_append(t: tuple[T, ...], item: T) -> tuple[T, ...]:
    """
    Provides a functionality to append items to a tuple.
    """
    return tuple([*t, item])


def tuple_extend(t: tuple[T, ...], collection: list[T] | tuple[T, ...]) -> tuple[T, ...]:
    """
    Provides a functionality to extend a collection to a tuple.
    """
    return tuple([*t, *collection])