from abc import ABC, abstractmethod


class Component(ABC):
    def __init__(self) -> None:
        self._transcript: str = self._create_transcript()
        self._output: str = self._create_output()

    @property
    def output(self) -> str:
        """The final string representation of this component."""
        return self._output

    @property
    def transcript(self) -> str:
        """The IPA transcript of this component."""
        return self._transcript

    @abstractmethod
    def _create_transcript(self) -> str:
        """Creates an IPA transcript for this component."""
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