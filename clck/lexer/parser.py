from logging import debug
from clck.lexer.definitions import GroupingIdentifiers
from clck.lexer.tokenizer import Token


class Parser:
    def __init__(self, tokens: list[Token] | tuple[Token, ...]) -> None:
        self._tokens = tuple(tokens)
    
    @property
    def tokens(self) -> tuple[Token, ...]:
        return self._tokens
    
    def parse(self) -> ...:
        # Look for topmost probability group

        total_open_parens = 0
        total_close_parens = 0
        paren_cycle = 0
        start_index: int = -1
        retrieved_tokens: list[Token] = []

        for i, token in enumerate(self._tokens):
            match token.type:
                case GroupingIdentifiers.PROBABILITY_GROUP_OPEN:
                    total_open_parens += 1
                    paren_cycle += 1

                    if paren_cycle == 1:
                        start_index = i

                case GroupingIdentifiers.PROBABILITY_GROUP_CLOSE:
                    total_close_parens += 1
                    paren_cycle -= 1

                    if paren_cycle == 0:
                        retrieved_tokens.extend(self._tokens[start_index + 1:i])

                case _:
                    pass

            if retrieved_tokens:
                print(tuple(retrieved_tokens))
                retrieved_tokens = []