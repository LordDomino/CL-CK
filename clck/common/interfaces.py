from abc import ABC, abstractmethod

from clck.common.component import ComponentBlueprint


class Initializable(ABC):
    """Interface class for implementing initialization methods in CLCK
    classes that need parameter processing in super constructors.
    
    Super constructor calls in some CLCK classes require its parameters
    to be pre-formatted before it is passed on to the `Component` class'
    `__init__()` method. This abstract class, thus, serves as an
    equivalent of an interface, and this (including the abstract methods
    within) can be implemented via multiple inheritance. Note, however, 
    that the methods written in here are for the sake of consistency and
    convention.
    """

    @abstractmethod
    def _init_ipa_transcript(self) -> str:
        """Initializes and returns the IPA transcription of this
        component.

        The string representation of how this component might be
        transcribed as an IPA phonemic transcription.

        Returns
        -------
        - `str` the IPA transcription of this component
        """
        pass

    @abstractmethod
    def _init_formulang_transcript(self) -> str:
        """Initializes and returns the Formulang transcription of this
        component.

        Returns
        -------
        - `str` the Formulang transcription of this component
        """
        pass

    @abstractmethod
    def _init_output(self) -> str:
        """Initializes and returns the output string of this component.
        
        The output string of a component is its printable string version
        that previews the 'actual' orthographic representation of it.

        Returns
        -------
        - `str` the output string of this component
        """
        pass

    @abstractmethod
    def _init_romanization(self) -> str:
        return f"{self.__class__.__name__} romanization WIP"

    @abstractmethod
    def _init_default_bp(self, *args: object, **kwargs: object) -> "ComponentBlueprint":
        """Initializes and returns the default `ComponentBlueprint` that
        this instance obeys.
        
        The default component blueprint is the specified component
        blueprint `_default_bp` during this component's initialization.
        Otherwise, it is assigned as the class default blueprint
        returned using the classmethod `get_default_blueprint()`.

        Returns
        -------
        - `ComponentBlueprint` the default component blueprint of this
            instance
        """
        pass

    @abstractmethod
    def _init_blueprint(self, *args: object, **kwargs: object) -> "ComponentBlueprint":
        pass