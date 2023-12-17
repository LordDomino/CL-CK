from typing import Any, TypeAlias
from clck.lexer.definitions import VALID_CHARS
from clck.utils import strip_whitespace


ResultName: TypeAlias = str


class Tokenizer:
    """The class for `Tokenizer`.
    
    A `Tokenizer` allows interpretation of a given string formula before
    it can be passed on to a `Parser` object. It is an essential part of
    a lexing system and it usually handles the first phase of linguistic
    generation. An instance of this class also allows storage of
    relevant data about the analyzed string formula. `Tokenizer`s have
    an `analyze()` method that calls other tokenization methods of this
    class such as ... . 
    
    Below demonstrates simple code to retrieve tokenization data from a
    given string formula.::

        my_tokenizer = Tokenizer("abc")
        my_tokenizer.analyze()

    After a successful method call of `analyze()`, all relevant
    information are stored to the `result_data` dictionary of the
    `Tokenizer` instance, accessible publicly especially for other
    lexing classes such as the `Parser` class.
    """

    def __init__(self, formula: str) -> None:
        """Creates a new `Tokenizer` instance.

        Parameters
        ----------
        formula : str
            the string formula to feed this tokenizer with
        """

        self._formula: str = formula
        self._result_data: dict[ResultName, Any] = {}

    @property
    def result_data(self) -> dict[ResultName, Any]:
        """The dictionary containing the result data based on the most
        recent `analyze()` method call"""

        return self._result_data

    def analyze(self) -> None:
        """Analyzes this instance's formula string and stores each
        analytical data to the dictionary `result_data`.
        """

        self._result_data["string_length"] = self.get_string_length()

    def are_formula_characters_valid(self) -> bool:
        """Checks for each character in the given string `formula`. This
        returns `False` if any of the checked characters is not present
        in `VALID_CHARS`, otherwise returns `True`.

        Returns
        -------
        bool
            `True` if all formula characters are valid, otherwise
            `False`
        """

        for char in self._formula:
            if char not in VALID_CHARS:
                return False
        return True
    
    def get_string_length(self) -> int:
        """Returns the length of the formula string.

        Returns
        -------
        int
            the length of the formula string
        """

        return len(strip_whitespace(self._formula))