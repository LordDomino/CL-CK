import string
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

	# __repr__ configurations
	# _repr_id = False
	# _repr_id = False

	def __init__(self, str: str, weight: int | float = 1) -> None:
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



class Pattern:
	"""Class for all CL-CK patterns.
	
	A pattern is a sequence of phonemes and values ordered in the correct syntax,
	indicating how a morpheme could be formed."""

	SYN_OPENINGS: str = "([{"
	SYN_CLOSINGS: str = ")]}"
	SYN_GROUPERS: str = SYN_OPENINGS + SYN_CLOSINGS
	SYN_SPLITTERS: str = "|"
	SYN_SEPARATOR: str = "."
	SYN_OPERATORS: str = "+-"
	SYN_OTHERS: str = "\\"
	SYN_SYMBOLS: str = SYN_SPLITTERS + SYN_GROUPERS + SYN_OPERATORS + SYN_OTHERS + SYN_SEPARATOR
	VALIDS: str = SYN_SYMBOLS + string.ascii_letters

	def __init__(self, pattern_string: str, chance: str = "A", split: bool = False,
	grouped: bool = False, top: bool = True) -> None:
		self._is_split: bool = split
		self._is_grouped: bool = grouped
		self._is_top: bool = top
		self._fragments: list[Phoneme | Pattern] = []

		self.phonemes: list[Phoneme] = []
		self.pattern_string: str = pattern_string
		self.chance: str = chance

		self._syntaxize(self.pattern_string)
		self.phonemes = self._extract_phonemes()

	def __repr__(self) -> str:
		return f"PATTERN \"{self.pattern_string}\""

	def _extract_phonemes(self) -> list[Phoneme]:
		return_list: list[Phoneme] = []
		for _f in self._fragments:
			if isinstance(_f, Pattern):
				return_list.extend(_f._extract_phonemes())
			elif isinstance(_f, Phoneme):
				return_list.append(_f)

		return return_list

	def _validate_match(self, openers: str, closers: str) -> bool:
		if len(openers) != len(closers):
			return False

		validity: str = ""

		for o, c in zip(openers, closers[::-1]):
			if f"{o}{c}" in ("()", "[]", "{}"):
				validity += "1"
			else:
				validity += "0"

		if "0" in validity:
			return False
		else:
			return True


	def _syntaxize(self, pattern_string: str) -> None:

		specimen: str = pattern_string
		unit: str = ""
		nest: int = 0
		split: int = -1

		# Refine specimen by checking if the pattern is grouped
		spec_ends: str = f"{self.pattern_string[0]}{self.pattern_string[-1]}"

		# Checks if the pattern is 
		if self._is_grouped or spec_ends in ("()", "[]", "{}"):
			_ind = 0
			_n = 0
			for _i, c in enumerate(specimen):
				if c in Pattern.VALIDS:
					if c in Pattern.SYN_OPENINGS:
						_n += 1
					elif c in Pattern.SYN_CLOSINGS:
						_n -= 1
					
					if _n == 0:
						_ind = _i
						break

			if _ind == len(specimen) - 1:
				self._is_grouped = True

				if self._is_top is False:
					specimen = specimen[1:-1]
				
				if f"{self.pattern_string[0]}{self.pattern_string[-1]}" == "()":
					self.chance = "A"
				elif f"{self.pattern_string[0]}{self.pattern_string[-1]}" == "[]":
					self.chance = "R"

		for p in Pattern.SYN_GROUPERS:
			if p in specimen:
				nest = 0
				break

		# Search for top-level operations
		_fragments: list = []

		for c in specimen:
			if c in Pattern.VALIDS:
				if c in Pattern.SYN_OPENINGS:
					nest += 1
				elif c in Pattern.SYN_CLOSINGS:
					nest -= 1
				
				if c in Pattern.SYN_SPLITTERS and nest > 0:
					split *= 1
				elif c in Pattern.SYN_SPLITTERS and nest == 0 and split < 0:
					split *= -1
			
			else:
				raise ValueError(f"Unknown symbol \"{c}\"")	

		for c in specimen:
			if c in Pattern.VALIDS:
				unit += c

				if c in Pattern.SYN_SPLITTERS + ".":
					self._is_split = True

					if nest == 0 and unit != "":
						_fragments.append(unit[0:-1])
						unit = ""

				elif c in Pattern.SYN_OPENINGS:
					self._is_grouped = True

					if split != 1 and nest == 0:
						if unit[0:-1] != "":
							_fragments.append(unit[0:-1])
						unit = unit[-1]
					nest += 1

				elif c in Pattern.SYN_CLOSINGS:
					nest -= 1
					if split != 1 and nest == 0:
						_fragments.append(unit)
						unit = ""
				
				elif c in Pattern.SYN_SEPARATOR:
					if nest == 0 and unit != "":
						_fragments.append(unit[0:-1])
						unit = ""
		
		if unit != "":
			if self._is_split:
				_fragments.append(unit)
			else:
				if self._is_grouped:
					_fragments.append(unit)
				else:
					self._fragments.append(Phoneme(unit))

		for unit in _fragments:
			_is_protophoneme: bool = True
			if self._is_split:
				_chance: str = "R"
			else:
				_chance: str = "A"
			
			for c in unit:
				if c in Pattern.SYN_SYMBOLS:
					_is_protophoneme = False
					self._fragments.append(Pattern(unit, chance=_chance, top=False))
					break

			if _is_protophoneme:
				self._fragments.append(Pattern(unit, chance=_chance, top=False))


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