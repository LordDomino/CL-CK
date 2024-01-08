from clck.common.component import Component
from clck.phonetics.articulatory_properties import (
    AirstreamMechanism,
    ArticulatoryProperty,
    ConsonantArticulatoryProperty,
    MannerOfArticulation,
    Phonation,
    PlaceOfArticulation,
    Backness,
    Height,
    Roundedness,
    VowelArticulatoryProperty
)


class Phone(Component):
    """
    The class representing phones in phonetics.

    A phone is a distinguishable speech sound. It is represented by a
    designated IPA symbol and is usually enclosed in square brackets
    during phonetic transcription. All phones contain at least some form
    of articulatory properties.
    """

    DEFAULT_IPA_PHONES: tuple["Phone", ...] = ()
    """The tuple of all phones set as default."""

    def __init__(self, symbol: str,
            articulatory_properties: tuple[ArticulatoryProperty, ...],
            _is_IPA_default: bool = False) -> None:
        """
        Creates a new `Phone` instance with the given articulatory
        properties.
        
        Parameters
        ----------
        - `symbol`: the character representation of the phone. This is
            usually designated as an IPA symbol representing a distinct
            sound from the IPA chart
        - `articulatory_properties`: the tuple of articulatory
            properties of this phone
        - `_is_default`: whether or not to create this as a default
            object
        """
        super().__init__()
        self._is_default = _is_IPA_default
        self._symbol = symbol
        self._articulatory_properties = (articulatory_properties)
        self._create_base_properties()

        if self.is_default_IPA_phone():
            Phone._append_to_defaults(self)

    def __eq__(self, __value: object) -> bool:
        if self.__class__ != __value.__class__:
                return False
        else:
            if isinstance(__value, Phone):
                if self.__dict__ == __value.__dict__:
                    return True
                elif (
                    (self._symbol, *self._articulatory_properties) ==
                    (__value.symbol, *__value.articulatory_properties)):
                    return True
                else:
                    return False
            else:
                return False

    def __call__(self) -> str:
        return self._symbol

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} {self._ipa_transcript}>"

    def __str__(self) -> str:
        s: str = ""
        properties: list[str] = []
        if len(self._articulatory_properties) > 0:
            for property in self._articulatory_properties:
                properties.append(property.name)
            s = f" ({' '.join(properties)})"
        return f"{self.__class__.__name__} {self._ipa_transcript}{s}"

    @property
    def articulatory_properties(self) -> tuple[ArticulatoryProperty, ...]:
        """The articulatory properties of this phone."""
        return self._articulatory_properties

    @property
    def articulatory_property_names(self) -> tuple[str, ...]:
        """The property names of this phoneme."""
        return tuple(self._get_property_names())

    @property
    def name(self) -> str:
        """The name of this phoneme."""
        return self.__str__()

    @property
    def symbol(self) -> str:
        """The assigned Unicode symbol for this phone."""
        return self._symbol

    def is_default_IPA_phone(self) -> bool:
        """
        Returns `True` if this phone is labelled as a default phone,
        otherwise returns `False`.
        """
        return self._is_default

    def _create_output(self) -> str:
        return self._symbol

    def _create_ipa_transcript(self) -> str:
        return f"[{self._symbol}]"
    
    def _create_formulang_transcript(self) -> str:
        return f"{self._symbol}"

    def _get_property_names(self) -> list[str]:
        """
        Returns a list of string corresponding to the names of each
        articulatory property this phone contains.
        """
        return [property.name for property in self._articulatory_properties]

    @classmethod
    def _append_to_defaults(cls, phoneme: "Phone") -> None:
        Phone.DEFAULT_IPA_PHONES = tuple([*Phone.DEFAULT_IPA_PHONES, phoneme])


class DummyPhone(Phone):
    def __init__(self, symbol: str) -> None:
        """
        Creates a `Dummy` instance containing no articulatory
        properties.
        
        Dummy phones should generally be used as placeholders or fillers
        during the generation process. They are always represented by a
        `$` symbol.
        """
        super().__init__(symbol, ())


class ConsonantPhone(Phone):
    """
    The class representing all consonant phones.
    """

    def __init__(self, symbol: str, place: PlaceOfArticulation,
            manner: MannerOfArticulation,
            other_properties: tuple[ConsonantArticulatoryProperty, ...] = (),
            _is_IPA_default: bool = False) -> None:
        """
        Creates a new `Consonant` instance.

        Parameters
        ----------
        - `symbol` - the character representation of the phone. This is
            usually designated as an IPA symbol representing a distinct
            sound from the IPA chart.
        - `place` - the place of articulation of the phone
        - `manner` - the manner of articulation of the phone
        - `other_properties` - other articulatory properties that are
            not stated by default
        - `_is_default` - whether or not to create this as a default
            object
        """
        super().__init__(symbol, (place, manner, *other_properties),
            _is_IPA_default)
        self._place: PlaceOfArticulation = place
        self._manner: MannerOfArticulation = manner


class VowelPhone(Phone):
    def __init__(self, symbol: str, backness: Backness, height: Height,
            roundedness: Roundedness,
            other_properties: tuple[VowelArticulatoryProperty, ...],
            _is_IPA_default: bool = False) -> None:
        super().__init__(symbol, (height, backness, roundedness,
            *other_properties), _is_IPA_default)
        self._height: Height = height
        self._backness: Backness = backness
        self._roundedness: Roundedness = roundedness



class PulmonicConsonantPhone(ConsonantPhone):
    """
    The class representing all pulmonic consonant phones.

    'Pulmonic consonants are consonants that depend upon an egressive
    (outward-flowing) air stream originating in the lungs.'
        Definition from https://shorturl.at/oquxO
    """

    def __init__(self, symbol: str, place: PlaceOfArticulation,
            manner: MannerOfArticulation, voicing: Phonation,
            other_properties: tuple[ConsonantArticulatoryProperty, ...] = (),
            _is_IPA_default: bool = False) -> None:
        """
        Creates a new `PulmonicConsonantPhone` instance.

        A `PulmonicConsonantPhone` instance contains an
        `AirstreamMechanism.PULMONIC` property by default.

        Parameters
        ----------
        - `symbol` - the character representation of the phone. This is
            usually designated as an IPA symbol representing a distinct
            sound from the IPA chart.
        - `place` - the place of articulation of the phone
        - `manner` - the manner of articulation of the phone
        - `voicing` - the voicing (phonation) of the phone's
            articulation. This can be either `Phonation.VOICED` or
            `Phonation.VOICELESS`.
        - `other_properties` - other articulatory properties that are
            not stated by default
        - `_is_default` - whether or not to create this as a default
            object
        """
        super().__init__(symbol, place, manner,
            (AirstreamMechanism.PULMONIC, voicing, *other_properties),
            _is_IPA_default)
        self._airstream_mechanism = AirstreamMechanism.PULMONIC
        self._voicing: Phonation = voicing



class NonpulmonicConsonantPhone(ConsonantPhone):
    def __init__(self, symbol: str, place: PlaceOfArticulation,
            manner: MannerOfArticulation,
            other_properties: tuple[ConsonantArticulatoryProperty, ...] = (),
            _is_IPA_default: bool = False) -> None:
        super().__init__(symbol, place, manner, other_properties,
            _is_IPA_default)



class EjectiveConsonantPhone(NonpulmonicConsonantPhone):
    def __init__(self, symbol: str, place: PlaceOfArticulation,
            manner: MannerOfArticulation,
            other_properties: tuple[ConsonantArticulatoryProperty, ...] = (),
            _is_IPA_default: bool = False) -> None:
        super().__init__(symbol, place, manner, other_properties,
            _is_IPA_default)



class ImplosiveConsonantPhone(NonpulmonicConsonantPhone):
    def __init__(self, symbol: str, place: PlaceOfArticulation,
            manner: MannerOfArticulation,
            other_properties: tuple[ConsonantArticulatoryProperty, ...] = (),
            _is_IPA_default: bool = False) -> None:
        super().__init__(symbol, place, manner, other_properties,
            _is_IPA_default)



class ClickConsonantPhone(NonpulmonicConsonantPhone):
    def __init__(self, symbol: str, place: PlaceOfArticulation,
            manner: MannerOfArticulation,
            other_properties: tuple[ConsonantArticulatoryProperty, ...] = (),
            _is_IPA_default: bool = False) -> None:
        super().__init__(symbol, place, manner, other_properties,
            _is_IPA_default)