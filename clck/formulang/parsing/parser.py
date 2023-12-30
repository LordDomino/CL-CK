from clck.formulang.definitions.tokens import Literals
from clck.formulang.definitions.tokens import Operators
from clck.formulang.lexer.tokenizer import Token
from clck.formulang.parsing.parse_tree import Concatenation
from clck.formulang.parsing.parse_tree import Expression
from clck.formulang.parsing.parse_tree import Formula
from clck.formulang.parsing.parse_tree import Subtraction
from clck.formulang.parsing.parse_tree import Term
from clck.phonology import DummyPhoneme
from clck.phonology import Phoneme


class Parser:
    def __init__(self, tokens: list[Token] | tuple[Token, ...]) -> None:
        self._tokens = tuple(tokens)
        self._sequence_pos: int = -1
        self._next_token: Token | None = self._get_next_token()
        
        # initially start with None for sequence position -1
        self._current_token: Token | None = None

    def parse(self) -> Formula:
        return Formula(self._parse_expr())

    def _parse_expr(self) -> Expression:
        phoneme = self._parse_phoneme()
        self._advance()

        if self._next_token != None:
            if self._next_token.type == Operators.CONCATENATOR:
                self._advance()
                term = self._parse_term()
                return Expression(Concatenation(phoneme, term))
            elif self._next_token.type == Operators.SUBTRACTOR:
                self._advance()
                term = self._parse_term()
                return Expression(Subtraction(phoneme, term))
            else:
                raise Exception("Parse error")
        else:
            return Expression(phoneme)
    
    def _parse_term(self) -> Term:
        return Term(self._parse_expr())
    
    def _parse_phoneme(self) -> Phoneme:
        if self._next_token != None and self._next_token.type in (
            Literals.STRING_LITERAL, Literals.IPA_CHARS):
            return DummyPhoneme(self._next_token.value)
        else:
            raise Exception(f"{self._next_token} is not a phoneme")

    def _get_next_token(self) -> Token | None:
        # Set self._next_token to the next token
        try:
            return self._tokens[self._sequence_pos + 1]
        except:
            return None
        
    def _advance(self) -> None:
        try:
            self._sequence_pos += 1
            self._current_token = self._tokens[self._sequence_pos]
            self._next_token = self._get_next_token()
        except:
            self._next_token = None