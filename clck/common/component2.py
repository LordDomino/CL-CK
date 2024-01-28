from abc import ABC, abstractmethod


class Component2:
    def __init__(self, output: str, ipa_transcript: str,
        formulang_transcript: str) -> None:
        self._output = output
        self._ipa_transcript = ipa_transcript
        self._formulang_transcript = formulang_transcript

    @property
    def output(self) -> str:
        return self._output
    
    @property
    def ipa_transcript(self) -> str:
        return self._ipa_transcript
    
    @property
    def formulang_transcript(self) -> str:
        return self._formulang_transcript



class Structure2(Component2):
    def __init__(self, comps: tuple[str, ...]) -> None:
        super().__init__(self._init_output(comps), self._init_output(comps), self._init_output(comps))

    def _init_output(self, comps: tuple[str, ...]) -> str:
        return "".join(comps)


class Substructure(Structure2):
    def __init__(self, comps: tuple[str, ...]) -> None:
        super().__init__(comps)



s = Substructure(("a", "b", "c"))