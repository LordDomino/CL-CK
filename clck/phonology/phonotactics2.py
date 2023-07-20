from ctypes import Structure
from enum import Enum

from clck.phonology.phonotactics2 import RuleType


class RuleType(Enum):
    FORBID = 0
    FORCE = 1
    ALLOW = 2


def clip_float(value: float | int) -> float:
    """
    Returns a float value of either `1.0` if the value is greater than
    `1.0`, `0.0` if less than `0.0`, or the original value if the value is
    within the range `(0.0, 1.0)`, inclusively.
    """
    if value > 1.0:
        return 1.0
    elif value < 0.0:
        return 0.0
    else:
        return float(value)


def clip_float_to_values(value: float | int, min: float | int,
        max: float | int) -> float:
    """
    Returns `max` if the value is greater than `max`, `min` if less than `min`,
    or the original value if the value is within the range `(min, max)`,
    inclusively.
    """
    if value > max:
        return float(max)
    elif value < min:
        return float(min)
    else:
        return value


class GeneratorRule: ...



class PreGenerationRule(GeneratorRule):
    """The `PreGenerationRule` class declares the specific rules to be obeyed by
    a generator as its guide before generating phonemes.
    """
    def __init__(self) -> None:
        super().__init__()

    # def __init__(self, type: RuleType, condition: ...,
            # chance: float = 1.0, repitition: int = 1) -> None:
        # """Creates a new `PreGenerationRule` instance.
        # 
        # Parameters
        # ----------
        # - `type` is 
        # """
        # super().__init__()
        # self._type = type
        # self._condition = condition
        # self._chance = clip_float(chance)
        # self._repitition = repitition
# 
    # @property
    # def type(self) -> RuleType:
        # """The type of this rule."""
        # return self._type
    # 
    # @property
    # def chance(self) -> float:
        # """The float value within `0.0` and `1.0` which represents the chance of
        # this rule being considered during generation.
        # """
        # return self._chance



class ForbiddenStructures(PreGenerationRule):
    def __init__(self, *structures: Structure) -> None:
        super().__init__()
        self._structures = structures



class PostGenerationRule(GeneratorRule): ...



class Phonotactics:
    """`Phonotactics` is a special container for storing phonotactic information
    such as `SyllableShape` and rules.
    """
    def __init__(self, rules: tuple[GeneratorRule]) -> None:
        self._rules: tuple[GeneratorRule] = rules

    @property
    def rules(self) -> tuple[GeneratorRule]:
        """The tuple of phonotactic rules of this phonotactics."""
        return self._rules