from .phonemes import Phoneme



class SyllableComponent:
    def __init__(self, *components: "SyllableComponent | Phoneme") -> None:
        self.components: tuple[SyllableComponent | Phoneme] = components

    
    def get_phonemes(self) -> list[Phoneme]:
        phonemes: list[Phoneme] = []
        for component in self.components:
            if isinstance(component, Phoneme):
                phonemes.append(component)
            else:
                component.get_phonemes()
        return phonemes

    
    def remove_duplicates(self) -> None:
        self.components = tuple([*set(self.components)])

class Onset(SyllableComponent): ...
class Rhyme(SyllableComponent): ...
class Nucleus(Rhyme): ...
class Coda(Rhyme): ...



class Syllable:
    def __init__(self, onset: Onset, nucleus: Nucleus, coda: Coda) -> None:
        self._onset: Onset = onset
        self._nucleus: Nucleus = nucleus
        self._coda: Coda = coda
        self._phonemes: tuple[Phoneme] = tuple(onset.get_phonemes() + nucleus.get_phonemes() + coda.get_phonemes())
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
    

    @property
    def onset_shape(self) -> str:
        return self._onset
    

    @property
    def nucleus_shape(self) -> str:
        return self._nucleus


    @property
    def coda_shape(self) -> str:
        return self._coda