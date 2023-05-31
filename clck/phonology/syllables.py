from .phonemes import Phoneme



class SyllableComponent: ...

class Onset(SyllableComponent): ...
class Nucleus(SyllableComponent): ...
class Coda(SyllableComponent): ...



class Syllable:
    def __init__(self, *phonemes: Phoneme) -> None:
        self._phonemes: tuple[Phoneme] = phonemes
        self._final_representation: str = self._get_final_representation()


    def __repr__(self) -> str:
        return f"<Syllable \033[1m{self._final_representation}\033[0m>"


    @property
    def phonemes(self) -> tuple[Phoneme]:
        return self._phonemes
    

    @property
    def final_representation(self) -> str:
        return self._final_representation


    def _get_final_representation(self) -> str:
        symbol_list: list[str] = []
        for phoneme in self._phonemes:
            symbol_list.append(phoneme.symbol)
        return "".join(symbol_list)


class SyllableShape:
    def __init__(self, onset: str, nucleus: str, coda: str) -> None:
        self._onset: str = onset
        self._nucleus: str = nucleus
        self._coda: str = coda
        self._pattern: str = "".join([self._onset, self._nucleus, self._coda]).upper()
        self._length: int = len(self._pattern)
        self._pattern_types: list[str] = list(set(self._pattern))


    @property
    def pattern(self) -> str:
        return self._pattern
    

    @property
    def length(self) -> int:
        return self._length