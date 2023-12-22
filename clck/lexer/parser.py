from clck.lexer.tokenizer import Token
from clck.lexer.tokenizer import Tokenizer


class Parser:
    def __init__(self, tokens: list[Token] | tuple[Token, ...]) -> None:
        self._tokens = tuple(tokens)

    @classmethod
    def from_Tokenizer(cls, tokenizer: Tokenizer) -> "Parser":
        return cls(tokenizer.get_tokens())
    
    @property
    def tokens(self) -> tuple[Token, ...]:
        return self._tokens