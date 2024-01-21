from abc import ABC
from abc import abstractmethod
from typing import TypeVar

from clck.config import print_debug
# from clck.formulang.common import generate

ComponentT = TypeVar("ComponentT", bound="Component")


class Component(ABC):
    """The class representing all abstract representations of linguistic
    objects from which most classes of CLCK inherit from.
    
    In CLCK, these linguistic objects are the building blocks which
    operate and are operated upon to form various constructs and
    features of a language. As being an abstract representation of a
    unit of language, `Component`s are always transcriptable and can be
    directly previewed as its output string.

    `Component`s contain several base properties which are initialized
    by calling the `__init__` of this class. The base properties are
    `output`, `ipa_transcript`, `formulang_transcript`, `romanization`,
    and `blueprint`.
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
        self._blueprint = self._init_blueprint()
        print_debug(f"{self} base properties initialized")

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, ComponentBlueprint):
            if self._blueprint == __value:
                return True
            else:
                return False
        else:
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

    @abstractmethod
    def _init_blueprint(self) -> "ComponentBlueprint":
        return ComponentBlueprint((self,))

    def set_romanization(self, romanization: str) -> None:
        """Sets the romanized string value for this component.

        Parameters
        ----------
            romanization (str)
                the string to set this component's romanization
        """
        self._romanization = romanization

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
    def blueprint(self) -> "ComponentBlueprint | type":
        return self._blueprint
    

class ComponentBlueprint:
    def __init__(self, comps: tuple["ComponentBlueprint | Component | type[Component]", ...]) -> None:
        self._bp = comps

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, ComponentBlueprint):
            if len(self._bp) != len(__value._bp):
                return False

            for i, b in enumerate(__value._bp):
                a = self._bp[i]
                if a == b:
                    continue
                elif isinstance(a, Component) and isinstance(b, type):
                    if isinstance(a, b):
                        continue
                    else:
                        return False
                elif isinstance(a, type) and isinstance(b, Component):
                    if isinstance(b, a):
                        continue
                    else:
                        return False
                elif isinstance(a, type) and isinstance(b, type):
                    if issubclass(a, b):
                        continue
                    else:
                        return False
                else:
                    return False
            return True
        else:
            return False

    def __str__(self) -> str:
        s: list[str] = []
        for c in self._bp:
            s.append(c.__class__.__name__)
        return f"<ComponentBlueprint ({', '.join(s)})>"
    

class AnyComponent(Component):
    def __init__(self) -> None:
        super().__init__()