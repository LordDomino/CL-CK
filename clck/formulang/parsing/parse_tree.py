from clck.component import Component
from clck.formulang.definitions.tokens import Operators
from clck.formulang.lexer.tokenizer import Token
from clck.phonology import Phoneme
from clck.syllabics import CustomStructure, Structure
from clck.utils import clean_collection


class TreeNode:

    _indent_count: int = 0
    _indent_size: int = 2

    def __init__(self, subnodes: tuple["TreeNode | Phoneme | Structure", ...],
        brace_level: int) -> None:
        self._subnodes = subnodes
        self._brace_level = brace_level

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} brace_level={self._brace_level}>"

    def __str__(self) -> str:
        print(self.__repr__())
        _str = "{\n"
        TreeNode._indent_in()

        _str += self._get_indentation() + f"type: {self.__class__.__name__},\n"

        if len(self._subnodes) == 1:
            _str += self._get_indentation() + "value: "
            _str += f"{self._subnodes[0].__str__()}"
        else:
            _str += self._get_indentation() + "value: [\n"

            TreeNode._indent_in()
            for arg in self._subnodes:
                _str += self._get_indentation() + f"{arg.__str__()}" + ",\n"

            TreeNode._indent_out()
            _str += self._get_indentation() + "]"

        TreeNode._indent_out()
        _str += "\n" + self._get_indentation() + "}"

        return _str

    def eval(self) -> Phoneme | Structure:        
        for subnode in self._subnodes:
            if isinstance(subnode, TreeNode):
                return subnode.eval()
            else:
                return subnode

    def _get_indentation(self) -> str:
        return " " * TreeNode._indent_count * TreeNode._indent_size
    
    @classmethod
    def _indent_in(cls) -> None:
        cls._indent_count += 1

    @classmethod
    def _indent_out(cls) -> None:
        cls._indent_count -= 1


class Operator(TreeNode):
    def __init__(self, subnodes: tuple[TreeNode | Phoneme | Structure, ...],
        brace_level: int) -> None:
        super().__init__(subnodes, brace_level)


class BinaryOperator(Operator):
    def __init__(self, left: TreeNode | Phoneme | Structure,
        right: TreeNode | Phoneme | Structure, operator: Token,
        brace_level: int) -> None:
        super().__init__((left, right), brace_level)
        self._left = left
        self._right = right
        self._operator = operator

    # def eval(self) -> Phoneme | Structure:
    #     if isinstance(self._left, TreeNode):
    #         lval = self._left.eval()
    #     else:
    #         lval = self._left

    #     if isinstance(self._right, TreeNode):
    #         rval = self._right.eval()
    #     else:
    #         rval = self._right

    #     return (lval, rval)


class Concatenation(BinaryOperator):

    _level: int = 0

    def __init__(self, left: TreeNode | Phoneme | Structure,
        right: TreeNode | Phoneme | Structure, brace_level: int) -> None:
        super().__init__(left, right, Token(Operators.CONCATENATOR, "+", -1), brace_level)


    def eval(self) -> Structure:
        Concatenation._level += 1
        components: list[Phoneme | Structure] = []

        for subnode in self._subnodes:
            if isinstance(subnode, Phoneme):
                components.append(subnode)
            elif isinstance(subnode, Structure):
                components.append(subnode)
            else:
                components.append(subnode.eval())

        return CustomStructure((Component,), tuple(components))


class Subtraction(BinaryOperator):
    def __init__(self, left: TreeNode | Phoneme | Structure,
        right: TreeNode | Phoneme | Structure, brace_level: int) -> None:
        super().__init__(left, right, Token(Operators.SUBTRACTOR, "-", -1), brace_level)

    # def eval(self) -> Phoneme | Structure:
    #     operands = super().eval()
    #     return CustomStructure((Component,), (operands[0], operands[1]))


class Expression(TreeNode):
    def __init__(self, subnodes: tuple[TreeNode | Phoneme | Structure, ...],
        brace_level: int) -> None:
        super().__init__(subnodes, brace_level)


class Term(TreeNode):
    def __init__(self, subnodes: tuple[TreeNode | Phoneme | Structure, ...],
        brace_level: int) -> None:
        super().__init__(clean_collection(subnodes), brace_level)


class Formula(TreeNode):
    def __init__(self, subnodes: tuple[TreeNode | Phoneme | Structure, ...]) -> None:
        super().__init__(subnodes, -1)


class StructureNode(TreeNode):
    def __init__(self, subnodes: tuple[TreeNode | Phoneme | Structure, ...],
        brace_level: int) -> None:
        super().__init__(subnodes, brace_level)