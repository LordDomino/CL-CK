import re
from clck.config import print_debug
from clck.formula.syntax_definition import DELIMITER, VALID_CHARS, VALID_TOKENS
from clck.utils import strip_whitespace


def get_max_token_len() -> int:
    """Returns the maximum length of a possible token, based on the defined
    tokens.
    """
    max_len: int = -1
    for e in VALID_TOKENS:
        if len(e) > max_len:
            max_len = len(e)

    return max_len


def get_parenthical_pair_count(formula: str | tuple[str, ...]) -> int:
    """Returns the number of parenthical pairs in the given formula."""
    if isinstance(formula, str):
        ...
    else:
        ...


def get_tokens(formula: str) -> tuple[str, ...]:
    if is_formula_valid(formula):
        return recombine_tokens(tokenize_formula(formula))
    else:
        raise Exception(f"Invalid formula: {formula}")


def is_formula_valid(formula: str) -> bool:
    for char in formula:
        if char not in VALID_CHARS:
            return False

    return True


def recombine_tokens(tokens: tuple[str, ...] | list[str]) -> tuple[str, ...]:
    """Returns a tuple of 'true' tokens from the formula."""
    l: list[str] = []

    max_token_len: int = get_max_token_len()

    step: int = max_token_len
    skip: bool = False

    for start_i, t in enumerate(tokens):
        if step > 1 and skip:
            step -= 1
            continue
        else:
            step: int = max_token_len
            stop_i: int = start_i + max_token_len
            extend_str: str = "".join(tokens[start_i:stop_i])
            while step >= 1:
                if extend_str in VALID_TOKENS:
                    print_debug(f"Base element: {t}, {extend_str}")
                    l.append(extend_str)
                    skip = True
                    break
                elif step > 1:
                    step -= 1
                    skip = False
                    stop_i = start_i + step
                    extend_str = "".join(tokens[start_i:stop_i])
                else:
                    if len(extend_str) > 1:
                        print_debug(f"Base element: {t}, {extend_str}")
                        l.append(extend_str)
                        step = max_token_len
                        skip = False
                        break
                    else:
                        raise Exception(f"Unknown token '{extend_str}'")

    return tuple(l)


def tokenize_formula(formula: str) -> tuple[str, ...]:
    """Returns a tuple of 'loose' tokens from the formula."""
    tokens = filter(None, re.split(DELIMITER, strip_whitespace(formula)))

    return tuple(tokens)