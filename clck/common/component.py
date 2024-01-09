from abc import ABC, abstractmethod

from clck.config import print_debug
# from clck.formulang.common import generate


class Component(ABC):
    """The class representing all linguistic component.
    
    A linguistic component is an abstract representation of a unit of
    language which is transcriptable (contains an IPA transcript) and
    can be outputted as a string that is readable by the user.
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
        """
        Creates and returns the IPA transcript for this component.
        
        Returns
        -------
        - The IPA transcript for this component.
        """
        pass

    @abstractmethod
    def _init_formulang_transcript(self) -> str:
        pass

    @abstractmethod
    def _init_output(self) -> str:
        """
        Creates and returns the output string of this component.

        Returns
        -------
        - The output string of this component.
        """
        pass

    @abstractmethod
    def _init_romanization(self) -> str | None:
        pass

    @property
    def output(self) -> str:
        """The final string representation of this component."""
        return self._output

    @property
    def ipa_transcript(self) -> str:
        """The IPA transcript of this component."""
        return self._ipa_transcript
    
    @property
    def formulang_transcript(self) -> str:
        return self._formulang_transcript
    
    # @classmethod
    # def from_formulang(cls, formula: str) -> "Component":
    #     generated = generate(formula)
    #     if generated == None:
    #         raise Exception("Cannot create component from None")
    #     else:
    #         return generated