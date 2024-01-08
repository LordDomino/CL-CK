from clck.common.component import Component
from clck.phonetics.phones import ConsonantPhone
from clck.phonetics.phones import DummyPhone
from clck.phonetics.phones import Phone
from clck.phonetics.phones import VowelPhone
from clck.phonetics.articulatory_properties import ArticulatoryProperty
from clck.phonetics.articulatory_properties import MannerOfArticulation
from clck.phonetics.articulatory_properties import PlaceOfArticulation


class Phoneme(Component):

    DEFAULT_IPA_PHONEMES: list["Phoneme"] = []
    DEFAULT_IPA_SYMBOLS: list[str] = []

    def __init__(self, base_phone: Phone) -> None:
        """
        Creates a `Phoneme` instance having one initial allophone.

        Parameters
        ----------
        - `base_phone`: is the initial allophone (a `Phone` instance)
            assigned to this phoneme
        """
        super().__init__()
        self._base_phone = base_phone
        self._symbol = base_phone.symbol
        self._create_base_properties()

        self._allophones: list[Phone] = [base_phone]

        if base_phone.is_default_IPA_phone():
            Phoneme.DEFAULT_IPA_PHONEMES.append(self)
            Phoneme.DEFAULT_IPA_SYMBOLS.append(self._symbol)

    def __call__(self) -> str:
        return self._symbol

    def __repr__(self) -> str:
        s: list[str] = []
        for property in self._base_phone.articulatory_properties:
            s.append(property.name)
        return f"<{self.__class__.__name__} {self._ipa_transcript}>"

    def __str__(self) -> str:
        return f"{self.__class__.__name__} {self._ipa_transcript}"

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
    
    def _create_ipa_transcript(self) -> str:
        return f"/{self._symbol}/"

    def _create_formulang_transcript(self) -> str:
        return f"/{self._symbol}/"


class DummyPhoneme(Phoneme):
    def __init__(self, symbol: str = "$") -> None:
        super().__init__(DummyPhone(symbol))


class ConsonantPhoneme(Phoneme):

    IPA_CONSONANTS: list["ConsonantPhoneme"] = []

    def __init__(self, _base_phone: ConsonantPhone) -> None:
        super().__init__(_base_phone)
        if _base_phone.is_default_IPA_phone():
            ConsonantPhoneme.IPA_CONSONANTS.append(self)


class VowelPhoneme(Phoneme):
    def __init__(self, _base_phone: VowelPhone) -> None:
        super().__init__(_base_phone)


class DummyConsonantPhoneme(DummyPhoneme, ConsonantPhoneme):
    def __init__(self) -> None:
        super().__init__()


class DummyVowelPhoneme(DummyPhoneme, VowelPhoneme):
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
        Returns all (consonant) phonemes in this inventory containing
        the given place of articulation. Note that the
        `PlaceOfArticulation` property is only attributable to
        `Consonant` instances, thus it is not applicable to
        non-consonantal phonemes.

        Parameters
        ----------
        - `place`: the `PlaceOfArticulation` property contained in the
            phonemes that will be retrieved
        """
        l: list[Phoneme] = []
        for phoneme in self._phonemes:
            # safeguard code to prevent non-consonant phonemes to be
            # accepted in the if statement (see second clause of if
            # statement)
            if (place in phoneme.base_phone.articulatory_properties and
                isinstance(phoneme.base_phone, ConsonantPhoneme)):
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