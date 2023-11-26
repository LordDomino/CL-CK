from enum import Enum, auto


class GroupingIdentifiers(Enum):
    OPTIONAL_GROUP_OPEN = "("
    OPTIONAL_GROUP_CLOSE = ")"

class PhonemeGroupIdentifiers(Enum):
    CONSONANTS = "C"
    VOWELS = "V"

class ActionReferences(Enum):
    OPTIONAL = auto()
    REQUIRED = auto()