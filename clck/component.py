from abc import ABC, abstractmethod

from clck.config import print_debug



class Component(ABC):
    """The class representing all linguistic component.
    
    A linguistic component is an abstract representation of a unit of
    language which is transcriptable (contains an IPA transcript) and
    can be outputted as a string that is readable by the user.
    """

    def __init__(self) -> None:
        """Creates a new `Component` object."""
        self._transcript: str
        self._output: str
        self._are_base_properties_initialized = False

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
    def _create_transcript(self) -> str:
        """
        Creates and returns the IPA transcript for this component.
        
        Returns
        -------
        - The IPA transcript for this component.
        """
        pass

    @abstractmethod
    def _create_output(self) -> str:
        """
        Creates and returns the output string of this component.

        Returns
        -------
        - The output string of this component.
        """
        pass

    @property
    def output(self) -> str:
        """The final string representation of this component."""
        return self._output

    @property
    def transcript(self) -> str:
        """The IPA transcript of this component."""
        return self._transcript

    def _create_base_properties(self) -> None:
        """
        Convenience method to execute common post-initialization to
        work with inheritance.
        """
        self._transcript: str = self._create_transcript()
        self._output: str = self._create_output()
        self._are_base_properties_initialized = True

        if self._are_base_properties_initialized:
            print_debug(f"{self} base properties initialized")