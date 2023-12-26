from clck.lexer.definitions import CommonGroupings
from clck.lexer.tokenizer import Token


class Parser:
    def __init__(self, tokens: list[Token] | tuple[Token, ...]) -> None:
        self._tokens = tuple(tokens)
    
    @property
    def tokens(self) -> tuple[Token, ...]:
        return self._tokens
    
    def parse(self) -> ...:
        return self._deep_parse(self._tokens)

    def _deep_parse(self, tokens: list[Token] | tuple[Token, ...]) -> ...:
        # Look for topmost probability group

        total_open_parens = 0
        total_close_parens = 0
        paren_cycle = 0
        start_index: int = -1
        retrieved_tokens: list[Token] = []

        for i, token in enumerate(tokens):
            match token.type:
                case CommonGroupings.PROBABILITY_GROUP_OPEN:
                    total_open_parens += 1
                    paren_cycle += 1

                    if paren_cycle == 1:
                        start_index = i

                case CommonGroupings.PROBABILITY_GROUP_CLOSE:
                    total_close_parens += 1
                    paren_cycle -= 1

                    if paren_cycle == 0:
                        retrieved_tokens.extend(tokens[start_index + 1:i])

                case _:
                    pass

            if retrieved_tokens:
                # Actually parse more
                print(tuple(retrieved_tokens))
                self._deep_parse(retrieved_tokens)
                retrieved_tokens = []