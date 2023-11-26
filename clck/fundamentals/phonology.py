from clck.fundamentals.component import Component
from clck.fundamentals.phonetics import (
    ConsonantPhone,
    DummyPhone,
    Phone,
    VowelPhone
)
from clck.phonology.articulatory_properties import (
    ArticulatoryProperty,
    MannerOfArticulation,
    PlaceOfArticulation
)


class Phoneme(Component):

    DEFAULT_IPA_PHONEMES: list["Phoneme"] = []

    def __init__(self, _base_phone: Phone) -> None:
        """
        Creates a `Phoneme` instance having one initial allophone.
        """
        super().__init__()
        self._base_phone = _base_phone
        self._symbol = _base_phone.symbol
        self._create_base_properties()

        self._allophones: list[Phone] = [_base_phone]

        if _base_phone.is_default_IPA_phone():
            Phoneme.DEFAULT_IPA_PHONEMES.append(self)

    def __call__(self) -> str:
        return self._symbol

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} {self._symbol}>"

    def __str__(self) -> str:
        s: list[str] = []
        for property in self._base_phone.articulatory_properties:
            s.append(property.name)
        return f"{self.__class__.__name__} {self._transcript} ({' '.join(s)})"

    @property
    def allophones(self) -> tuple[Phone, ...]:
        """The current allophones of this phoneme."""
        return tuple(self._allophones)

    @property
    def base_phone(self) -> Phone:
        """The base phone of this phoneme."""
        return self._base_phone

    @property
    def symbol(self) -> str:
        """The assigned Unicode symbol for this phoneme."""
        return self._symbol

    def _create_output(self) -> str:
        return self._symbol
    
    def _create_transcript(self) -> str:
        return f"/{self._symbol}/"


class Dummy(Phoneme):
    def __init__(self) -> None:
        super().__init__(DummyPhone())


class Consonant(Phoneme):
    def __init__(self, _base_phone: ConsonantPhone) -> None:
        super().__init__(_base_phone)


class Vowel(Phoneme):
    def __init__(self, _base_phone: VowelPhone) -> None:
        super().__init__(_base_phone)


class DummyConsonant(Dummy, Consonant):
    def __init__(self) -> None:
        super().__init__()


class DummyVowel(Dummy, Vowel):
    def __init__(self) -> None:
        super().__init__()


class PhonemicInventory:
    def __init__(self, *phonemes: Phoneme) -> None:
        """
        Creates a new `PhonemicInventory` instance containing the given
        phonemes.

        Parameters
        ----------
        - `phonemes`: the given phonemes to be added to this inventory
        """
        self._phonemes: tuple[Phoneme, ...] = phonemes
        self._consonants: tuple[ConsonantPhone, ...] = self.get_consonants()
        self._vowels: tuple[VowelPhone, ...] = self.get_vowels()

    @property
    def consonants(self) -> tuple[ConsonantPhone, ...]:
        """The consonants of this phonemic inventory."""
        return self._consonants

    @property
    def phonemes(self) -> tuple[Phoneme, ...]:
        """The phonemes of this phonemic inventory."""
        return self._phonemes

    @property
    def vowels(self) -> tuple[VowelPhone, ...]:
        """The vowels of this phonemic inventory."""
        return self._vowels

    def get_consonants(self) -> tuple[ConsonantPhone, ...]:
        """
        Returns all the consonants of this phonemic inventory.
        """
        consonants: list[ConsonantPhone] = []
        for phoneme in self._phonemes:
            if isinstance(phoneme, ConsonantPhone):
                consonants.append(phoneme)
        return tuple(consonants)
    
    def get_phonemes_by_manner_of_articulation(self,
            manner: MannerOfArticulation) -> tuple[Phoneme, ...]:
        """
        Returns all phonemes in this inventory containing the given
        manner of articulation.

        Parameters
        ----------
        - `manner`: the `MannerOfArticulation` property contained in the
            phonemes that will be retrieved
        """
        l: list[Phoneme] = []
        for phoneme in self._phonemes:
            if manner in phoneme.base_phone.articulatory_properties:
                l.append(phoneme)
        return tuple(l)
    
    def get_phonemes_by_place_of_articulation(self,
            place: PlaceOfArticulation) -> tuple[Phoneme, ...]:
        """
        Returns all phonemes in this inventory containing the given
        place of articulation.

        Parameters
        ----------
        - `place`: the `PlaceOfArticulation` property contained in the
            phonemes that will be retrieved
        """
        l: list[Phoneme] = []
        for phoneme in self._phonemes:
            if place in phoneme.base_phone.articulatory_properties:
                l.append(phoneme)
        return tuple(l)
    
    def get_phonemes_by_articulatory_property(self,
            property: ArticulatoryProperty) -> tuple[Phoneme, ...]:
        """
        Returns all phonemes in this inventory containing the given
        articulatory property.

        Parameters
        ----------
        - `property`: the `ArticulatoryProperty` contained in the
            phonemes that will be retrieved
        """
        l: list[Phoneme] = []
        for phoneme in self._phonemes:
            if property in phoneme.base_phone.articulatory_properties:
                l.append(phoneme)
        return tuple(l)

    def get_vowels(self) -> tuple[VowelPhone, ...]:
        """
        Returns all the vowels of this phonemic inventory.
        """
        vowels: list[VowelPhone] = []
        for phoneme in self._phonemes:
            if isinstance(phoneme, VowelPhone):
                vowels.append(phoneme)
        return tuple(vowels)