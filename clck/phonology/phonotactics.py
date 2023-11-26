from ..fundamentals.component import Component
from ..fundamentals.phonetics import Phone
from ..fundamentals.component import Component
from ..fundamentals.component import Component
from ..config import printwarning
from ..fundamentals.structure import *
from ..fundamentals.syllabics import SyllabicComponent


class PhonotacticRule:
    """
    The `PhonotacticRule` is a class representing a real-world phonotactic rule.
    """

    def __init__(self) -> None:
        """
        Creates a `PhonotacticRule` object.
        
        Arguments:
        - `valid_structures` - the list of valid structures where this rule can
        apply.
        """
        pass



class PhonotacticRuleAction(ABC):
    @abstractmethod
    def execute(self, *components: Component) -> tuple[Component]:
        pass

class PhonotacticRulePlacement: ...

# PRA Probabilities
RULE_MAY = 0.5
RULE_MUST_NOT = 0.0
RULE_MUST_ALWAYS = 1.0

class PRA_Occur(PhonotacticRuleAction):
    def execute(self, *components: Component) -> tuple[Component]:
        return super().execute(*components)
    

class PRA_Replace(PhonotacticRuleAction):
    def execute(self, *components: Component) -> tuple[Component]:
        return super().execute(*components)
    


class PRA_Delete(PhonotacticRuleAction):
    def execute(self, *components: Component) -> tuple[Component]:
        return super().execute(*components)

# PRA Actions
OCCUR = PRA_Occur()
REPLACE = PRA_Replace()
DELETE = PRA_Delete()

# PRA Placements
BEFORE = PhonotacticRulePlacement()
AFTER = PhonotacticRulePlacement()
ANYWHERE_BEFORE = PhonotacticRulePlacement()
ANYWHERE_AFTER = PhonotacticRulePlacement()



class PositionalRule(PhonotacticRule):
    def __init__(self, target_structure: type[SyllabicComponent | Phone],
            bank: tuple[SyllabicComponent] | None,
            probability: float, action: PhonotacticRuleAction,
            placement: PhonotacticRulePlacement,
            _condition: None = None) -> None:
        """Creates a new `PositionalRule` instance.
        
        Parameters
        ----------
        - `bank` - the tuple of syllabic components that will be used when this
            rule is executed.
        - `probability` - a float between 0 and 1 indicating the chance of this
            rule to be executed. Constants `RULE_MAY`, `RULE_MUST_NOT`, and
            `RULE_MUST_ALWAYS` correspond to values `0.5`, `0.0`, and `1.0`,
            respectively.
        - `action` - the type of positional rule when executing this rule.
        - `placement` - indicates which places 
        """
        super().__init__()
        self._target_structure: type[SyllabicComponent | Phone] = target_structure
        self._bank: tuple[SyllabicComponent] | None = bank
        self._probability: float = probability
        self._action: PhonotacticRuleAction = action
        self._placement: PhonotacticRulePlacement = placement
        self._coverage: int = 1

    @property
    def bank(self) -> tuple[SyllabicComponent] | None:
        return self._bank
    
    @property
    def probability(self) -> float:
        return self._probability
    
    @property
    def action(self) -> PhonotacticRuleAction:
        return self._action
    
    @property
    def placement(self) -> PhonotacticRulePlacement:
        return self._placement

    def execute(self, specimen: SyllabicComponent,
            anonymous_bank: tuple[SyllabicComponent] | None = None,
            override: bool = False) -> bool:
        """Executes this rule on to the specified specimen. Returns `True` if
        the specified specimen obeys the implementation of this rule.

        Parameters
        ----------
        - `specimen` - the component to which this rule will be applied.
        - `anonymous_bank` - is an optional tuple to serve as the `bank` during
            implementation. Defaults to `None`. 
        - `override_bank` - states whether or not the given `anonymous_bank`
            overrides this rule's original `bank` during implementation.
            Defaults to `False`.

        If during the construction of this rule `bank` was set to `None`, then
        the parameter `anonymous_bank` must be provided, regardless of the
        boolean in `override_bank`. Meanwhile, if a bank was provided, then
        `anonymous_bank` may still be used in the implementation, only if
        `override_bank` is `True`.
        """

        # It may be possible for a user to assign a bank and still override it
        # with an anonymous one, so we need to know which will be used.
        bank = self._get_execute_bank(
            anonymous_bank, override)

        self._action.execute()

    def is_anonymous(self) -> bool:
        """Returns `True` if this rule is anonymous.
        
        An anonymous `PhonotacticRule` is anonymous if `bank` is set to `None`
        during construction, which allows the use of different banks every time
        `execute()` is called.
        """
        if self._bank is None:
            return True
        else:
            return False

    def _create_dummy_structure(self, specimen: SyllabicComponent) -> None:
        """Creates a dummy structure that will be used during the application of
        this rule.
        """
        for c in specimen.components: ...


    def _get_execute_bank(self, anonymous_bank: tuple[SyllabicComponent] | None,
            override: bool) -> tuple[SyllabicComponent]:
        """Returns the actual bank to be used in the execution of this rule."""

        if self._bank is None:
            if anonymous_bank is None:
                raise ValueError(f"Parameter for anonymous_bank must be "
                                 f"provided since {self} is anonymous.")
            elif override is True:
                printwarning(f"Anonymous bank override is unnecessary for "
                             f"anonymous rules.")
                exec_bank = anonymous_bank
            else:
                exec_bank = anonymous_bank
        else:
            if anonymous_bank is None:
                if override:
                    printwarning(f"Bank override is unnecessary for "
                        f"unspecified anonymous_bank.")
                    exec_bank = self._bank
                else:
                    exec_bank = self._bank
            else:
                if override:
                    exec_bank = anonymous_bank
                else:
                    printwarning(f"Argument for anonymous_bank is unnecessary "
                        f"for this rule's unoverriden bank.")
                    exec_bank = self._bank

        return exec_bank

    # def _get_phonemes_before_target(self, specimen: SyllabicComponent) -> tuple[SyllabicComponent | Phoneme]:
    #     components: list[SyllabicComponent | Phoneme] = []
    #     for c in specimen.components:
    #         if isinstance(c, Phoneme):
    #             components.append(c)
    #         else:
    #             components.append(c)
    #             c.