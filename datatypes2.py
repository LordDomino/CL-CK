import random
from typing import Any, Iterable, Type
from errors import ClCkDuplicateError



_prefixes_ = {
	"Emic": "dE",
	"Phoneme": "PH",
	"Grapheme": "GH",
	"Morpheme": "MH",
}


class Emic:
	"""Base class for all emic units in CL-CK."""

	# Class variables: statics
	__emic_size: int = 0

	# Class variables: inheritables
	_elements: list = []
	_strs: list[str] = []
	_size: int = 0
	_cls_prefix = _prefixes_["Emic"]

	# __repr__ configurations
	_repr_id = True
	_repr_type = True

	def __init__(self, *objs: Any) -> None:
		Emic.__emic_size += 1
		Emic._elements.append(self)
		self.__class__._elements = self.__class__._elements + [self]
		self.__class__._strs = self.__class__._strs + [*objs]
		self.__class__._size += 1

		self._str = str
		self._emicval = None
		self._id = self.__class__._size

	def __repr__(self) -> str:
		repr_str = f"{self._cls_prefix}"

		if self._repr_id:
			repr_str += f"{self._id:0004}"
		if self._repr_type:
			repr_str = f"EMIC-" + repr_str

		repr_str += f" \"{self._emicval}\""		

		return repr_str

	@classmethod
	@property
	def emics(cls) -> tuple:
		"""All emic units of the same type."""
		return tuple(cls._elements)

	@classmethod
	@property
	def size(cls) -> int:
		"""The number of emic units already registered of the same type."""
		if cls == Emic:
			return cls.__emic_size
		else:
			return cls._size

	def _is_duplicate(self, obj: Any, set: list | tuple) -> bool:
		if str in set:
			return True
		else:
			return False


class PrimaryEmic(Emic):
	def __init__(self, str: str) -> None:
		super().__init__(str)
		if self._is_duplicate(str, self._strs):
			raise ClCkDuplicateError(f"{self.__class__.__name__} \"{str}\" already exists! Use another str instead.")

		self.__class__._elements = self.__class__._elements + [self]
		self.__class__._strs = self.__class__._strs + [str]

		self._str = str
		self._emicval = None
		self._id = self.__class__._size



class ConstructiveEmic(Emic):
	def __init__(self, *objs: Any) -> None:
		super().__init__(*objs)
		self._components: list = [*objs]



class Grapheme(PrimaryEmic):
	"""Class for a single grapheme unit.
	
	A grapheme is the smallest unit of a writing system, representing a phoneme or
	multiple phonemes. In CL-CK, it is expressed as a string."""

	# Class variables
	_cls_prefix = _prefixes_["Grapheme"]

	def __init__(self, str: str) -> None:
		super().__init__(str)

		self._emicval = f"{str}"



class Phoneme(PrimaryEmic):
	"""Class for a single phoneme unit.
	
	A phoneme is a representation of sound. In CL-CK, it is expressed as a
	string."""

	# Class variables
	_cls_prefix = _prefixes_["Phoneme"]

	# __repr__ configurations
	# _repr_id = False
	# _repr_id = False

	def __init__(self, str: str) -> None:
		super().__init__(str)

		self._emicval = f"/{str}/"
		self._bound_grapheme: Grapheme | None = None

	@property
	def bound_grapheme(self) -> Grapheme | None:
		"""Returns the grapheme bound to the current phoneme. Returns None if no 
		grapheme is bound."""
		return self._bound_grapheme



class Morpheme(ConstructiveEmic):

	_cls_prefix = _prefixes_["Morpheme"]

	def __init__(self, *phonemes: Phoneme) -> None:
		super().__init__(*phonemes)

		emicval: str = ""
		for ph in phonemes:
			emicval += f"{ph._str}."

		self._emicval = emicval





class Inventory:
	"""Inventory class to store units and CL-CK objects.
	
	An Inventory object works much like a list, only that it has specific CL-CK
	properties."""

	_emicize_type: Type[Emic] | None = None

	def __init__(self, *args: list | str | Emic) -> None:
		self._e: list = []

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



class PhonemeInventory(Inventory):

	_emicize_type = Phoneme

	def __init__(self, *args: list | str | Emic) -> None:
		super().__init__(*args)
		self._e: list[Phoneme] = []
		self.add(*args)



class GraphemeInventory(Inventory):

	_emicize_type = Grapheme

	def __init__(self, *args: list | str) -> None:
		super().__init__(*args)
		self._e: list[Grapheme] = []
		self.add(*args)


def bind(grapheme: Grapheme, *phonemes: Phoneme) -> list[Phoneme]:
	"""Binds one or more phonemes to a grapheme, then returns all the bound
	phonemes."""
	return_list: list[Phoneme] = []
	for ph in phonemes:
		ph._bound_grapheme = grapheme
		return_list.append(ph)
	
	return return_list


def bind_pairs(graphemes: list[Grapheme] | tuple[Grapheme], *phonemes: list[Phoneme] | tuple[Phoneme]) -> list[list[Phoneme]]:
	return_list: list[list[Phoneme]] = []
	for gh, ph_set in zip(graphemes, phonemes):
		print(gh, ph_set)
		ret_set: list[Phoneme] = []
		for ph in ph_set:
			ph._bound_grapheme = gh
			ret_set.append(ph)
		return_list.append(ret_set)

	return return_list


def randomizer(set: list | tuple, repeats: int = 1) -> list:
	return random.choices(set, k=repeats)