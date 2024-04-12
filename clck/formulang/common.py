from typing import TypeVar
from clck.common.component import Component
from clck.common.structure import EmptyStructure, Structure
from clck.formulang.parsing.fl_parser import Parser
from clck.formulang.parsing.fl_tokenizer import Tokenizer
from clck.formulang.parsing.parse_tree import Formula, TreeNode
from clck.phonology.syllabics import Nucleus, SyllabicComponent, Syllable
from tests.test_classes import SyllableComponent

StructureT = TypeVar("StructureT", bound="Structure")

class Formulang:

    @staticmethod
    def generate_ast(formula: str) -> Formula:
        tokenizer = Tokenizer(formula)
        tokenizer.analyze()
        parser = Parser(tokenizer.get_tokens())
        ast = parser.parse()
        return ast

    @staticmethod
    def generate(formula: str) -> Component:
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
    def generate_of_type(formula: str, type: type[StructureT]) -> StructureT:
        _g = Formulang.generate(formula)
        return type(_g)
    
    @staticmethod
    def generate_multiple(formula: str, count: int) -> tuple[Component, ...]:
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
        ret: list[Component] = []
        for _ in range(count):
            ret.append(Formulang.generate(formula))
        return tuple(ret)
    
    @staticmethod
    def generate_syllable(left_margin: str | None, nucleus: str,
        right_margin: str | None) -> Syllable:

        if left_margin:
            lm_n = Formulang.generate_of_type(left_margin, SyllabicComponent)
        else:
            lm_n = Formulang.generate_of_type("", SyllabicComponent)

        n = Formulang.generate_of_type(nucleus, Nucleus)

        if right_margin:
            rm_n = Formulang.generate_of_type(right_margin, SyllabicComponent)
        else:
            rm_n = Formulang.generate_of_type("", SyllabicComponent)

        return Syllable((lm_n, n, rm_n))
    

class FormulangTempContainer:
    def __init__(self, formulang_result: TreeNode) -> None:
        self._result = formulang_result
        