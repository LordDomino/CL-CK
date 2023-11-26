import string
from enum import Enum



class TypeIdentifiers(Enum):
    PHONEME = "/"
    BANK_OPEN = "["
    BANK_CLOSE = "]"
    GROUP_OPEN = "("
    GROUP_CLOSE = ")"
    STRUCTURE_OPEN = "{"
    STRUCTURE_CLOSE = "}"



class StatementIdentifiers(Enum):
    IF = "?"
    THEN = "->"
    SUPPORT_STATEMENT = "\""



class Operators(Enum):
    OR = ","
    AND = "+"
    MINUS = "-"



_SYNTAX_TYPES = (TypeIdentifiers, StatementIdentifiers, Operators)
DELIMITER = r"([\?\(\)\/\-\+\{\}\>])"
VALID_LETTERS = string.ascii_letters
VALID_DIGITS = string.digits


def get_valid_chars(*valid_chars: str) -> str:
    chars: str = ""

    for v in valid_chars:
        chars += v

    for c_type in _SYNTAX_TYPES:
        for var in c_type:
            chars += var.value
    
    return "".join(list(set(list(chars))))


def get_valid_tokens(*enum_types: type[Enum]) -> tuple[str, ...]:
    """
    Returns a tuple of all valid tokens possible in a syntax.
    """
    tokens: list[str] = []

    for enum_type in enum_types:  # register tokens from enum classes
        for attr in enum_type:
            tokens.append(attr.value)
    for char in f"{VALID_LETTERS}{VALID_DIGITS}":  # register single-character tokens
        tokens.append(char)

    return tuple(tokens)


VALID_CHARS = get_valid_chars(VALID_LETTERS, VALID_DIGITS)
VALID_TOKENS = get_valid_tokens(TypeIdentifiers, StatementIdentifiers, Operators)