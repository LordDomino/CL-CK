from clck.formulang.definitions.tokens import CommonGroupings, Literals, StandardTokens, TypeGroupings
from clck.formulang.definitions.tokens import Operators
from clck.formulang.lexer.tokenizer import Token
from clck.formulang.parsing.parse_tree import BinaryOperation, Concatenation, Factor, FormulangPhoneme, Modifier, Selection, StructureNode, SumNode
from clck.formulang.parsing.parse_tree import Expression
from clck.formulang.parsing.parse_tree import Formula
from clck.formulang.parsing.parse_tree import Subtraction
from clck.formulang.parsing.parse_tree import Term


class Parser:
    def __init__(self, tokens: list[Token] | tuple[Token, ...]) -> None:
        self._tokens = tuple(tokens)
        self._sequence_pos: int = -1
        self._next_tokens: tuple[Token | None, ...] = self._get_next_tokens(1)
        
        # initially start with None for sequence position -1
        self._current_token: Token | None = None
        self._current_brace_level: int = -1

    def parse(self) -> Formula:
        return Formula((self._parse_expr(),))

    def _parse_expr(self) -> Expression:
        return Expression((self._parse_sum(),), self._current_brace_level)

    def _parse_sum(self) -> SumNode:
        selection: Selection = self._parse_selection()

        # M --> R
        if self._next_tokens == () or self._next_tokens[0] == None:
            if self._current_token != None:
                return SumNode((selection,), self._current_token.brace_level)
            else:
                raise Exception("Current token is None")

        # Otherwise, either M --> R + M or M --> R - M
        else:
            # M --> R + M
            if self._next_tokens[0].type == Operators.CONCATENATOR:
                self._advance(1)
                sum: SumNode = self._parse_sum()
                return SumNode(
                    (Concatenation(selection, sum, self._current_brace_level),),
                    self._current_brace_level
                )

            # M --> R - M
            elif self._next_tokens[0].type == Operators.SUBTRACTOR:
                self._advance(1)
                sum: SumNode = self._parse_sum()
                return SumNode(
                    (Subtraction(selection, sum, self._current_brace_level),),
                    self._current_brace_level
                )
            else:
                self._advance(1)
                if self._current_token != None:
                    return SumNode((selection,), self._current_token.brace_level)
                else:
                    raise Exception

    def _parse_selection(self) -> Selection:
        factor: Factor = self._parse_factor()
        
        # R --> F
        if self._next_tokens == () or self._next_tokens[0] == None:
            if self._current_token != None:
                return Selection(factor, None, self._current_token.brace_level)
            else:
                raise Exception("Current token is None")
        
        # Otherwise, R --> F | R
        else:
            # R --> F + R
            if self._next_tokens[0].type == Operators.SELECTOR:
                self._advance(1)
                selection: Selection = self._parse_selection()
                return Selection(factor, selection, self._current_brace_level)
            else:
                self._advance(1)
                if self._current_token != None:
                    return Selection(factor, None, self._current_token.brace_level)
                else:
                    raise Exception("Current token is none")

    def _parse_factor(self) -> Factor:
        term = self._parse_term()

        # F --> T
        if self._next_tokens == () or self._next_tokens[0] == None:
            if self._current_token != None:
                return Factor((term,), self._current_token.brace_level)
            else:
                raise Exception("Current token is None")
            
        # Otherwise, F --> T ^ N
        else:
            # R --> F + R
            if self._next_tokens[0].type == Operators.MODIFIER:
                self._advance(1)
                modifier: Modifier = self._parse_modifier()
                return Factor((term, modifier), self._current_brace_level)
            else:
                self._advance(1)
                if self._current_token != None:
                    return Factor((term,), self._current_token.brace_level)
                else:
                    raise Exception

    def _parse_modifier(self) -> Modifier:
        pass

    def _parse_expr_old(self) -> Expression:
        term = self._parse_term()
        self._advance(1)

        if self._next_tokens == () or self._next_tokens[0] == None:
            if self._current_token != None:
                return Expression((term,), self._current_token.brace_level)
            else:
                raise Exception("Parse error")
        else:
            if self._current_token != None:
                returns: dict[StandardTokens, type[BinaryOperation]] = {
                    Operators.CONCATENATOR: Concatenation,
                    Operators.SUBTRACTOR: Subtraction,
                    Operators.SELECTOR: Selection,
                }

                for token_type in returns.keys():
                    if self._next_tokens[0].type == token_type:
                        self._advance(1)
                        expr = self._parse_sum()
                        return Expression(
                            (returns[token_type](term, expr, self._current_brace_level),),
                            self._current_brace_level
                        )

                return Expression((term,), self._current_token.brace_level)
            else:
                raise Exception("Parse error")

    def _parse_term(self) -> Term:
        if self._next_tokens[0] == None:
            raise Exception("Term parse error")
        else:
            if self._next_tokens[0].type == CommonGroupings.PROBABILITY_GROUP_OPEN:
                self._advance(1)
                term = Term((self._parse_sum(),), self._current_brace_level)
                return term
            elif self._next_tokens[0].type == TypeGroupings.STRUCTURE_OPEN:
                self._advance(1)
                term = Term((self._parse_structure(),), self._current_brace_level)
                return term
            else:
                return Term((self._parse_phoneme(),), self._current_brace_level)

    def _parse_phoneme(self) -> FormulangPhoneme:
        if self._next_tokens[0] != None and self._next_tokens[0].type in (
            Literals.STRING_LITERAL, Literals.IPA_CHARS):
            phoneme = FormulangPhoneme(self._next_tokens[0].value, self._current_brace_level)
            self._advance(1)
            return phoneme
        else:
            raise Exception(f"{self._next_tokens} is not a phoneme")

    def _parse_structure(self) -> StructureNode:
        return StructureNode(self._parse_sum(), self._current_brace_level)

    def _get_next_tokens(self, ahead: int) -> tuple[Token | None, ...]:
        # Set self._next_token to the next token
        ret: list[Token | None] = []
        current_ahead: int = 0
        try:
            while current_ahead < ahead:
                current_ahead += 1
                ret.append(self._tokens[self._sequence_pos + current_ahead])
            return tuple(ret)
        except:
            while current_ahead < ahead:
                ret.append(None)
                current_ahead += 1
            return tuple(ret)
        
    def _advance(self, steps: int) -> None:
        self._sequence_pos += 1

        try:
            self._current_token = self._tokens[self._sequence_pos]
            self._current_brace_level = self._current_token.brace_level
        except:
            self._current_token = None

        self._next_tokens = self._get_next_tokens(steps)