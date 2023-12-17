from enum import Enum


STANDARD_TOKENS: list["StandardToken"] = []
"""The list of all recognized `StandardToken` enum members"""


class StandardToken(Enum):
    @classmethod
    def register_enums_from_classes(cls,
        enum_classes: tuple[type["StandardToken"], ...]) -> None:
        """Registers all defined enumerations from the given enum
        classes in `enum_classes`.

        Parameters
        ----------
        enum_classes : tuple[type[StandardToken], ...]
            the tuple of `StandardToken` enum classes where the
            enumerations are defined
        """
        for enum_cls in enum_classes:
            for enum in enum_cls:
                STANDARD_TOKENS.append(enum)


class Repeatable(StandardToken): ...
class Identifier(StandardToken): ...

class GroupingIdentifier(Identifier):
    PROBABILITY_GROUP_OPEN = "("
    PROBABILITY_GROUP_CLOSE = ")"


class PhonemeGroupIdentifier(Identifier):
    CONSONANTS = "C"
    VOWELS = "V"


ENUM_CLASSES: tuple[type[StandardToken], ...] = (
    GroupingIdentifier,
    PhonemeGroupIdentifier,
)
"""The tuple of all `StandardToken` enum classes"""

StandardToken.register_enums_from_classes(ENUM_CLASSES)


def get_longest_token_len() -> int:
    """Returns the length of the longest token defined under the enum
    class `StandardToken`.

    Returns
    -------
    int
        the length of the longest token defined under the enum class
        `StandardToken`
    """
    max_len: int = 0
    for enum in STANDARD_TOKENS:
        if len(enum.value) > max_len:
            max_len = len(str(enum.value))
    return max_len


def get_valid_chars() -> tuple[str, ...]:
    """Returns a tuple of all valid characters acceptable in a string
    formula.

    Returns
    -------
    tuple[str, ...]
        the tuple of all valid characters acceptable in a formula
    """
    chars: list[str] = []
    for enum in StandardToken:
        chars.append(enum.value)
    return tuple(set(chars))


VALID_CHARS: tuple[str, ...] = get_valid_chars()
"""The tuple of all valid characters acceptable in a string formula."""