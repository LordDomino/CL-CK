import string
from dataclasses import dataclass
from enum import auto
from enum import Enum
from typing import TypeVar

from clck.phonology.phonemes import Phoneme


T = TypeVar("T")


STANDARD_TOKENS: list["StandardTokenType"] = []
"""The list of all recognized `StandardToken` enum members"""


class SyntaxObjectTypes(Enum):
    STRUCTURE = auto()
    PHONEME = auto()
    LITERAL = auto()

class StandardTokenType(Enum):

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}.{self.name}"

    @classmethod
    def get_all_subclasses(cls) -> tuple[type["StandardTokenType"], ...]:
        """Returns a tuple of all `StandardTokens` enum subclasses.

        Returns
        -------
        tuple[type[StandardTokens]]
            the tuple of all `StandardTokens`
        """
        temp: list[type[StandardTokenType]] = []

        temp.extend(cls.__subclasses__())
        for c in cls.__subclasses__():
            temp.extend(c.get_all_subclasses())

        return tuple(temp)

    @staticmethod
    def register_enums_from_classes(
        enum_classes: tuple[type["StandardTokenType"], ...]) -> None:
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
    
        for enum_class in StandardTokenType.get_all_subclasses():
            for enum in enum_class:
                if isinstance(enum.value, str):
                    chars.extend(list(enum.value))

        for phoneme in Phoneme.DEFAULT_IPA_PHONEMES:
            chars.append(phoneme.symbol)

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
        for c in StandardTokenType.get_all_subclasses():
            if issubclass(c, cls_type):
                temp.append(c)

        return tuple(temp)
    
    @staticmethod
    def get_identifier_classes() -> tuple[type["Groupings"], ...]:
        return StandardTokenType.get_enum_classes_by_type(Groupings)

    @staticmethod
    def get_wildcard_classes() -> tuple[type["Wildcards"], ...]:
        return StandardTokenType.get_enum_classes_by_type(Wildcards)
    
    @staticmethod
    def get_token_definitions_by_type(cls_type: type["StandardTokenType"]) -> tuple["StandardTokenType", ...]:
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
        temp: list[StandardTokenType] = []
        for enum_cls in StandardTokenType.get_enum_classes_by_type(cls_type):
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


class SyntaxTokens(StandardTokenType):
    """Syntax tokens are tokens that are essential to the formulation
    of the formula meta-syntax.
    """


class NativeTokens(StandardTokenType):
    """Native tokens are non-special tokens containing literals etc.
    """


class Literals(NativeTokens):
    """`Literals` contain the string literal and numeric literal
    definitions.
    """
    STRING_LITERAL = r"[a-zA-Z]+"
    NUMERIC_LITERAL = r"[0-9]+"
    EPSILON = ""
    ELLIPSIS = r"\.\.\."
    # IPA_CHARS = rf"[{''.join(Phoneme.DEFAULT_IPA_SYMBOLS)}]+" 


class Wildcards(NativeTokens):
    """`Wildcards` define default wildcard literals that are reserved
    for special wildcard purposes, such as declaring a consonant or a
    vowel in a formula string.
    """


class PhonemeGroupIdentifiers(Wildcards):
    """`PhonemeGroupIdentifiers` define the reserved string literals
    used for declaring phoneme groups in a formula string.
    """
    CONSONANTS = "C"
    VOWELS = "V"


class Operators(SyntaxTokens):
    """`Operators` defines the regex delimiter definitions for
    tokenizing and parsing a formula string.

    Note: Unary, binary, ternary, and possible n-ary operators are
    combined here.
    """
    ASSIGNMENT_OPERATOR = ASSIGNER = r"\="
    CONCATENATOR = r"\+"
    CONDITIONAL_IF = r"\?"
    CONDITIONAL_THEN = r"\=>"
    MODIFIER = r"\^"
    MUTATOR = r"\->"
    SELECTOR = r"\|"
    SUBTRACTOR = r"\-"
    IS_EQUALS = r"\=="
    IS_NOT_EQUALS = r"\!="


class Delimiters(SyntaxTokens):
    """`Delimiters` defines different delimiters in the formula meta-
    syntax.
    """
    SEPARATOR = r"\."


class Groupings(SyntaxTokens): ...


class CommonGroupings(Groupings):
    PROBABILITY_GROUP_OPEN = r"\("
    PROBABILITY_GROUP_CLOSE = r"\)"


class TypeGroupings(Groupings):
    # PHONEME_OPEN = r"\/"
    # PHONEME_CLOSE = r"\/"
    STRUCTURE_OPEN = r"\{"
    STRUCTURE_CLOSE = r"\}"


TOKEN_CLASSES: tuple[type[StandardTokenType], ...] = StandardTokenType.get_all_subclasses()
"""The tuple of all `StandardToken` enum classes"""

VALID_CHARS: tuple[str, ...] = StandardTokenType.get_valid_chars()
"""The tuple of all valid characters acceptable in a string formula."""

# It's important to register all tokens to STANDARD_TOKENS.
# Without this, tokens will not be able to be recognized by CLCK.
StandardTokenType.register_enums_from_classes(TOKEN_CLASSES)


class SyntaxDefinitions(Enum): ...
class Operations(SyntaxDefinitions): ...
class Declarations(SyntaxDefinitions): ...


@dataclass
class OperationDefinition:
    syntax: tuple[SyntaxTokens | SyntaxObjectTypes, ...]
    is_chainable: bool


class BinaryOperations(Operations):
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
        (CommonGroupings.PROBABILITY_GROUP_OPEN, SyntaxObjectTypes.STRUCTURE, CommonGroupings.PROBABILITY_GROUP_CLOSE),
        False
    )


class Conditionals(Operations): pass
class Comparisons(Operations): pass