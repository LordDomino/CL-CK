import random
from clck.component import Component
from clck.phonology import DummyPhoneme
from clck.syllabics import Structure
from clck.utils import clean_collection


class FormulangPhoneme(DummyPhoneme):
    def __init__(self, symbol: str, brace_level: int) -> None:
        super().__init__(symbol)
        self._brace_level = brace_level

    @property
    def brace_level(self) -> int:
        return self._brace_level


class FormulangStructure(Structure):
    def __init__(self, _valid_comp_types: tuple[type[Component], ...],
        components: tuple[Component, ...], brace_level: int) -> None:
        super().__init__(_valid_comp_types, components)
        self._brace_level = brace_level

    @property
    def brace_level(self) -> int:
        return self._brace_level

    def _create_ipa_transcript(self) -> str:
        return super()._create_ipa_transcript()


class TreeNode:

    _indent_count: int = 0
    _indent_size: int = 2

    def __init__(self, subnodes: tuple["TreeNode | FormulangPhoneme | FormulangStructure", ...],
        brace_level: int) -> None:
        self._subnodes = subnodes
        self._brace_level = brace_level

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} brace_level={self._brace_level}>"

    def __str__(self) -> str:
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

    @property
    def brace_level(self) -> int:
        return self._brace_level

    def eval(self) -> FormulangPhoneme | FormulangStructure:       
        for subnode in self._subnodes:
            if isinstance(subnode, TreeNode):
                return subnode.eval()
            else:
                return subnode
        raise Exception("Evaluation error")

    def _get_indentation(self) -> str:
        return " " * TreeNode._indent_count * TreeNode._indent_size
    
    @classmethod
    def _indent_in(cls) -> None:
        cls._indent_count += 1

    @classmethod
    def _indent_out(cls) -> None:
        cls._indent_count -= 1


class Formula(TreeNode):
    def __init__(self, subnodes: tuple[TreeNode | FormulangPhoneme | FormulangStructure, ...]) -> None:
        super().__init__(subnodes, -1)


class Expression(TreeNode):
    def __init__(self, subnodes: tuple[TreeNode | FormulangPhoneme | FormulangStructure, ...],
        brace_level: int) -> None:
        super().__init__(subnodes, brace_level)


class SumNode(TreeNode):
    def __init__(self, subnodes: tuple[TreeNode | FormulangPhoneme | FormulangStructure, ...], brace_level: int) -> None:
        super().__init__(subnodes, brace_level)


class Factor(TreeNode):
    def __init__(self, subnodes: tuple[TreeNode | FormulangPhoneme | FormulangStructure, ...], brace_level: int) -> None:
        super().__init__(subnodes, brace_level)


class Modifier(TreeNode):
    def __init__(self, subnodes: tuple[TreeNode | FormulangPhoneme | FormulangStructure, ...], brace_level: int) -> None:
        super().__init__(subnodes, brace_level)


class Operation(TreeNode):
    def __init__(self, subnodes: tuple[TreeNode | FormulangPhoneme | FormulangStructure, ...],
        brace_level: int) -> None:
        super().__init__(clean_collection(subnodes), brace_level)


class BinaryOperation(Operation):
    def __init__(self, left: TreeNode,
        right: TreeNode | None, brace_level: int) -> None:
        if right == None:
            super().__init__((left,), brace_level)
        else:
            super().__init__((left, right), brace_level)
        self._left = left
        self._right = right


class Concatenation(BinaryOperation):
    def __init__(self, left: TreeNode, right: TreeNode | None,
        brace_level: int) -> None:
        super().__init__(left, right, brace_level)

    def eval(self) -> FormulangStructure:
        # The following code allows detection of 'chained' operations to
        # add either as structures or phonemes depending on the brace level
        left = self._left.eval()

        components: list[Component] = []
        if isinstance(left, FormulangPhoneme):
            components.append(left)
        else:
            if left.brace_level == self.brace_level:
                components.extend(left.components)
            else:
                components.append(left)

        if isinstance(self._right, TreeNode):
            right = self._right.eval()

            if isinstance(right, FormulangPhoneme):
                components.append(right)
            else:
                if right.brace_level == self.brace_level:
                    components.extend(right.components)
                else:
                    components.append(right)

        return FormulangStructure((Component,), tuple(components),
            self._brace_level)


class Subtraction(BinaryOperation):
    def __init__(self, left: TreeNode,
        right: TreeNode, brace_level: int) -> None:
        super().__init__(left, right, brace_level)


class Selection(BinaryOperation):
    def __init__(self, left: TreeNode, right: TreeNode | None,
        brace_level: int) -> None:
        super().__init__(left, right, brace_level)

    def eval(self) -> FormulangPhoneme | FormulangStructure:
        left = self._left.eval()

        if self._right is None:
            return left
        else:
            right = self._right.eval()
            return random.choice((left, right))


class Term(TreeNode):
    def __init__(self, subnodes: tuple[TreeNode | FormulangPhoneme | FormulangStructure, ...],
        brace_level: int) -> None:
        super().__init__(clean_collection(subnodes), brace_level)


class StructureNode(TreeNode):
    def __init__(self, subnode: Expression,
        brace_level: int) -> None:
        super().__init__((subnode,), brace_level)
        self._subnode = subnode

    def eval(self) -> FormulangPhoneme | FormulangStructure:
        expr = self._subnode.eval()
        if isinstance(expr, FormulangPhoneme) and self._brace_level == 1:
            return FormulangStructure((Component,), (expr,), self._brace_level)
        else:
            return expr