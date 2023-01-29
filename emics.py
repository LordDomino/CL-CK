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

	# Syntax constants defining valid characters in Pattern syntax

	# Alphabet letters
	SYNTAX_UPPERCASE: str = "abcdefghijklmnopqrstuvwxyz"
	SYNTAX_LOWERCASE: str = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
	SYNTAX_LETTERS: str = SYNTAX_UPPERCASE + SYNTAX_LOWERCASE

	# Whitespaces
	SYNTAX_WHITESPACE: str = " \t\v\n\r\f"

	# Parenthicals
	SYNTAX_OPENINGS: str = "([{"
	SYNTAX_CLOSINGS: str = ")]}"
	SYNTAX_GROUPERS: str = SYNTAX_OPENINGS + SYNTAX_CLOSINGS

	# Selector
	SYNTAX_SELECTOR: str = "|"

	# Separator/splitter
	SYNTAX_SEPARATOR: str = "."

	# Combiner and dropper
	SYNTAX_OPERATORS: str = "+-"

	# Other miscellaneous symbols for future use
	SYNTAX_OTHERS: str = "\\"

	# All pattern symbols
	SYNTAX_SYMBOLS: str = SYNTAX_GROUPERS + SYNTAX_SELECTOR + SYNTAX_SEPARATOR + SYNTAX_OPERATORS + SYNTAX_OTHERS

	# All valid characters
	SYNTAX_VALIDS: str = SYNTAX_SYMBOLS + SYNTAX_LETTERS + SYNTAX_WHITESPACE

	def __init__(self, pattern_string: str, _is_enclosed: bool = False,
	_is_partitioned: bool = False, _is_protophoneme: bool = True,
	_is_main_pattern: bool = True, _generation_chance: Literal["A", "R", "S"] = "A") -> None:
		
		# Default pattern properties
		self._is_enclosed: bool = _is_enclosed # determines whether or not the pattern is enclosed by any grouping pair
		self._is_partitioned: bool = _is_partitioned # determines whether or not the pattern is partitioned by selector operations
		self._is_protophoneme: bool = _is_protophoneme # determines whether or not the pattern is purely alphabetic, thus, ready to be converted to a phoneme
		self._is_main_pattern: bool = _is_main_pattern # determines whether or not the pattern is the topmost pattern
		self._generation_chance: Literal["A", "R", "S"] = _generation_chance # determines if the generation of this pattern is selected (as in "S") or always (as in "A")

		self._fragments: list[Phoneme | Pattern] = []
		self.phonemes: list[Phoneme] = []
		self.pattern_string: str = pattern_string

		self._compile(self.pattern_string)
		self.phonemes = self._extract_phonemes()

	def __repr__(self) -> str:
		return f"PATTERN \"{self.pattern_string}\""

	def _compile(self, pattern_string: str) -> None:

		spcm: str = pattern_string # specimen string
		cltr: str = "" # collector string
		nest: int = 0 # nesting index
		slct: int = -1 # selection index
		c: str = "" # character loop-through variable

		# 0. VALIDITY CHECK
		# Basic loop-through to see if any invalid characters are present in the pattern.
		for c in spcm:
			if c not in Pattern.SYNTAX_VALIDS:
				raise ValueError("Unknown character " + c)

		# Check if this pattern is a protophoneme
		for c in pattern_string:
			if c in Pattern.SYNTAX_SYMBOLS:
				self._is_protophoneme = False
				break
		
		# If this pattern is a protophoneme, already append it as a phoneme
		if self._is_protophoneme:
			try:
				self._fragments.append(Phoneme(pattern_string))
			except:
				for phoneme in Phoneme._elements:
					if pattern_string == phoneme._str:
						self._fragments.append(phoneme)
			return

		# Check if the pattern has paired parenthicals
		if _is_parenthicals_paired(pattern_string, Pattern.SYNTAX_OPENINGS, Pattern.SYNTAX_CLOSINGS) is False:
			raise ValueError("Parenthicals not paired correctly!")


		# 1. ENCLOSURE IDENTIFICATION
		# Retrieve the first and last char of the pattern
		spcm_ends: str = f"{self.pattern_string[0]}{self.pattern_string[-1]}"
		
		# Compare the retrieved string to the pairings
		if self._is_enclosed or spcm_ends in ("()", "[]", "{}"):
			stop_index = 0 # index at which the parenthicals fully close

			# Loop through the specimen and check if the first opening parenthesis
			# fully closes in the middle.
			for i, c in enumerate(spcm):
				if c in Pattern.SYNTAX_OPENINGS:
					nest += 1
				elif c in Pattern.SYNTAX_CLOSINGS:
					nest -= 1
				
				# If nesting index reaches 0, then the parenthicals have fully closed.
				# Break the loop and proceed.
				if nest == 0:
					stop_index = i
					break

			# Check if the nest have fully closed right at the end of the pattern.
			if stop_index == len(spcm) - 1:
				self._is_enclosed = True # Set IS_ENCLOSED if the stop index is the same as the index of the end parenthicals

				# If the pattern is not the main pattern, then clear the enclosure groupings.
				if self._is_main_pattern is False:
					spcm = spcm[1:-1]
				
				if spcm_ends == "()": # parenthesis indicate an "always" generation chance
					self._generation_chance = "A"
				elif spcm_ends == "[]": # meanwhile square brackets indicate a "selected" generation chance
					self._generation_chance = "R"

		del spcm_ends

		if spcm == "":
			raise ValueError("Cannot have empty parenthical!")

		# 2. TOP-ORDER OPERATION (TOOPER) IDENTIFICATION
		# Loop through the characters of the specimen.
		for c in spcm:
			# Perform nest indexing by incrementing or decrementing the nest index
			# every time an opening or closing grouper is found.
			if c in Pattern.SYNTAX_OPENINGS:
				nest += 1
			elif c in Pattern.SYNTAX_CLOSINGS:
				nest -= 1
			
			# If the nesting is ongoing and a selector is found, keep the value of
			# selector index as -1 by multiplying 1 to its initial -1 value.
			if c in Pattern.SYNTAX_SELECTOR and nest > 0:
				slct *= 1
			
			# Otherwise, if a selector is found and its index is -1 outside any nests,
			# set its index as 1 by multiplying -1 to its -1 value.
			elif c in Pattern.SYNTAX_SELECTOR and nest == 0 and slct == -1:
				slct *= -1

		# Set the boolean IS_PARTITIONED to true if the selector operator is dominant
		# over the parenthicals, otherwise, it should remain as false.
		if slct == 1:
			self._is_partitioned = True
		else:
			self._is_partitioned = False

		# 3. PATTERN FRAGMENTATION
		# Perform a loop-through of the specimen to analyze the pattern character by
		# character.

		fragments: list[str] = []

		for c in spcm:
			if c in Pattern.SYNTAX_WHITESPACE:
				continue
			cltr += c # add the character to the collector dump. All alphabet letters are unconditionally added.

			if c in Pattern.SYNTAX_SELECTOR: # CASE A: The encountered character is a selector.
				if self._is_partitioned: # If the pattern is partitioned at the top-order,
					if nest == 0 and cltr != "": # check if currently not nesting and if unit is not empty,
						if cltr != c:
							fragments.append(cltr[0:-1]) # then append.
							cltr = ""
						else:
							raise ValueError("Selector operator must have one unit on both left and right side!")

			elif c in Pattern.SYNTAX_OPENINGS: # CASE B: The encountered character is a parenthical opening.	
				if nest == 0:
					if self._is_partitioned is False:
						if cltr != c:
							fragments.append(cltr[0:-1])
							cltr = cltr[-1]
				nest += 1

			elif c in Pattern.SYNTAX_CLOSINGS: # CASE C: The encountered character is a parenthical closing.
				nest -= 1	
				if nest == 0:
					if self._is_partitioned is False:
						if cltr != "":
							fragments.append(cltr)
							cltr = ""
			
			elif c in Pattern.SYNTAX_SEPARATOR + "+": # CASE D: The encountered character is a unit separator.
				if nest > 0 or self._is_partitioned:
					pass
				else:
					if cltr != c:
						fragments.append(cltr[0:-1])
					cltr = ""

		# 3. LEFTOVER COLLECTION
		if cltr != "":
			fragments.append(cltr)

		del c, nest, cltr, slct, spcm

		# 4. FRAGMENT CONVERSION
		for frag in fragments:
			is_protophoneme: bool = True

			# Check if fragment is a protophoneme
			for c in frag:
				if c in Pattern.SYNTAX_SYMBOLS:
					is_protophoneme = False # If any symbol is found, then the fragment is not a protophoneme
					break
			
			if self._is_partitioned:
				pattern = Pattern(frag, _is_protophoneme = is_protophoneme, _is_main_pattern = False, _generation_chance = "S")
				self._fragments.append(pattern)
			else:
				pattern = Pattern(frag, _is_protophoneme = is_protophoneme, _is_main_pattern = False, _generation_chance = "A")
				self._fragments.append(pattern)

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

		for o, c in zip(openers, closers):
			if f"{o}{c}" in ("()", "[]", "{}"):
				validity += "1"
			else:
				validity += "0"

		if "0" in validity:
			return False
		else:
			return True
	
	def execute(self) -> str:
		return_string: str = ""

		if self._is_partitioned:
			selector_list: list[str] = []

			for frag in self._fragments:
				if isinstance(frag, Pattern):
					selector_list.append(frag.execute())
				elif isinstance(frag, Phoneme):
					selector_list.append(frag.get_clean_str())

			return_string = random.choice(selector_list)
			return return_string

		else:
			random_chance: bool = False

			if self._is_enclosed:
				if self._generation_chance == "R":
					random_chance = True
			
			for frag in self._fragments:
				if isinstance(frag, Pattern):
					return_string += frag.execute()
				elif isinstance(frag, Phoneme):
					return_string += frag.get_clean_str()
		
			if random_chance:
				return_string = random.choice(["", return_string])

			return return_string



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


def _is_parenthicals_paired(string: str, openings: str, closings: str) -> bool:
	if len(openings) != len(closings):
		raise ValueError(f"Openings of length {len(openings)} not same as closings of length {len(closings)}!")
	
	open_index: list[int] = [0] * len(openings)
	close_index: list[int] = [0] * len(closings)

	for c in string:
		if c not in openings + closings:
			continue

		if c in openings:
			for i, op in enumerate(openings):
				if c == op:
					open_index[i] += 1
					break

		elif c in closings:
			for i, cl in enumerate(closings):
				if c == cl:
					close_index[i] += 1
					break

	for o, c in zip(open_index, close_index):
		if o != c:
			return False

	return True


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