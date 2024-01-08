from clck.formulang.parsing.fl_parser import Parser
from clck.formulang.parsing.fl_tokenizer import Tokenizer
from clck.phonology.phonemes import Phoneme
from clck.phonology.syllabics import Structure


def generate(formula: str) -> Phoneme | Structure | None:
    """Generate a result from the given formula string.

    Parameters
    ----------
    formula : str
        the formula to evaluate and get the result from

    Returns
    -------
    Phoneme | Structure | None
        the generated result after evaluating the formula string
    """
    tokenizer = Tokenizer(formula)
    tokenizer.analyze()
    parser = Parser(tokenizer.get_tokens())
    ast = parser.parse()
    return ast.eval()

def generate_multiple(formula: str, count: int) -> tuple[Phoneme | Structure | None, ...]:
    """Generate a tuple of results from the given formula string.

    Parameters
    ----------
    formula : str
        the formula to evaluate and get the results from
    count : int
        the number of iterations in evaluating the formula

    Returns
    -------
    tuple[Phoneme | Structure | None, ...]
        the tuple of results after evaluating the formula string
    """
    ret: list[Phoneme | Structure | None] = []
    for _ in range(count):
        ret.append(generate(formula))
    return tuple(ret)