from abc import abstractmethod

from .articulation import *



class Phone:
	def __init__(self, symbol: str) -> None:
		self._symbol: str = symbol

	def __call__(self) -> str:
		return self._symbol

	@property
	def symbol(self) -> str:
		return self._symbol



class Phoneme(Phone):
	def __init__(self, symbol: str,
	      articulatory_properties: tuple[ArticulatoryProperty, ...]) -> None:
		super().__init__(symbol)
		self._articulatory_properties: tuple[ArticulatoryProperty, ...] = (
			articulatory_properties)
		self._name = self.name


	def __str__(self) -> str:
		return f"{self.__class__.__name__} phoneme, {self._symbol}"


	def __repr__(self) -> str:
		return f"<{self.__class__.__name__} {self._symbol}>"
	

	@property
	@abstractmethod
	def name(self) -> str:
		pass



class Consonant(Phoneme):
	def __init__(self, symbol: str,
	      	place: Place, manner: Manner) -> None:
		self._place: Place = place
		self._manner: Manner = manner
		super().__init__(symbol, (place, manner))



class Vowel(Phoneme):
	def __init__(self, symbol: str,
		  backness: Backness,
	      height: Height,
		  roundedness: Roundedness) -> None:
		self._height: Height = height
		self._backness: Backness = backness
		self._roundedness: Roundedness = roundedness
		super().__init__(symbol, (height, backness, roundedness))


	@property
	def name(self) -> str:
		return (f"{self._height.name.capitalize()} "
			f"{self._backness.name.lower()} "
			f"{self._roundedness.name.capitalize()} vowel, {self._symbol}")



class PulmonicConsonant(Consonant):
	def __init__(self, symbol: str, place: Place, manner: Manner,
	      voicing: Voicing) -> None:
		self._voicing: Voicing = voicing
		super().__init__(symbol, place, manner)


	@property
	def name(self) -> str:
		return (f"{self._voicing.name.capitalize()} {self._place.name.lower()} "
			f"{self._manner.name.capitalize()} vowel, {self._symbol}")



class NonpulmonicConsonant(Consonant):
	def __init__(self, symbol: str, place: Place, manner: Manner) -> None:
		super().__init__(symbol, place, manner)



class EjectiveConsonant(NonpulmonicConsonant):
	def __init__(self, symbol: str, place: Place, manner: Manner) -> None:
		super().__init__(symbol, place, manner)



class ImplosiveConsonant(NonpulmonicConsonant):
	def __init__(self, symbol: str, place: Place, manner: Manner) -> None:
		super().__init__(symbol, place, manner)



class ClickConsonant(NonpulmonicConsonant):
	def __init__(self, symbol: str, place: Place, manner: Manner) -> None:
		super().__init__(symbol, place, manner)