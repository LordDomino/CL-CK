from typing import Type
from errors import ClCkDuplicateError



_prefixes_ = {
	"Emic": "dE",
	"Phoneme": "PH",
	"Grapheme": "GH",
}


class Emic:
	"""Base class for all emic units in CL-CK."""

	# Class variables
	_elements: list = []
	_strs: list[str] = []
	_size: int = 0
	_cls_prefix = _prefixes_["Emic"]

	# __repr__ configurations
	_repr_id = False
	_repr_type = False

	def __init__(self, str: str) -> None:
		if self._is_duplicate(str):
			raise ClCkDuplicateError(f"{self.__class__.__name__} \"{str}\" already exists! Use another str instead.")

		self.__class__._elements.append(self)
		self.__class__._strs.append(str)
		self.__class__._size += 1

		self._str = str
		self._emicval = None
		self._id = self.__class__._size

	def _is_duplicate(self, str: str) -> bool:
		if str in Emic._strs:
			return True
		else:
			return False

	def __repr__(self) -> str:
		repr_str = f"{self.__class__._cls_prefix}"

		if self._repr_id:
			repr_str += f"{self._id:0004}"
		if self._repr_type:
			repr_str = f"EMIC-" + repr_str

		repr_str += f" \"{self._emicval}\""		

		return repr_str

	@classmethod
	@property
	def elements(cls) -> tuple:
		"""All elements of the class."""
		return tuple(cls._elements)

	@classmethod
	@property
	def size(cls) -> int:
		"""The number of elements."""
		return cls._size



class Phoneme(Emic):
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
		self._grapheme: Grapheme | None = None



class Grapheme(Emic):
	"""Class for a single grapheme unit.
	
	A grapheme is the smallest unit of a writing system, representing a phoneme or
	multiple phonemes. In CL-CK, it is expressed as a string."""

	# Class variables
	_cls_prefix = _prefixes_["Grapheme"]

	def __init__(self, str: str) -> None:
		super().__init__(str)

		self._emicval = str



class Inventory:
	"""Inventory class to store units and CL-CK objects.
	
	An Inventory object works much like a list, only that it has specific CL-CK
	properties."""
	def __init__(self, *args: list | str | Emic) -> None:
		self._e: list = []
		self.add(*args, emictype=None)


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

	def _emicize(self, emictype: Type[Emic] | None = None, *elements: str | Emic) -> list[Emic] | list[str | Emic]:
		if emictype is None:
			return list(elements)
		else:
			return_list: list[Emic] = []
			for e in elements:
				if isinstance(e, str):
					return_list.append(emictype(e))
				else:
					raise ValueError()

			return return_list

	def add(self, *args: list | str | Emic, emictype: Type[Emic] | None = None) -> None:
		self._e += self._emicize(None, *self._collect_args(*args))

	def extract(self, emictype: Emic | None, *elements) -> list:
		return_list: list = []
		for e in elements:
			if isinstance(e, str):
				return_list.append(Phoneme(e))
			elif isinstance(e, Emic):
				return_list.append(e)
		return return_list

	def get_elements(self) -> tuple:
		"""Returns a tuple of all the elements of the inventory."""
		return tuple(self._e)



class PhonemeInventory(Inventory):
	def __init__(self, *args: list | str | Emic) -> None:
		super().__init__(*args)
		self.add(*args, emictype=Phoneme)



class GraphemeInventory(Inventory):
	def __init__(self, *args: list | str) -> None:
		super().__init__(*args)
		self.add(*args, emictype=Grapheme)
		


def bind(grapheme: Grapheme, *phonemes: Phoneme) -> list[Phoneme]:
	"""Binds one or more phonemes to a grapheme, then returns all the binded
	phonemes."""
	return_list: list[Phoneme] = []
	for phoneme in phonemes:
		phoneme._grapheme = grapheme
		return_list.append(phoneme)
	
	return return_list
