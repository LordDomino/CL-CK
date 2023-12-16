from clck.lexer.definitions import VALID_CHARS


def is_formula_valid(formula: str) -> bool:
    """
    Returns `False` if the given string `formula` contains an illegal
    character not present in `VALID_CHARS`, otherwise returns `True`.
    """
    for char in formula:
        if char not in VALID_CHARS:
            return False
    return True