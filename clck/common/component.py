from abc import ABC, abstractmethod
from types import UnionType
from typing import TypeAlias, TypeVar, Union

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
    def __init__(self, _default_bp: "ComponentBlueprint") -> None:
        """Initializes common properties of this `Component` instance.
        """
        self._output: str = self._init_output()
        self._ipa_transcript: str = self._init_ipa_transcript()
        self._formulang_transcript: str = self._init_formulang_transcript()
        self._romanization: str | None = self._init_romanization()
        self._default_blueprint: ComponentBlueprint = _default_bp
        self._blueprint: ComponentBlueprint = self._init_blueprint()
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
                    if self._ipa_transcript == __value._ipa_transcript:
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
    def _init_romanization(self) -> str:
        return f"{self.__class__.__name__} romanization WIP"

    @abstractmethod
    def _init_default_bp(self, *args: object, **kwargs: object) -> "ComponentBlueprint":
        """Initializes and returns the default `ComponentBlueprint` that
        this instance obeys. The default component blueprint is the
        specified component blueprint `_default_bp` during this
        component's initialization. Otherwise, it is assigned as the
        class default blueprint returned using the classmethod
        `get_default_blueprint()`.

        Returns
        -------
        ComponentBlueprint
            the default component blueprint of this instance
        """
        return self.__class__.get_default_blueprint()

    @abstractmethod
    def _init_blueprint(self, *args: object, **kwargs: object) -> "ComponentBlueprint":
        pass

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
        """The printable string version that previews the Latin script
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
        """The Formulang representation of this component.
        """
        return self._formulang_transcript

    @property
    def romanization(self) -> str | None:
        return self._romanization
    
    @property
    def blueprint(self) -> "ComponentBlueprint":
        return self._blueprint
    
    @classmethod
    @abstractmethod
    def get_default_blueprint(cls) -> "ComponentBlueprint":
        """Returns the general default component blueprint that all
        instances of this class will obey.

        Returns
        -------
        ComponentBlueprint
            the class' general default component blueprint
        """
        return ComponentBlueprint(Component)


BlueprintElement: TypeAlias = Union["ComponentBlueprint", ComponentT, type[ComponentT]]


class ComponentBlueprint:
    """The class for all component blueprints.

    A component blueprint is a representation of a component's
    structure and sub-components. It describes what CLCK classes or
    types are present in a component's structure hierarchy. Each
    `Component` instance is attributed to a default `ComponentBlueprint`
    during initialization, but it can be attributed to other
    `ComponentBlueprint`s if such component is compatible.

    Blueprint Compatibility
    -----------------------
    Two `ComponentBlueprint` instances, `A` and `B`, can be compared
    together to test their compatibility, that is, if `A`'s blueprint
    elements can be substituted to that of `B`'s.
    ::

        ComponentBlueprint((ConsonantPhoneme,))
        ComponentBlueprint((Phoneme,))

    A component blueprint `A` is compatible to another component
    blueprint `B` if `B` contains the type of `A`'s elements::

        # blueprint of an instance
        A = ComponentBlueprint((ConsonantPhoneme(...),))

        # blueprint of the instance's class
        B = ComponentBlueprint((ConsonantPhoneme,))

        A.is_compatible_to(B)  # -> True
    
    But not if `B` contains a different instance even if it's the same
    type as `A`'s.

    --------------------------------------------------------------------

    
    """
    def __init__(self, *comps: BlueprintElement[ComponentT], strict: bool = True) -> None:
        self._bp = comps
        self._is_strict = strict

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, ComponentBlueprint):
            if self._bp == __value._bp:
                return True
            else:
                return False
        else:
            return False

    def __str__(self) -> str:
        s: list[str] = []
        for c in self._bp:
            if isinstance(c, ComponentBlueprint):
                s.append(c.__class__.__name__)
            elif isinstance(c, Component):
                s.append(c.__str__())
            elif isinstance(c, UnionType):
                s.append(str(c))
            else:
                s.append(c.__name__)
        return f"<ComponentBlueprint ({', '.join(s)})>"

    @property
    def size(self) -> int:
        """The number of allowed blueprint elements of this instance.
        """
        return len(self._bp)

    def is_compatible_to(self, cb: "ComponentBlueprint") -> bool:
        """Returns `True` if this component blueprint instance is
        compatible to the given component blueprint `cb`, that is, if
        the elements of this instance's blueprint are an instance or
        subclass of the elements of `cb`. Otherwise, this returns
        `False`.

        Parameters
        ----------
        cb : ComponentBlueprint
            the component blueprint to test the compatibility

        Returns
        -------
        bool
            whether or not this instance is compatible to the given
            component blueprint
        """

        if cb.is_reverse_compatible(self):
            pass
        elif len(self._bp) != len(cb._bp):
            return False

        for i, b in enumerate(cb._bp):
            a = self._bp[i]
            if self._match_cases(a, b):
                continue
            else:
                return False

        return True

    def is_reverse_compatible(self, cb: "ComponentBlueprint") -> bool:
        """Returns `True` if `cb` is compatible to this instance,
        otherwise, returns `False`.

        Parameters
        ----------
        cb : ComponentBlueprint
            the component blueprint to test the compatibility

        Returns
        -------
        bool
            whether or not the given component blueprint is compatible
            to this instance's component blueprint
        """
        return False

    def _match_cases(self, a: BlueprintElement[ComponentT],
        b: BlueprintElement[ComponentT]) -> bool:
        from clck.common.structure import Structure

        if a == b:
            return True
        elif isinstance(a, AnyBlueprint):
            return False
        elif isinstance(b, type) and issubclass(b, AnyBlueprint):
            return True
        elif isinstance(b, AnyBlueprint) and ComponentBlueprint(a) == b:
            return True
        elif isinstance(a, Structure) and isinstance(b, ComponentBlueprint):
            if a.blueprint.is_compatible_to(b):
                return True
        elif isinstance(a, Component) and isinstance(b, type):
            if isinstance(a, b):
                return True
        elif isinstance(a, type) and isinstance(b, Component):
            if isinstance(b, a):
                return True
        elif isinstance(a, type) and isinstance(b, type):
            if issubclass(a, b):
                return True
        return False


class AnyBlueprint(ComponentBlueprint):
    def __init__(self, *bound: BlueprintElement[ComponentT]) -> None:
        super().__init__()
        self._bound = bound

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, ComponentBlueprint):
            for b in self._bound:
                for a in __value._bp:
                    if self._match_cases(a, b):
                        return True
            return False
        else:
            return False
    
    @property
    def bound(self) -> tuple[ComponentBlueprint | Component | type[Component], ...]:
        """The blueprint elements that this blueprint only allows.
        """
        return self._bound


class FlexibleBlueprint(AnyBlueprint):
    def __init__(self, bound: tuple[BlueprintElement[ComponentT], ...] = (),
        limit_size: int = 0) -> None:
        super().__init__(*bound)
        self._limit_size = limit_size

    @property
    def limit_size(self) -> int:
        return self._limit_size

    def is_reverse_compatible(self, cb: ComponentBlueprint) -> bool:
        if self._limit_size == 0:
            pass
        elif self._limit_size > 0 and cb.size == self._limit_size:
            pass
        else:
            return False

        if self._bound == ():
            return True

        for b in cb._bp:
            for a in self._bound:
                if self._match_cases(b, a):
                    return True
        
        return False