from typing import Type

from .emics import Emic
from .emics import Phoneme
from .emics import Grapheme
from .patterns import Pattern


class Inventory:
	"""Inventory class to store units and CL-CK objects.
	
	An Inventory object works much like a list, only that it has specific CL-CK
	properties."""

	_emicize_type: Type[Emic] | None = None

	def __init__(self, *args: list | str | Emic) -> None:
		self._e: list = [*args]

	def __str__(self) -> str:
		return f"<{self.__class__.__name__} {str(self.elements)}>"

	@property
	def elements(self) -> tuple:
		"""Returns a tuple of all the elements of the inventory."""
		return tuple(self._e)

	def _collect_args(self, *args: list | str | Emic) -> list[str | Emic]:
		"""Function to collect arguments during initialization."""
		return_list: list = []

		for e in args:
			if isinstance(e, list):
				return_list = return_list + e
			elif isinstance(e, str):
				return_list.append(e)
			elif isinstance(e, Emic):
				return_list.append(e)

		return (return_list)

	def _emicize(self, *elements: str | Emic) -> list[Emic] | list[str | Emic]:
		if self._emicize_type is None:
			return list(elements)
		else:
			return_list: list[Emic] = []
			for e in elements:
				if isinstance(e, str):
					return_list.append(self._emicize_type(e))
				elif isinstance(e, self._emicize_type):
					return_list.append(e)
				else:
					raise ValueError(f"Cannot perform emicization from {e} ({e.__class__.__name__}) to emic type {self._emicize_type.__name__}!")

			return return_list

	def add(self, *args: list | str | Emic) -> None:
		self._e += self._emicize(*self._collect_args(*args))

	def print_clean(self) -> None:
		printlist: list[str] = []
		for e in self.elements:
			if isinstance(e, Emic):
				printlist.append(e._emicval)
			else:
				printlist.append(e)

		print(printlist)



class EmicGroup(Inventory):
	def __init__(self, *args: Emic) -> None:
		super().__init__(*args)



class PhonemeInventory(Inventory):

	_emicize_type = Phoneme

	def __init__(self, *args: "list | str | Phoneme | Pattern") -> None:
		pass_list: list[list | str | Phoneme] = []
		
		for e in args:
			if isinstance(e, Pattern):
				pass_list.extend(e.phonemes)

		super().__init__(*pass_list)
		self._e: list[Phoneme] = []
		self.add(*pass_list)



class GraphemeInventory(Inventory):

	_emicize_type = Grapheme

	def __init__(self, *args: list | str) -> None:
		super().__init__(*args)
		self._e: list[Grapheme] = []
		self.add(*args)