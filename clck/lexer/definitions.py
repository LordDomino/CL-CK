from dataclasses import dataclass
from enum import Enum
from enum import auto
import string
from typing import TypeVar


T = TypeVar("T")


STANDARD_TOKENS: list["StandardTokens"] = []
"""The list of all recognized `StandardToken` enum members"""


class SyntaxObjectTypes(Enum):
    TOKEN = auto()
    STRUCTURE = auto()
    PHONEME = auto()

class StandardTokens(Enum):

    @classmethod
    def get_all_subclasses(cls) -> tuple[type["StandardTokens"], ...]:
        temp: list[type[StandardTokens]] = []

        temp.extend(cls.__subclasses__())
        for c in cls.__subclasses__():
            temp.extend(c.get_all_subclasses())

        return tuple(temp)

    @staticmethod
    def register_enums_from_classes(
        enum_classes: tuple[type["StandardTokens"], ...]) -> None:
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

    @staticmethod
    def get_valid_chars() -> tuple[str, ...]:
        """Returns a tuple of all valid characters acceptable in a
        string formula.

        Returns
        -------
        tuple[str, ...]
            the tuple of all valid characters acceptable in a formula
        """

        chars: list[str] = []
        for enum_class in StandardTokens.get_all_subclasses():
            for enum in enum_class:
                if isinstance(enum.value, str):
                    chars.extend(list(enum.value))

        return tuple(set(chars))
    
    @staticmethod
    def get_longest_token_len() -> int:
        """Returns the length of the longest token defined under the
        enum class `StandardToken`.

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
    
    @staticmethod
    def get_enum_classes_by_type(cls_type: type[T]) -> tuple[type[T], ...]:
        """Returns a tuple of enum classes that are subclasses of the
        given superclass type `cls_type`.

        Parameters
        ----------
        cls_type : type[T]
            the superclass type of the enum classes to be retrieved

        Returns
        -------
        tuple[type[T], ...]
            the tuple of enum classes that are subclasses of the given
            superclass type
        """
        temp: list[type[T]] = []
        for c in StandardTokens.get_all_subclasses():
            if issubclass(c, cls_type):
                temp.append(c)

        return tuple(temp)
    
    @staticmethod
    def get_identifier_classes() -> tuple[type["Identifiers"], ...]:
        return StandardTokens.get_enum_classes_by_type(Identifiers)

    @staticmethod
    def get_wildcard_classes() -> tuple[type["Wildcards"], ...]:
        return StandardTokens.get_enum_classes_by_type(Wildcards)
    
    @staticmethod
    def get_tokens_by_type(cls_type: type["StandardTokens"]) -> tuple[str, ...]:
        """Returns the tuple of strings representing the tokens of the
        given type `cls_type`.

        Parameters
        ----------
        cls_type : type[&quot;StandardTokens&quot;]
            the enum superclass of the token strings to be retrieved

        Returns
        -------
        tuple[str, ...]
            the tuple of strings representing the tokens of the given
            type `cls_type`
        """
        temp: list[str] = []
        for enum_cls in StandardTokens.get_enum_classes_by_type(cls_type):
            for enum in enum_cls:
                temp.append(enum.value)

        return tuple(temp)


class SyntaxTokens(StandardTokens): ...
class NativeTokens(StandardTokens): ...

class Characters(NativeTokens):
    LOWERCASE_LETTERS = string.ascii_lowercase
    UPPERCASE_LETTERS = string.ascii_uppercase
    LETTERS = string.ascii_letters
    DIGITS = string.digits

class Wildcards(NativeTokens): ...


class PhonemeGroupIdentifiers(Wildcards):
    CONSONANTS = "C"
    VOWELS = "V"


class Operators(SyntaxTokens):
    ASSIGNMENT_OPERATOR = ASSIGNER = "="
    CONCATENATOR = "+"
    CONDITIONAL_IF = "?"
    CONDITIONAL_THEN = "=>"
    MODIFIER = "^"
    MUTATOR = "->"
    SELECTOR = "|"
    SUBTRACTOR = "-"


class Comparator(SyntaxTokens):
    IS_EQUALS = "=="
    IS_NOT_EQUALS = "!="

class Identifiers(SyntaxTokens): ...


class GroupingIdentifiers(Identifiers):
    PROBABILITY_GROUP_OPEN = "("
    PROBABILITY_GROUP_CLOSE = ")"


class TypeIdentifiers(Identifiers):
    PHONEME_OPEN = "/"
    PHONEME_CLOSE = "/"
    STRUCTURE_OPEN = "{"
    STRUCTURE_CLOSE = "}"


TOKEN_CLASSES: tuple[type[StandardTokens], ...] = StandardTokens.get_all_subclasses()
"""The tuple of all `StandardToken` enum classes"""

VALID_CHARS: tuple[str, ...] = StandardTokens.get_valid_chars()
"""The tuple of all valid characters acceptable in a string formula."""

# It's important to register all tokens to STANDARD_TOKENS
# Without this, tokens will not be able to be recognized by CLCK
StandardTokens.register_enums_from_classes(TOKEN_CLASSES)


class SyntaxDefinitions(Enum): ...
class Operations(SyntaxDefinitions): ...
class Declarations(SyntaxDefinitions): ...


@dataclass
class OperationDefinition:
    syntax: tuple[SyntaxTokens | SyntaxObjectTypes, ...]
    is_chainable: bool


class MainOperations(Operations):
    ASSIGNMENT = OperationDefinition(
        (SyntaxObjectTypes.STRUCTURE, Operators.ASSIGNER, SyntaxObjectTypes.STRUCTURE),
        False
    )

    CONCATENATION = OperationDefinition(
        (SyntaxObjectTypes.STRUCTURE, Operators.ASSIGNER, SyntaxObjectTypes.STRUCTURE),
        True
    )

    MUTATION = OperationDefinition(
        (SyntaxObjectTypes.STRUCTURE, Operators.MUTATOR, SyntaxObjectTypes.STRUCTURE),
        False
    )

    SELECTION = OperationDefinition(
        (SyntaxObjectTypes.STRUCTURE, Operators.SELECTOR, SyntaxObjectTypes.STRUCTURE),
        True
    )

    SUBTRACTION = OperationDefinition(
        (SyntaxObjectTypes.STRUCTURE, Operators.SUBTRACTOR, SyntaxObjectTypes.STRUCTURE),
        True
    )


class Conditionals(Operations): ...
class Comparisons(Operations): ...