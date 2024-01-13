from abc import ABC
from abc import abstractmethod
import time

import clck
from clck.config import print_debug
# from clck.formulang.common import generate


class Component(ABC):
    """The class representing all abstract representations of linguistic
    objects from which most classes of CLCK inherit from.
    
    In CLCK, these linguistic objects are the building blocks which
    operate and are operated upon to form various constructs and
    features of a language. As being an abstract representation of a
    unit of language, `Component`s are always transcriptable and can be
    directly previewed as its output string.

    `Component`s contain several base properties which are initialized
    upon from a subclass super call. The base properties are `output`,
    `ipa_transcript`, `formulang_transcript`, `romanization`, and
    `blueprint`.
    """

    @abstractmethod
    def __init__(self) -> None:
        """Convenience method to execute common post-initialization to
        work with inheritance.
        """
        self._output: str = self._init_output()
        self._ipa_transcript: str = self._init_ipa_transcript()
        self._formulang_transcript: str = self._init_formulang_transcript()
        self._romanization: str | None = self._init_romanization()
        self._blueprint = self._init_component_blueprint()

        print_debug(f"{self} base properties initialized")

    def __eq__(self, __value: object) -> bool:
        if self.__class__ != __value.__class__:
            return False
        else:
            if isinstance(__value, Component):
                if self.__dict__ == __value.__dict__:
                    return True
                else:
                    return False
            else:
                return False

    @abstractmethod
    def _init_ipa_transcript(self) -> str:
        """Initializes and returns the IPA transcription of this
        component.

        The string representation of how this component might be
        transcribed as an IPA phonemic transcription.

        Returns
        -------
        str
            the IPA transcription of this component.
        """
        pass

    @abstractmethod
    def _init_formulang_transcript(self) -> str:
        pass

    @abstractmethod
    def _init_output(self) -> str:
        """Initializes and returns the output string of this component.
        
        The output string of a component is its printable string version
        that previews the 'actual' orthographic representation of it.

        Returns
        -------
        str
            the output string of this component.
        """
        pass

    @abstractmethod
    def _init_romanization(self) -> str | None:
        pass

    #@abstractmethod
    def _init_component_blueprint(self) -> "ComponentBlueprint":
        pass

    @property
    def output(self) -> str:
        """The printable string version that previews the 'actual'
        orthographic representation of this component.
        """
        return self._output

    @property
    def ipa_transcript(self) -> str:
        """The string representation of how this component might be
        transcribed as an IPA phonemic transcription.
        """
        return self._ipa_transcript
    
    @property
    def formulang_transcript(self) -> str:
        return self._formulang_transcript

    @property
    def romanization(self) -> str | None:
        return self._romanization
    
    @property
    def blueprint(self) -> "ComponentBlueprint":
        return self._blueprint

    
    def set_romanization(self, romanization: str) -> None:
        """Sets the romanized string value for this component.

        Parameters
        ----------
            romanization (str)
                the string to set this component's romanization
        """
        self._romanization = romanization

class ComponentBlueprint:
    def __init__(self, id: "str | tuple[ComponentBlueprint | str, ...]") -> None:
        self._id = id
        self._level = self._get_level()
        self._structure = self._get_structure()

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, ComponentBlueprint):
            if __value._structure == self._structure:
                return True
            else:
                return False
        else:
            return False

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} size={len(self._id)}>"

    @property
    def id(self) -> "str | tuple[ComponentBlueprint | str, ...]":
        return self._id
    
    @property
    def level(self) -> int:
        return self._level
    
    @property
    def structure(self) -> str:
        return self._structure

    def _get_structure(self) -> str:
        if isinstance(self._id, str):
            return self._id
        else:
            bp: list[str] = []
            for cb in self._id:
                if isinstance(cb, str):
                    bp.append(cb)
                else:
                    bp.append(cb._get_structure())
            return f"{{{'+'.join(bp)}}}"
    
    def _get_level(self) -> int:
        if isinstance(self._id, str):
            return 0
        else:
            lvl = 0
            for cb in self._id:
                if isinstance(cb, ComponentBlueprint):
                    lvl += 1 + cb._get_level()
                    break
            return lvl

    def subset(self, structure: str) -> bool: 
        ast = clck.Formulang.generate_ast(structure)

        from clck.formulang.parsing.fl_parser import EllipsisNode

        ast = ast._subset()
        print(ast)
        print(ast.__class__)

        while not isinstance(ast, EllipsisNode):
            ast = ast._subset()
            print(ast.__class__)