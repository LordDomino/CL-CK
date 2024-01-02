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
        self._next_token: tuple[Token | None, ...] = ()
        
        # initially start with None for sequence position -1
        self._current_token: Token | None = None

    def parse(self) -> Formula:
        self._advance(1)
        return Formula(self._parse_expr())

    def _parse_expr(self) -> Expression:
        phoneme = self._parse_phoneme()
        self._advance(1)

        if self._next_token[0] == None:
            return Expression(phoneme)
        else:
            if self._next_token[0].type == Operators.CONCATENATOR:
                self._advance(1)
                term = self._parse_term()
                return Expression(Concatenation(phoneme, term))
            elif self._next_token[0].type == Operators.SUBTRACTOR:
                self._advance(1)
                term = self._parse_term()
                return Expression(Subtraction(phoneme, term))
            else:
                raise Exception("Parse error")
    
    def _parse_term(self) -> Term:
        term = Term(self._parse_expr())
        return term
    
    def _parse_phoneme(self) -> Phoneme:
        if self._next_token[0] != None and self._next_token[0].type in (
            Literals.STRING_LITERAL, Literals.IPA_CHARS):
            return DummyPhoneme(self._next_token[0].value)
        else:
            raise Exception(f"{self._next_token} is not a phoneme")

    def _get_next_tokens(self, ahead: int = 1) -> tuple[Token | None, ...]:
        # Set self._next_token to the next token
        ret: list[Token | None] = []
        current_ahead: int = 0
        try:
            while current_ahead < ahead:
                ret.append(self._tokens[self._sequence_pos + current_ahead])
                current_ahead += 1
            return tuple(ret)
        except:
            while current_ahead < ahead:
                ret.append(None)
                current_ahead += 1
            return tuple(ret)
        
    def _advance(self, ahead: int = 1) -> None:
        self._sequence_pos += 1

        try:
            self._current_token = self._tokens[self._sequence_pos]
        except:
            self._current_token = None

        self._next_token = self._get_next_tokens(ahead)
