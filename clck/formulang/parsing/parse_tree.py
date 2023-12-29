from clck.component import Component
from clck.formulang.definitions.tokens import Operators
from clck.formulang.lexer.tokenizer import Token
from clck.syllabics import CustomStructure
from clck.utils import clean_collection


class TreeNode:

    _indent_count: int = 0
    _indent_size: int = 4

    def __init__(self, *subnodes: "TreeNode | Component") -> None:
        self._subnodes = subnodes

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}>"

    def __str__(self) -> str:
        _str = "{\n"
        TreeNode._indent_in()

        _str += self._get_indentation() + f"\"type\": \"{self.__class__.__name__}\",\n"

        if len(self._subnodes) == 1:
            _str += self._get_indentation() + "\"value\": "
            _str += f"{self._subnodes[0].__str__()}"
        else:
            _str += self._get_indentation() + "\"value\": {\n"

            TreeNode._indent_in()
            for arg in self._subnodes:
                _str += self._get_indentation() + f"\"{arg.__str__()}\"" + ",\n"

            TreeNode._indent_out()
            _str += self._get_indentation() + "}"

        TreeNode._indent_out()
        _str += "\n" + self._get_indentation() + "}"

        return _str

    def eval(self) -> Component:
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
    def __init__(self, *args: TreeNode | Component) -> None:
        super().__init__(*args)


class BinaryOperator(Operator):
    def __init__(self, left: TreeNode | Component,
        right: TreeNode | Component, operator: Token) -> None:
        super().__init__(left, right)
        self._left = left
        self._right = right
        self._operator = operator

    def eval(self) -> tuple[Component, Component]:
        if isinstance(self._left, TreeNode):
            lval = self._left.eval()
        else:
            lval = self._left

        if isinstance(self._right, TreeNode):
            rval = self._right.eval()
        else:
            rval = self._right

        return (lval, rval)


class Concatenation(BinaryOperator):
    def __init__(self, left: TreeNode | Component,
        right: TreeNode | Component) -> None:
        super().__init__(left, right, Token(Operators.CONCATENATOR, "+"))

    def eval(self) -> Component:
        operands = super().eval()
        s = CustomStructure((Component,), (operands[0], operands[1]))
        s._substructures = ()
        return s


class Subtraction(BinaryOperator):
    def __init__(self, left: TreeNode | Component,
        right: TreeNode | Component) -> None:
        super().__init__(left, right, Token(Operators.SUBTRACTOR, "-"))

    def eval(self) -> Component:
        operands = super().eval()
        return CustomStructure((Component,), (operands[0], operands[1]))


class Term(TreeNode):
    def __init__(self, *args: TreeNode | Component) -> None:
        super().__init__(*clean_collection(args))


class Expression(TreeNode):
    def __init__(self, *args: TreeNode | Component) -> None:
        super().__init__(*args)


class Formula(TreeNode):
    def __init__(self, *args: TreeNode | Component) -> None:
        super().__init__(*args)