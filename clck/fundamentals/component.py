from abc import ABC, abstractmethod



class Component(ABC):
    """Class representing all linguistic component, especially the phonemic
    components of a language.
    
    A linguistic component is an abstract representation of a unit of a language
    which is transcriptable (contains an IPA transcript) and can be outputted
    as a string that is readable by the user.
    """

    def __init__(self) -> None:
        """Creates a new `Component` object."""
        self._transcript: str = self._create_transcript()
        self._output: str = self._create_output()

    @abstractmethod
    def _create_transcript(self) -> str:
        """
        Creates the IPA transcript for this component.
        
        Returns
        -------
        - The IPA transcript for this component.
        """
        pass

    @abstractmethod
    def _create_output(self) -> str:
        """
        Creates the output string of this component.

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

