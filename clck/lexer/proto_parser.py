from typing import Any

from clck.lexer.definitions import Literals


class ProtoParser:
    def __init__(self, formula_str: str) -> None:
        self._formula_str = formula_str

    def parse(self) -> dict[Any, Any]:
        return self._formula()

    def _formula(self):
        return {
            "type" : "Formula",
            "body" : self._numeric_literal()
        }
    
    def _numeric_literal(self):
        return {
            "type" : Literals.NUMERIC_LITERAL.name,
            "value" : int(self._formula_str)
        }