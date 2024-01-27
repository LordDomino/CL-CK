from typing import Callable
from clck.formulang.definitions.tokens import CommonGroupings, Literals, StandardTokenType, TypeGroupings
from clck.formulang.definitions.tokens import Operators
from clck.formulang.parsing.fl_tokenizer import EPSILON_TOKEN, Token
from clck.formulang.parsing.parse_tree import Concatenation, EllipsisNode, Factor, FormulangPhoneme, ProbabilityNode, Selection, StructureNode, Operation, TreeNode
from clck.formulang.parsing.parse_tree import Expression
from clck.formulang.parsing.parse_tree import Formula
from clck.formulang.parsing.parse_tree import Subtraction
from clck.formulang.parsing.parse_tree import Term


class Parser:

    def __init__(self, tokens: list[Token] | tuple[Token, ...]) -> None:
        self._tokens = tuple(tokens)
        self._sequence_pos: int = -1
        self._next_tokens: tuple[Token, ...] = self._get_next_tokens(1)
        
        # initially start with None for sequence position -1
        self._current_token: Token | None = None
        self._current_brace_level: int = -1

    def parse(self) -> Formula:
        ast = self._raw_parse()
        self._reset()

        return ast

    def _raw_parse(self) -> Formula:
        if self._next_tokens[0] == EPSILON_TOKEN:
            return Formula(())
        else:
            expr = self._parse_expr()

            if self._sequence_pos < len(self._tokens) - 2:
                raise Exception(f"Leftover, token unknown {self._next_tokens[0]}")
            else:
                return Formula((expr,))

    def _parse_expr(self) -> Expression:
        expr = Expression((self._parse_selection(),), self._current_brace_level)
        return expr

    def _parse_selection(self) -> Selection | TreeNode:
        operation = self._parse_operation()
        brace_level = self._current_brace_level
        
        matched = self._match_next_token(
            {
                Operators.SELECTOR: lambda: self._parse_selection(),
            }
        )

        if matched:
            # R --> F + R (chained)
            if operation.brace_level == matched[0].brace_level:
                return Selection((operation, *matched[0].subnodes), brace_level)
            # R --> F + R
            else:
                return Selection((operation, matched[0]), brace_level)
        else:
            # R --> F
            return operation

    def _parse_operation(self) -> Operation | TreeNode:
        factor = self._parse_factor()
        brace_level = self._current_brace_level

        matched = self._match_next_token(
            {
                Operators.CONCATENATOR: lambda: self._parse_operation(),
                Operators.SUBTRACTOR: lambda: self._parse_operation()
            }
        )

        if matched:

            # M --> R + M
            if matched[1] == Operators.CONCATENATOR:
                return Concatenation((factor, *matched[0].subnodes), brace_level)

            # M --> R - M
            elif matched[1] == Operators.SUBTRACTOR:
                # no specifications for chained and binary operations yet
                return Subtraction((factor, *matched[0].subnodes), brace_level)
            else:
                raise Exception("Unknown match error")
        else:
            # M --> R
            return factor

    def _parse_factor(self) -> Factor | TreeNode:
        term = self._parse_term()
        brace_level = self._current_brace_level

        matched = self._match_next_token(
            {
                Operators.MODIFIER: lambda: self._parse_modifier()
            }
        )

        if matched:
            return Factor((term, matched[0]), brace_level)
        else:
            return term

    def _parse_modifier(self) -> ...:
        pass

    def _parse_term(self) -> Term | TreeNode:
        brace_level = self._current_brace_level

        if self._next_tokens[0].type == CommonGroupings.PROBABILITY_GROUP_OPEN:
            self._advance(1)
            term = Term((self._parse_probability(),), brace_level)
            self._advance(1)
            return term
        elif self._next_tokens[0].type == TypeGroupings.STRUCTURE_OPEN:
            try:
                self._advance(1)
                term = Term((self._parse_structure(),), brace_level)
                self._advance(1)
                return term
            except Exception as e:
                print(e.args)
                self._advance(1)
                return Term((), brace_level)
        elif self._next_tokens[0].type == Literals.ELLIPSIS:
            dummy_phoneme = EllipsisNode(brace_level)
            self._advance(1)
            return dummy_phoneme
        else:
            return self._parse_phoneme()

    def _parse_phoneme(self) -> FormulangPhoneme:
        if self._next_tokens[0].type in (Literals.STRING_LITERAL,):
            phoneme = FormulangPhoneme(self._next_tokens[0].value, self._next_tokens[0].brace_level)
            self._advance(1)
            return phoneme
        else:
            raise Exception(f"Found {self._next_tokens[0]} but expected a phoneme")

    def _parse_structure(self) -> StructureNode | TreeNode:
        return StructureNode(self._parse_expr(), self._current_brace_level)

    def _parse_probability(self) -> ProbabilityNode | TreeNode:
        return ProbabilityNode((self._parse_expr(),), self._current_brace_level)

    def _get_next_tokens(self, ahead: int) -> tuple[Token, ...]:
        # Set self._next_token to the next token
        ret: list[Token] = []
        current_ahead: int = 0
        try:
            while current_ahead < ahead:
                current_ahead += 1
                ret.append(self._tokens[self._sequence_pos + current_ahead])
            return tuple(ret)
        except:
            while current_ahead < ahead:
                ret.append(EPSILON_TOKEN)
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

    def _assert_next_token(self) -> bool:
        """Returns `True` if a next token is available, otherwise
        returns `False`.

        Returns
        -------
        bool
            whether or not there is a next token available
        """
        return not self._assert_next_token_empty()

    def _assert_next_token_empty(self) -> bool:
        """Returns `False` if no more next tokens is/are available,
        otherwise returns `True`.

        Returns
        -------
        bool
            whether or not no more next tokens is/are available
        """
        if self._next_tokens == () or self._next_tokens[0] == EPSILON_TOKEN:
            return True
        else:
            return False
        
    def _match_next_token(self, match_to: dict[StandardTokenType,
            Callable[..., TreeNode]]
            ) -> tuple[TreeNode, StandardTokenType] | None:
        for key in match_to.keys():
            if self._next_tokens[0].type == key:
                self._advance(1)
                parsed = match_to[key]()
                return (parsed, key)
            
    def _reset(self) -> None:
        self._sequence_pos: int = -1
        self._next_tokens: tuple[Token, ...] = self._get_next_tokens(1)
        self._current_token = None
        self._current_brace_level: int = -1