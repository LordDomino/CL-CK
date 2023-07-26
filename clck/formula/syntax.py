from enum import Enum
import random
import re
import string


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


_SYNTAX = (TypeIdentifiers, StatementIdentifiers, Operators)


def _get_valid_chars(*valid_chars: str) -> str:
    chars = ""

    for v in valid_chars:
        chars += v

    for c_type in _SYNTAX:
        for var in c_type:
            chars += var.value
    
    return "".join(list(set(list(chars))))


def _get_valid_tokens(*enum_types: type[Enum]) -> tuple[str]:
    """Returns a tuple of all valid tokens possible in a syntax."""
    tokens: list[str] = []

    for enum_type in enum_types:  # register tokens from enum classes
        for attr in enum_type:
            tokens.append(attr.value)
    for char in f"{VALID_LETTERS}{VALID_DIGITS}":  # register single-character tokens
        tokens.append(char)

    return tuple(tokens)


VALID_LETTERS: str = string.ascii_letters
VALID_DIGITS: str = string.digits
VALID_CHARS = _get_valid_chars(VALID_LETTERS, VALID_DIGITS)
VALID_TOKENS = _get_valid_tokens(TypeIdentifiers, StatementIdentifiers, Operators)


def _check_if_formula_valid(formula: str) -> bool:
    for char in formula:
        if char not in VALID_CHARS:
            return False
    return True


def _strip_formula(formula: str) -> str:
    return "".join(formula.split()) # strip formula off of whitespaces


def _tokenize(formula: str) -> tuple[str]:
    """Returns a tuple of tokens from the formula."""
    delimiter = ""
    tokens = re.split("", formula)