from clck.common.component import Component
from clck.common.structure import EmptyStructure, Structurable, Structure
from clck.formulang.parsing.fl_parser import Parser
from clck.formulang.parsing.fl_tokenizer import Tokenizer
from clck.formulang.parsing.parse_tree import TreeNode
from clck.phonology.phonemes import Phoneme
from clck.phonology.syllabics import Nucleus, Syllable


class Formulang:

    @staticmethod
    def generate_ast(formula: str) -> TreeNode:
        tokenizer = Tokenizer(formula)
        tokenizer.analyze()
        parser = Parser(tokenizer.get_tokens())
        ast = parser.parse()
        print(ast)
        return ast

    @staticmethod
    def generate(formula: str) -> Phoneme | Structure[Component]:
        """Generate a result from the given formula string.

        Parameters
        ----------
        formula : str
            the formula to evaluate and get the result from

        Returns
        -------
        Phoneme | Structure | None
            the generated result after evaluating the formula string
        """
        ast = Formulang.generate_ast(formula)
        result = ast.eval()
        if result:
            return result
        else:
            return EmptyStructure()
    
    @staticmethod
    def generate_multiple(formula: str, count: int) -> tuple[Phoneme | Structure[Component] | None, ...]:
        """Generate a tuple of results from the given formula string.

        Parameters
        ----------
        formula : str
            the formula to evaluate and get the results from
        count : int
            the number of iterations in evaluating the formula

        Returns
        -------
        tuple[Phoneme | Structure | None, ...]
            the tuple of results after evaluating the formula string
        """
        ret: list[Phoneme | Structure | None] = []
        for _ in range(count):
            ret.append(Formulang.generate(formula))
        return tuple(ret)
    
    @staticmethod
    def generate_syllable(left_margin: str | None, nucleus: str,
        right_margin: str | None) -> Syllable:

        if left_margin:
            lm_n = Formulang.generate(left_margin)
        else:
            lm_n = Formulang.generate("")

        n = Nucleus(Formulang.generate(nucleus))

        if right_margin:
            rm_n = Formulang.generate(right_margin)
        else:
            rm_n = Formulang.generate("")

        return Syllable((lm_n, n, rm_n))