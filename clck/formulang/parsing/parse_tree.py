import random
from typing import Generic, TypeVar
from clck.common.component import Component
from clck.common.structure import ComponentT, ComponentTypes, Structurable
from clck.common.structure import Structure
from clck.phonology.phonemes import DummyPhoneme, Phoneme
from clck.utils import clean_collection


PhonemeAndStructT = TypeVar("PhonemeAndStructT", "FormulangPhoneme", Structure[Component])
TreeNodeT = TypeVar("TreeNodeT", bound="TreeNode[FormulangPhoneme]")

class TreeNode(Generic[PhonemeAndStructT]):
    """Class for all Formulang parse tree nodes.
    """

    _indent_count: int = 0
    _indent_size: int = 4

    def __init__(self, subnodes: tuple["TreeNode[PhonemeAndStructT]", ...],
        brace_level: int) -> None:
        """Creates a new `TreeNode` object.

        Parameters
        ----------
        subnodes : tuple[TreeNode, ...]
            the subnodes of this `TreeNode`
        brace_level : int
            the indicator of this `TreeNode`'s level in the hierarchy of
            structures
        """
        self._subnodes = subnodes
        self._brace_level = brace_level

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} brace_level={self._brace_level}>"

    def __str__(self) -> str:
        _str = "{\n"
        TreeNode._indent_in()

        _str += self._get_indentation(4) + f"type: {self.__class__.__name__} brace_level={self._brace_level},\n"

        if len(self._subnodes) == 1:
            _str += self._get_indentation(4) + "value: "
            _str += f"{self._subnodes[0].__str__()}"
        else:
            _str += self._get_indentation(4) + "value: [\n"

            TreeNode._indent_in()
            for arg in self._subnodes:
                _str += self._get_indentation(4) + f"{arg.__str__()}" + ",\n"

            TreeNode._indent_out()
            _str += self._get_indentation(4) + "]"

        TreeNode._indent_out()
        _str += "\n" + self._get_indentation(4) + "}"

        return _str

    @property
    def brace_level(self) -> int:
        """The indicator of this `TreeNode`'s level in the hierarchy of
        structures.
        """
        return self._brace_level
    
    @property
    def subnodes(self) -> tuple["TreeNode[PhonemeAndStructT]", ...]:
        """The subnodes of this `TreeNode`.
        """
        return self._subnodes

    def eval(self) -> "FormulangPhoneme | FormulangStructure[Phoneme] | None":
        """Evaluates each subnode of this current `TreeNode` and returns
        a resultant `Phoneme`, `Structure`, or `None` based on the
        recursive evaluation in the parse tree.

        Returns
        -------
        FormulangPhoneme | FormulangStructure | None
            the result after recursive evaluation starting from this
            `TreeNode`

        Raises
        ------
        Exception
            if there are no subnodes for this instance
        """
        for subnode in self._subnodes:
            return subnode.eval()
        return None

    def get_json(self, indent: int = 4) -> str:
        """Returns a JSON string copy of the parse tree branch starting
        from this `TreeNode`.

        Parameters
        ----------
        indent : int, optional
            the number of spaces to indent each level in the JSON
            string, by default 4

        Returns
        -------
        str
            the JSON string of the parse tree branch
        """
        _str = "{\n"
        TreeNode._indent_in()

        _str += self._get_indentation(indent) + f"\"type\": \"{self.__class__.__name__} bl={self._brace_level}\",\n"

        if len(self._subnodes) == 1:
            _str += self._get_indentation(indent) + "\"value\": "
            _str += f"{self._subnodes[0].get_json(indent)}"
        else:
            _str += self._get_indentation(indent) + "\"value\": [\n"
            array: list[str] = []
            TreeNode._indent_in()
            for arg in self._subnodes:
                array.append(self._get_indentation(indent) + f"{arg.get_json(indent)}")
            TreeNode._indent_out()
            _str += ",\n".join(array) + "\n"
            _str += self._get_indentation(indent) + "]"


        TreeNode._indent_out()
        _str += "\n" + self._get_indentation(indent) + "}"

        return _str

    def _get_indentation(self, indent_size: int) -> str:
        return " " * TreeNode._indent_count * indent_size
    
    # def _subset(self) -> "TreeNode[PhonemeAndStructT]":
    #     _pure_ellipses = True
    #     for i, subnode in enumerate(self._subnodes):
    #         if isinstance(subnode, EllipsisNode):
    #             continue
    #         else:
    #             _pure_ellipses = False
    #             ellipsis = subnode._subset()
    #             new_subnodes = list(self._subnodes)
    #             new_subnodes[i] = ellipsis
    #             self._subnodes = tuple(new_subnodes)
    #             break

    #     if _pure_ellipses:
    #         return EllipsisNode(self._brace_level)
    #     else:
    #         return self

    @classmethod
    def _indent_in(cls) -> None:
        cls._indent_count += 1

    @classmethod
    def _indent_out(cls) -> None:
        cls._indent_count -= 1


class FormulangPhoneme(DummyPhoneme, TreeNode["FormulangPhoneme, FormulangPhoneme"]):
    def __init__(self, symbol: str, brace_level: int) -> None:
        super().__init__(symbol)
        self._brace_level = brace_level
        self._subnodes = (self,)

    @property
    def brace_level(self) -> int:
        return self._brace_level
    
    @property
    def subnodes(self) -> tuple["FormulangPhoneme"]:
        return self._subnodes
    
    def eval(self) -> "FormulangPhoneme":
        return self
    
    def get_json(self, indent: int = 4) -> str:
        TreeNode._indent_size = indent

        _str: str = ""

        _str += "{\n"
        TreeNode._indent_in()
        _str += self._get_indentation(indent) + f"\"{self.__class__.__name__}\": \"{self.ipa_transcript}\"\n"
        TreeNode._indent_out()
        _str += self._get_indentation(indent) + "}"
        return _str
    
    # def _subset(self) -> TreeNode["EllipsisNode"]:
    #     return EllipsisNode(self._brace_level)

class FormulangStructure(Structure[ComponentT]):
    def __init__(self, components: Structurable[ComponentT], brace_level: int = 0,
        _valid_types: ComponentTypes[ComponentT] = (Component,)) -> None:
        super().__init__(components, _valid_types=_valid_types)
        self._brace_level = brace_level

    def __repr__(self) -> str:
        return super().__str__()

    def __str__(self) -> str:
        return super().__str__()

    @property
    def brace_level(self) -> int:
        return self._brace_level
    
    @property
    def subnodes(self) -> tuple["FormulangStructure[ComponentT]"]:
        return (self,)

    # def eval(self) -> "FormulangStructure[ComponentT]":
    #     return self

    def _init_ipa_transcript(self) -> str:
        return super()._init_ipa_transcript()


class Formula(TreeNode[PhonemeAndStructT]):
    def __init__(self, subnodes: tuple[TreeNode[PhonemeAndStructT], ...]) -> None:
        super().__init__(subnodes, -1)


class Expression(TreeNode[PhonemeAndStructT]):
    def __init__(self, subnodes: tuple[TreeNode[PhonemeAndStructT], ...],
        brace_level: int) -> None:
        super().__init__(subnodes, brace_level)


class Factor(TreeNode[PhonemeAndStructT]):
    def __init__(self, subnodes: tuple[TreeNode[PhonemeAndStructT], ...],
        brace_level: int) -> None:
        super().__init__(subnodes, brace_level)


class Modifier(TreeNode[PhonemeAndStructT]):
    def __init__(self, subnodes: tuple[TreeNode[PhonemeAndStructT], ...],
        brace_level: int) -> None:
        super().__init__(subnodes, brace_level)


class Operation(TreeNode[PhonemeAndStructT]):
    def __init__(self, subnodes: tuple[TreeNode[PhonemeAndStructT], ...],
        brace_level: int) -> None:
        super().__init__(clean_collection(subnodes), brace_level)


class BinaryOperation(Operation[ PhonemeAndStructT]):
    def __init__(self, left: TreeNode[ PhonemeAndStructT],
        right: TreeNode[PhonemeAndStructT] | None, brace_level: int) -> None:
        if right == None:
            super().__init__((left,), brace_level)
        else:
            super().__init__((left, right), brace_level)
        self._left = left
        self._right = right


class Concatenation(Operation[PhonemeAndStructT]):
    def __init__(self, operands: tuple[TreeNode[PhonemeAndStructT], ...],
        brace_level: int) -> None:
        super().__init__(operands, brace_level)
        self._operands = operands

    def eval(self) -> FormulangStructure[PhonemeAndStructT] | None:
        # The following code allows detection of 'chained' operations to
        # add either as structures or phonemes depending on the brace level
        components: list[Phoneme | Structure[Phoneme]] = []

        for o in self._operands:
            operand = o.eval()
            if operand == None:
                continue

            if isinstance(operand, Phoneme):
                components.append(operand)
            else:
                if operand.brace_level == self.brace_level:
                    components.extend(operand.components)
                else:
                    components.append(operand)

        if components == []:
            return None
        else:
            return FormulangStructure(tuple(components), brace_level=self._brace_level)


class Subtraction(Operation[PhonemeAndStructT]):
    def __init__(self, operands: tuple[TreeNode[PhonemeAndStructT], ...],
        brace_level: int) -> None:
        super().__init__(operands, brace_level)
        self._operands = operands

    def eval(self) -> FormulangPhoneme | FormulangStructure | None:
        return super().eval()

class Selection(Operation[PhonemeAndStructT]):
    def __init__(self, options: tuple[TreeNode[PhonemeAndStructT], ...],
            brace_level: int) -> None:
        super().__init__(options, brace_level)
        self._options = options

    def eval(self) -> FormulangPhoneme | FormulangStructure | None:
        selected = random.choice(self._options).eval()
        return selected


class Term(TreeNode[PhonemeAndStructT]):
    def __init__(self, subnodes: tuple[TreeNode[PhonemeAndStructT] | FormulangPhoneme | FormulangStructure, ...],
        brace_level: int) -> None:
        super().__init__(clean_collection(subnodes), brace_level)


class StructureNode(TreeNode[PhonemeAndStructT]):
    def __init__(self, subnode: TreeNode[PhonemeAndStructT], brace_level: int) -> None:
        super().__init__((subnode,), brace_level)
        self._subnode = subnode

    def eval(self) -> FormulangPhoneme | FormulangStructure | None:
        expr = self._subnode.eval()
        if expr == None:
            return None

        if expr.brace_level == self.brace_level:
            if isinstance(expr, StructureNode):
                return expr
            else:
                return FormulangStructure(expr, brace_level=self._brace_level)
        else:
            return FormulangStructure(expr, brace_level=self._brace_level)


class ProbabilityNode(TreeNode[PhonemeAndStructT]):
    def __init__(self, subnodes: tuple[TreeNode[PhonemeAndStructT], ...], brace_level: int,
        probability: float = 0.5) -> None:
        super().__init__(subnodes, brace_level)
        self._probability = probability

    def eval(self) -> FormulangPhoneme | FormulangStructure | None:
        if random.random() < self._probability:
            return super().eval()
        else:
            return None
        

class EllipsisNode(FormulangPhoneme, TreeNode[PhonemeAndStructT]):
    def __init__(self, brace_level: int) -> None:
        super().__init__("...", brace_level)
        self._subnodes = ()

    def __repr__(self) -> str:
        return "<EllipsisNode ...>"
    
    def __str__(self) -> str:
        return "EllipsisNode ..."