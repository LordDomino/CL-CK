import random
from clck.formula.protosyntax import ActionReferences, GroupingIdentifiers
from clck.fundamentals.component import Component
from clck.fundamentals.phonology import Consonant, Phoneme, PhonemicInventory, Vowel
from clck.fundamentals.syllabics import SyllabicComponent
from clck.phonology.containers import PhonemeGroup


class SyllableGenerator:
    def __init__(self, bank: PhonemicInventory) -> None:
        self._bank = bank
        self._consonants = self.get_consonants()
        self._vowels = self.get_vowels()

    @property
    def bank(self) -> PhonemicInventory:
        """The phonemic inventory used by this generator."""
        return self._bank
    
    def generate(self, formula: str,
        size: int) -> tuple[tuple[Component, ...], ...]:
        rl: list[tuple[Component, ...]] = []
        
        lap = 1
        while lap <= size:
            
            group_net: int = 0
            parenthetical: str = ""
            group_action: None | ActionReferences = None
            execute_action: bool = False
            generated: list[Component] = []

            for char in formula:
                if char == GroupingIdentifiers.OPTIONAL_GROUP_CLOSE.value:
                    group_net -= 1

                if group_net > 0:
                    parenthetical += char
                else:
                    if group_action is not None:
                        execute_action = True

                    if execute_action:
                        if group_action == ActionReferences.OPTIONAL:
                            generated.extend(self._generate_optional(parenthetical, 1))
                            group_action = None
                            execute_action = False
                            parenthetical = ""

                if char == GroupingIdentifiers.OPTIONAL_GROUP_OPEN.value:
                    group_net += 1
                    group_action = ActionReferences.OPTIONAL

            rl.append(tuple(generated))
            lap += 1

        return tuple(rl)

    def get_consonants(self) -> tuple[Consonant, ...]:
        l: list[Consonant] = []
        IPA_consonants = PhonemeGroup.from_type("C", Consonant).phonemes
        for ph in self._bank.phonemes:
            if ph in IPA_consonants and isinstance(ph, Consonant):
                l.append(ph)
        return tuple(l)
    
    def get_vowels(self) -> tuple[Vowel, ...]:
        l: list[Vowel] = []
        IPA_vowels = PhonemeGroup.from_type("V", Vowel).phonemes
        for ph in self._bank.phonemes:
            if ph in IPA_vowels and isinstance(ph, Vowel):
                l.append(ph)
        return tuple(l)
    
    def _generate_optional(self, bank_label: str, size: int) -> tuple[SyllabicComponent | Phoneme, ...]:
        chance = random.randint(0, 1)

        if chance:
            if bank_label == "C":
                return (random.choice(self._consonants),)
            else:
                return ()
        else:
            return ()
