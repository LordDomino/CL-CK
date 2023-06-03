from abc import abstractmethod

from clck.phonology.articulation import ArticulatoryProperty

from .articulation import *



__all__: list[str] = [
	"Phoneme",
	"Consonant",
	"PulmonicConsonant",
	"NonpulmonicConsonant",
	"Vowel",
	"PhonemeCluster",
	"PhonologicalInventory",
	"Cluster"
]



class Phone:
	def __init__(self, symbol: str) -> None:
		self._symbol: str = symbol

	@property
	def symbol(self) -> str:
		return self._symbol


class Phoneme(Phone):
	def __init__(self, symbol: str,
	      artic_properties: tuple[ArticulatoryProperty, ...]) -> None:
		super().__init__(symbol)
		self._artic_properties: tuple[ArticulatoryProperty, ...] = artic_properties


	@abstractmethod
	def __str__(self) -> str:
		return f"{self.name.capitalize()} phoneme, {self._symbol}"


	@abstractmethod
	def __repr__(self) -> str:
		pass
	

	@property
	@abstractmethod
	def name(self) -> str:
		pass



class Consonant(Phoneme):
	def __init__(self, symbol: str,
	      place: Place,
	      manner: Manner,
	      airstream_mechanism: AirstreamMechanism) -> None:
		super().__init__(symbol, (place, manner, airstream_mechanism))
		self._place: Place = place
		self._manner: Manner = manner
		self._airstream_mechanism: AirstreamMechanism = airstream_mechanism


	@abstractmethod	
	def __repr__(self) -> str:
		return f"<Consonant \033[1m{self._symbol}\033[0m>"



class Vowel(Phoneme):
	def __init__(self, symbol: str,
	      height: Height,
		  backness: Backness,
		  roundedness: Roundedness) -> None:
		super().__init__(symbol, (height, backness, roundedness))
		self._height: Height = height
		self._backness: Backness = backness
		self._roundedness: Roundedness = roundedness


	def __repr__(self) -> str:
		return f"<Vowel \033[1m{self._symbol}\033[0m>"


	@property
	def name(self) -> str:
		return f"{self._height.name.capitalize()} {self._backness.name.lower()} {self._roundedness.name.capitalize()} vowel, {self._symbol}"



class PulmonicConsonant(Consonant):
	def __init__(
			self,
			string: str,
			place: Place,
			manner: Manner,
			voiced: bool
	) -> None:
		super().__init__(string, place, manner)
		self._voiced: bool = voiced


	@property
	def name(self) -> str:
		if self._voiced:
			return f"voiced {self._place} {self._manner}"
		else:
			return f"voiceless {self._place} {self._manner}"



class NonpulmonicConsonant(Consonant):

	phoneme_class_name = "non-pulmonic consonant"

	def __init__(
			self,
			string: str,
			place: Place,
			manner: Manner
	) -> None:
		super().__init__(string, place, manner)


class PhonemeCluster:

	def __init__(self, *phonemes: Phoneme) -> None:
		self._phonemes: tuple[Phoneme] = phonemes

	@property
	def phonemes(self) -> tuple[Phoneme]:
		return self._phonemes



class PhonologicalInventory:
	def __init__(self, *phonemes: Phoneme) -> None:
		self._phonemes: tuple[Phoneme] = phonemes
		self._consonants: tuple[Consonant] = self._get_consonants()
		self._vowels: tuple[Vowel] = self._get_vowels()


	@property
	def phonemes(self) -> tuple[Phoneme]:
		return self._phonemes
	

	@property
	def consonants(self) -> tuple[Consonant]:
		return self._consonants


	@property
	def vowels(self) -> tuple[Vowel]:
		return self._vowels
	

	def _get_consonants(self) -> tuple[Consonant]:
		consonants: list[Consonant] = []
		for phoneme in self._phonemes:
			if isinstance(phoneme, Consonant):
				consonants.append(phoneme)
		return tuple(consonants)
	

	def _get_vowels(self) -> tuple[Vowel]:
		vowels: list[Vowel] = []
		for phoneme in self._phonemes:
			if isinstance(phoneme, Vowel):
				vowels.append(phoneme)
		return tuple(vowels)



class Cluster:
	def __init__(self, *phonemes: Phoneme) -> None:
		self._phonemes: tuple[Phoneme] = phonemes

	@property
	def phonemes(self) -> tuple[Phoneme]:
		return self._phonemes