

from ..phonology.phonemes import Phoneme


class Manager: ...



class PhonemesManager(Manager):

    global_phonemes: list[Phoneme] = []

    def __init__(self) -> None:
        
        self.phonemes: list[Phoneme] = []


    def register_phoneme(self, phoneme: Phoneme) -> None:
        """
        Appends the given phoneme to this specific `PhonemeManager`'s index.

        Arguments
        - `phoneme` - the phoneme instance to be appended.
        """
        self.phonemes.append(phoneme)
        PhonemesManager.global_register_phoneme(phoneme)


    def register_phonemes(self, *phonemes: Phoneme) -> None:
        """
        Appens the given phonemes to this specific `PhonemeManager`'s index.

        Arguments
        - `phonemes` - the phonemes instances to be appended.
        """
        self.phonemes.extend(phonemes)
        PhonemesManager.global_register_phonemes(*phonemes)


    @staticmethod
    def global_register_phoneme(phoneme: Phoneme) -> None:
        """
        Appends the given phoneme to the global index of phonemes.
        
        Arguments
        - `phoneme` - the phoneme instance to be appended.
        """
        PhonemesManager.global_register_phonemes(phoneme)


    @staticmethod
    def global_register_phonemes(*phonemes: Phoneme) -> None:
        """
        Appends the given phonemes to the global index of phonemes.

        Arguments
        - `phonemes` - the phoneme instances to be appended.
        """
        PhonemesManager.global_phonemes.extend(phonemes)



class PropertiesManager(Manager): ...
class MorphemesManager(Manager): ...
class VocabularyManager(Manager): ...