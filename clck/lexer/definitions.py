from enum import Enum


class StandardToken(Enum): ...
class Repeatable(StandardToken): ...
class Identifier(StandardToken): ...

class GroupingIdentifier(Identifier):
    PROBABILITY_GROUP_OPEN = "("
    PROBABILITY_GROUP_CLOSE = ")"


class PhonemeGroupIdentifier(Identifier):
    CONSONANTS = "C"
    VOWELS = "V"


def get_longest_token_len() -> int:
    """
    Returns the length of the longest token defined in `StandardToken`.
    """
    max_len: int = 0
    for enum in StandardToken:
        if len(enum.value) > max_len:
            max_len = len(enum.value)
    return max_len


def get_valid_chars() -> tuple[str, ...]:
    """
    Returns a tuple of all valid characters acceptable in a string
    formula.
    """
    chars: list[str] = []
    for enum in StandardToken:
        chars.append(enum.value)
    return tuple(set(chars))


VALID_CHARS: tuple[str, ...] = get_valid_chars()