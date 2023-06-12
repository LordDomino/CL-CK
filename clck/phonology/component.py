from abc import ABC, abstractmethod


class Component(ABC):
    def __init__(self) -> None:
        self._transcript: str = self._create_transcript()


    @property
    def transcript(self) -> str:
        """The IPA transcript of this component."""
        return self._transcript


    @abstractmethod
    def _create_transcript(self) -> str:
        """Creates an IPA transcript for this component."""
        pass