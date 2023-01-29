import re
import random
from typing import Any, Type, Literal
from errors import ClCkDuplicateError



_prefixes_ = {
	"Emic": "dE",
	"Phoneme":  "PH",
	"Grapheme": "GH",
	"Morpheme": "MH",
}



class Emic:
	"""Base class for all emic units in CL-CK."""

	# >>> STATIC CLASS VARIABLES
	# These variables are uninheritable and shouldn't be overriden.
	__emic_elements: list["Emic"] = []

	# >>> NONSTATIC CLASS VARIABLES
	# These are variables that are inherited when extending this Emic class for 
	# different children classes.
	_elements: list["Emic"] = [] # set of all unique Emic units
	_strs: list[str] = [] # set of all unique strings used during instantiations
	_cls_prefix = _prefixes_["Emic"] # This variable must be overriden in the child class

	# >>> __repr__ METHOD CONFIGURATIONS
	# These are default variables for the default representation of the class.
	_repr_id = True # If set to True, the emic unit's ID value is shown.
	_repr_type = False # If set to True, the emic unit's parent class is shown.
		# This also shows if the object is an Emic.

	def __init__(self, string: str, weight: int | float = 1) -> None:

		# During instantiation, the emic object is appended to a base list of all
		# emics.
		Emic.__emic_elements.append(self)

		# The instance of some Emic type will be appended to a class-list of all its
		# emics, a different list from the base-list of elements
		self.__class__._elements = self.__class__._elements + [self]
		self.__class__._strs = self.__class__._strs + [string]

		self._str: str = string
		self._emicval: str = ""
		self._id: int = len(self.__class__._elements)
		self._weight: int | float = weight

	def __repr__(self) -> str:
		"""Sets the representation string of the entire class.
		
		This also defaults other __repr__ methods inherited by children classes."""
		
		repr_str = f"{self._cls_prefix}"

		if self._repr_id:
			repr_str += f"{self._id:0004}"
		if self._repr_type:
			repr_str = f"EMIC-" + repr_str

		repr_str += f" \"{self._emicval}\""		

		return repr_str

	@classmethod
	@property
	def emics(cls) -> tuple["Emic"]:
		"""All emic units of the same type."""
		return tuple(cls._elements)

	@classmethod
	@property
	def size(cls) -> int:
		"""The number of emic units already registered of the same type."""
		if cls == Emic:
			return len(cls.__emic_elements)
		else:
			return len(cls._elements)

	@classmethod
	@property
	def strvals(cls) -> tuple[str]:
		"""All the string values used for this type of Emic."""
		return tuple(cls._strs)

	@property
	def weight(self) -> int | float:
		return self._weight

	def _get_component_str(self) -> str:
		return self._str

	def _is_duplicate(self, obj: Any, set: list | tuple) -> bool:
		"""Checks if given object already exists in the given set of objects."""
		if obj in set:
			return True
		else:
			return False

	def get_clean_str(self) -> str:
		"""Returns this emic's clean string value which has been used during
		instantiation."""
		return self._str



class PrimaryEmic(Emic):
	"""A PrimaryEmic is an emic object which are building block foundations in the
	emic system of CL-CK.
	
	These emics do not contain other emics within them, and they
	are containable only be ConstructiveEmics."""

	def __init__(self, str: str, weight: int | float = 1) -> None:
		if self._is_duplicate(str, self.__class__._strs):
			raise ClCkDuplicateError(f"{self.__class__.__name__} \"{str}\" already exists! Use another str instead.")
		super().__init__(str, weight)



class ConstructiveEmic(Emic):
	"""A ConstructiveEmic is an emic object allowing encapsulation or containment
	of primary emics or other constructive emics."""

	_emicval_strsep: str = ""

	def __init__(self, *objs: Any) -> None:
		self._components: list[Emic] = [*objs]
		pass_str = self.__class__._emicval_strsep.join(self._get_component_str())
		super().__init__(pass_str)

		self._emicval = f"{pass_str}"

	def _get_component_str(self) -> list[str]:
		"""Returns a list of this emic's children component strings."""
		return_list: list[str] = []
		for c in self._components:
			return_list.append(c._get_component_str())
		
		return return_list

	def get_clean_str(self) -> None:
		str_list: list[str] = []

		for c in self._components:
			str_list.append(c.get_clean_str())

		return_str: str = "".join(str_list)

		print(return_str + "\n")
		


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
	
	A phoneme is a representation of sound. In CL-CK, it is expressed as a string.
	"""

	# Class variables
	_cls_prefix = _prefixes_["Phoneme"]
	_elements: list["Phoneme"] = []

	# __repr__ configurations
	# _repr_id = False
	# _repr_id = False

	def __init__(self, str: str, weight: int | float = 1) -> None:
		str = re.sub(re.compile(r'\s+'), '', str)
		super().__init__(str, weight)

		self._emicval = f"/{str}/"
		self._bound_grapheme: Grapheme | None = None

	@property
	def bound_grapheme(self) -> Grapheme | None:
		"""Grapheme bound to the current phoneme. Returns None if no grapheme is
		bound."""
		return self._bound_grapheme



class Morpheme(ConstructiveEmic):

	# Class variables
	_cls_prefix = _prefixes_["Morpheme"]
	_emicval_strsep = "."

	def __init__(self, *phonemes: Phoneme) -> None:
		self._components: list[Phoneme] = [*phonemes]
		super().__init__(*phonemes)



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



def extract(emictype: Type[Emic]) -> list[Emic]:
	return list(emictype.emics)


def find(emictype: Type[Emic], str: str) -> Emic | None:
	emics = emictype.emics
	for e in emics:
		if e._str == str:
			return e
	return None


def Output(emics: list[Emic], quoted: bool = False, spaced: bool = True, stacked: bool = False) -> str:
	r_str = ""
	str_util_left = ""
	str_util_right = ""

	if quoted:
		str_util_left += "\""
		str_util_right += "\""
	if spaced:
		str_util_right += " "
	if stacked:
		str_util_right += "\n"

	r_str = str_util_right + str_util_left
	print_clean_strs: list[str] = []

	for e in emics:
		print_clean_strs.append(e.get_clean_str())

	return_str = final = r_str.join(print_clean_strs)

	if quoted:
		return_str = "\"" + final + "\""

	return return_str