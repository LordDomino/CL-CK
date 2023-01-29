from emics import *



class Pattern:
	"""Class for all CL-CK patterns.
	
	A pattern is a sequence of phonemes and values ordered in the correct syntax,
	indicating how a morpheme could be formed."""

	patterns: list["Pattern"] = []

	# >>> Syntax constants defining valid characters in Pattern syntax
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
	SYNTAX_SEPARATOR: str = ".+"

	# Combiner and dropper
	SYNTAX_SUBTRACTOR: str = "-"

	# Other miscellaneous symbols for future use
	SYNTAX_OTHERS: str = "\\"

	# All pattern symbols
	SYNTAX_SYMBOLS: str = SYNTAX_GROUPERS + SYNTAX_SELECTOR + SYNTAX_SEPARATOR + SYNTAX_SUBTRACTOR + SYNTAX_OTHERS

	# All valid characters
	SYNTAX_VALIDS: str = SYNTAX_SYMBOLS + SYNTAX_LETTERS + SYNTAX_WHITESPACE

	def __init__(self, name: str, pattern_string: str, _is_enclosed: bool = False,
	_is_partitioned: bool = False, _is_protophoneme: bool = True,
	_is_main_pattern: bool = True, _generation_chance: Literal["ALW", "RND", "SEL", "SUB"] = "ALW") -> None:
		
		# Default pattern properties
		self._is_enclosed: bool = _is_enclosed # determines whether or not the pattern is enclosed by any grouping pair
		self._is_partitioned: bool = _is_partitioned # determines whether or not the pattern is partitioned by selector operations
		self._is_protophoneme: bool = _is_protophoneme # determines whether or not the pattern is purely alphabetic, thus, ready to be converted to a phoneme
		self._is_main_pattern: bool = _is_main_pattern # determines whether or not the pattern is the topmost pattern
		self._generation_chance = _generation_chance # determines if the generation of this pattern is selected (as in "S") or always (as in "A")

		self._fragments: list[Phoneme | Pattern] = []
		self.name: str = name
		self.phonemes: list[Phoneme] = []
		self.pattern_string: str = pattern_string

		if self._is_main_pattern:
			Pattern.patterns.append(self)

		self._compile(self.pattern_string)
		self.phonemes = self._extract_phonemes()

	def __repr__(self) -> str:
		return f"PATTERN \"{self.name}\" {self.pattern_string}"

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
					self._generation_chance = "ALW"
				elif spcm_ends == "[]": # meanwhile square brackets indicate a "selected" generation chance
					self._generation_chance = "RND"

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

			# elif c in Pattern.SYNTAX_SUBTRACTOR:
			# 	if nest > 0 or self._is_partitioned:
			# 		pass
			# 	else:
			# 		if cltr != c:
			# 			fragments.append()

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
				pattern = Pattern("CHILD", frag, _is_protophoneme = is_protophoneme, _is_main_pattern = False, _generation_chance = "SEL")
				self._fragments.append(pattern)
			else:
				pattern = Pattern("CHILD", frag, _is_protophoneme = is_protophoneme, _is_main_pattern = False, _generation_chance = "ALW")
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
				if self._generation_chance == "RND":
					random_chance = True
			
			for frag in self._fragments:
				if isinstance(frag, Pattern):
					return_string += frag.execute()
				elif isinstance(frag, Phoneme):
					return_string += frag.get_clean_str()
		
			if random_chance:
				return_string = random.choice(["", return_string])

			return return_string



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