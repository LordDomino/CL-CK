class ProtoTokenizer:
    def __init__(self, string: str) -> None:
        self._string = string
        self._cursor = 0

    def has_more_tokens(self) -> bool:
        if self._cursor < len(self._string):
            return True
        else:
            return False

    def get_next_token(self):
        if not self.has_more_tokens():
            return None
        
        string = self._string[0:self._cursor]

        if not isinstance(string[0], int):
            number = ""
            while ()