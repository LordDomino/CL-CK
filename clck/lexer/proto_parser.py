from clck.lexer.definitions import Characters
from clck.lexer.tokenizer import Token


class ProtoParser:
    def __init__(self, formula_str: str) -> None:
        self._formula_str = formula_str

    def parse(self, string: str) -> ...:
        pass

    def _formula(self):
        return self._numeric_literal()
    
    def _numeric_literal(self):
        return Token(Characters.NUMBER, int(self._formula_str))