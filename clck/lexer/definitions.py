from dataclasses import dataclass
from enum import Enum
from enum import auto
import string
from typing import TypeVar


T = TypeVar("T")


STANDARD_TOKENS: list["StandardTokens"] = []
"""The list of all recognized `StandardToken` enum members"""


class SyntaxObjectTypes(Enum):
    STRUCTURE = auto()
    PHONEME = auto()
    LANGUAGE_INPUT = auto()

class StandardTokens(Enum):

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}.{self.name}"

    @classmethod
    def get_all_subclasses(cls) -> tuple[type["StandardTokens"], ...]:
        """Returns a tuple of all `StandardTokens` enum subclasses.

        Returns
        -------
        tuple[type[StandardTokens]]
            the tuple of all `StandardTokens`
        """
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
        chars.extend(list(string.ascii_letters))
        chars.extend(list(string.digits))
    
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
    def get_token_definitions_by_type(cls_type: type["StandardTokens"]) -> tuple["StandardTokens", ...]:
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
        temp: list[StandardTokens] = []
        for enum_cls in StandardTokens.get_enum_classes_by_type(cls_type):
            for enum in enum_cls:
                temp.append(enum)

        return tuple(temp)

    @staticmethod
    def get_raw_token_definitions_by_type() -> tuple[str, ...]:
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
        for token_definition in STANDARD_TOKENS:
            temp.append(token_definition.value)

        return tuple(temp)


class SyntaxTokens(StandardTokens): ...
class NativeTokens(StandardTokens): ...


class Characters(NativeTokens):
    LITERAL_STRINGS = r"[a-zA-Z]+"
    NUMBER = r"[0-9]+"


class Wildcards(NativeTokens): ...


class PhonemeGroupIdentifiers(Wildcards):
    CONSONANTS = "C"
    VOWELS = "V"


class Operators(SyntaxTokens):
    ASSIGNMENT_OPERATOR = ASSIGNER = r"\="
    CONCATENATOR = r"\+"
    CONDITIONAL_IF = r"\?"
    CONDITIONAL_THEN = r"\=>"
    MODIFIER = r"\^"
    MUTATOR = r"\->"
    SELECTOR = r"\|"
    SUBTRACTOR = r"\-"


class Comparator(SyntaxTokens):
    IS_EQUALS = r"\=="
    IS_NOT_EQUALS = r"\!="


class Delimiters(SyntaxTokens):
    SEPARATOR = r"\."


class Identifiers(SyntaxTokens): ...


class GroupingIdentifiers(Identifiers):
    PROBABILITY_GROUP_OPEN = r"\("
    PROBABILITY_GROUP_CLOSE = r"\)"


class TypeIdentifiers(Identifiers):
    # PHONEME_OPEN = r"\/"
    # PHONEME_CLOSE = r"\/"
    STRUCTURE_OPEN = r"\{"
    STRUCTURE_CLOSE = r"\}"


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

    PROBABILITY = OperationDefinition(
        (GroupingIdentifiers.PROBABILITY_GROUP_OPEN, SyntaxObjectTypes.STRUCTURE, GroupingIdentifiers.PROBABILITY_GROUP_CLOSE),
        False
    )


class Conditionals(Operations): ...
class Comparisons(Operations): ...