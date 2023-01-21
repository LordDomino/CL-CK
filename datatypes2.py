import random
import string
import time
from typing import Any, Type
from errors import ClCkDuplicateError



_prefixes_ = {
	"Emic": "dE",
	"Phoneme":  "PH",
	"Grapheme": "GH",
	"Morpheme": "MH",
}



class Emic:
	"""Base class for all emic units in CL-CK."""

	# Class variables: statics
	__emic_size: int = 0
	__emic_elements: list["Emic"] = []

	# Class variables: class inheritables
	_elements: list["Emic"] = []
	_strs: list[str] = []
	_size: int = 0
	_cls_prefix = _prefixes_["Emic"]

	# __repr__ configurations
	_repr_id = True
	_repr_type = False

	def __init__(self, string: str, weight: int | float = 1) -> None:
		Emic.__emic_size += 1
		Emic.__emic_elements.append(self)
		self.__class__._elements = self.__class__._elements + [self]
		self.__class__._strs = self.__class__._strs + [string]
		self.__class__._size += 1

		self._str = string
		self._emicval: str = ""
		self._id = self.__class__._size
		self._weight: int | float = weight

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
	def emics(cls) -> tuple["Emic"]:
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

	@classmethod
	@property
	def strvals(cls) -> tuple[str]:
		"""All the string values used for this type of Emic."""
		return tuple(cls._strs)

	def _is_duplicate(self, obj: Any, set: list | tuple) -> bool:
		if obj in set:
			return True
		else:
			return False

	@property
	def weight(self) -> int | float:
		return self._weight

	def _get_component_str(self) -> str:
		return self._str

	def print_clean(self) -> str:
		print(self._str)
		return self._str



class PrimaryEmic(Emic):
	def __init__(self, str: str, weight: int | float = 1) -> None:
		if self._is_duplicate(str, self.__class__._strs):
			raise ClCkDuplicateError(f"{self.__class__.__name__} \"{str}\" already exists! Use another str instead.")
		super().__init__(str, weight)



class ConstructiveEmic(Emic):

	_emicval_strsep: str = ""

	def __init__(self, *objs: Any) -> None:
		self._components: list[Emic] = [*objs]
		pass_str = self.__class__._emicval_strsep.join(self._get_component_str())
		super().__init__(pass_str)

		self._emicval = f"{pass_str}"

	def _get_component_str(self) -> list[str]:
		return_list: list[str] = []
		for c in self._components:
			return_list.append(c._get_component_str())
		
		return return_list

	def print_clean(self) -> None:
		str_list: list[str] = []

		for c in self._components:
			str_list.append(c.print_clean())

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
	
	A phoneme is a representation of sound. In CL-CK, it is expressed as a
	string."""

	# Class variables
	_cls_prefix = _prefixes_["Phoneme"]

	# __repr__ configurations
	# _repr_id = False
	# _repr_id = False

	def __init__(self, str: str, weight: int | float = 1) -> None:
		super().__init__(str, weight)

		self._emicval = f"/{str}/"
		self._bound_grapheme: Grapheme | None = None

	@property
	def bound_grapheme(self) -> Grapheme | None:
		"""Returns the grapheme bound to the current phoneme. Returns None if no 
		grapheme is bound."""
		return self._bound_grapheme




class Morpheme(ConstructiveEmic):

	_cls_prefix = _prefixes_["Morpheme"]
	_emicval_strsep = "."

	def __init__(self, *phonemes: Phoneme) -> None:
		self._components: list[Phoneme] = [*phonemes]
		super().__init__(*phonemes)



class Inventory:
	"""Inventory class to store units and CL-CK objects.
	
	An Inventory object works much like a list, only that it has specific CL-CK
	properties."""

	_emicize_type: Type[Emic] | None = None

	def __init__(self, *args: list | str | Emic) -> None:
		self._e: list = []

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



class Pattern:
	def __init__(self, patternstring: str, grouped: bool = False) -> None:
		self._is_grouped: bool = grouped
		self.patternstring: str = patternstring
		self.fragments: list[Phoneme | Pattern] = []

		self.syntaxize(self.patternstring)

	def __repr__(self) -> str:
		return f"PATTERN \"{self.patternstring}\""

	def syntaxize(self, patternstring: str) -> None:
		
		SYN_OPENINGS: str = "[("
		SYN_CLOSINGS: str = "])"
		SYN_GROUPERS: str = SYN_OPENINGS + SYN_CLOSINGS
		SYN_COMPARATORS: str = "|"

		specimen: str = patternstring
		unit: str = ""
		nest: int = 0
		is_nested: bool = False
		is_single: bool = True
		is_adding: bool = True

		if self._is_grouped:
			specimen = specimen[1:-1]

		for i, c in enumerate(specimen):
			if c in SYN_GROUPERS:
				if c in SYN_OPENINGS:
					if specimen[i] == specimen[-1]: # Check if opening is at the end
						raise IndexError("Cannot have opening nest at the end!")
					elif specimen[i + 1] in SYN_CLOSINGS: # Check if group is empty
						raise IndexError("Cannot have empty groupings!")
					
					# If opening character succeeds error tests, then add it to the character
					if nest == 0 and unit != "": # Ensures that unit is saved before nesting
						if is_single: # Check if pattern is a sole string of alphabets,
							self.fragments.append(Phoneme(unit))
						else: # otherwise, append it as a another pattern
							self.fragments.append(Pattern(unit))
						unit = ""
					nest += 1
					unit += c
					print(unit)
				elif c in SYN_CLOSINGS:
					nest -= 1
					unit += c
					print(unit)
					if nest == 0 and unit != "":
						self.fragments.append(Pattern(unit, True))
						unit = ""
			elif c in SYN_COMPARATORS:
				unit += c
				is_single = False
				print(unit)
			elif c in list(string.ascii_letters):
				unit += c
				print(unit)

				# Check if next character is a comparator only in topmost level
				if nest == 0 and unit != "":
					if specimen[i + 1] in SYN_COMPARATORS:
						pass
			
			if nest == 0 and unit != "":
				if specimen[i + 1] in SYN_COMPARATORS:
					pass

		
		if unit != "":
			if is_single:
				self.fragments.append(Phoneme(unit))
			else:
				self.fragments.append(Pattern(unit))

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
		print_clean_strs.append(e.print_clean())

	return_str = final = r_str.join(print_clean_strs)

	if quoted:
		return_str = "\"" + final + "\""

	return return_str