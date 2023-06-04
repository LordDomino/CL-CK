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