from clck.config import print_debug
from clck.phonetics import Phone
from clck.phonetics import DummyPhone
from clck.syllabics import Structure


class StructureEvaluator:
    def __init__(self, s: Structure) -> None:
        """
        Creates a new instance of a `StructureEvaluator`.

        Parameters
        ----------
        - `s` - the `Structure` object to be evaluated
        """
        self._structure = s
        self._phonemes = s.phones

        self._ph_ref_dict = self._create_phoneme_reference_dictionary()
        self._struct_comps = self._get_structure_components()
        self._struct_ids = self._get_structure_ids()

        print_debug(self._phonemes)
        print_debug(self._struct_comps)
        print_debug(self._struct_ids)

    @property
    def phonemes(self) -> tuple[Phone, ...]:
        """The tuple of phonemes found in the given structure."""
        return self._phonemes

    @property
    def structure(self) -> Structure:
        """The given structure to this `StructureEvaluator`."""
        return self._structure

    def _create_phoneme_reference_dictionary(self) -> dict[Phone, str]:
        d: dict[Phone, str] = {}

        print_debug(f"Phoneme ref dict {set(self._phonemes)}")

        for i, p in enumerate(set(self._phonemes)):
            if not isinstance(p, DummyPhone):
                d[p] = f"p{i+1}"

        return d

    def _get_structure_ids(self) -> tuple[str, ...]:
        rl: list[str] = []
        for i, c in enumerate(self._struct_comps):
            rl.append(f"{i+1}{c}")
        
        return tuple(rl)

    def _get_structure_components(self) -> tuple[str, ...]:
        rl: list[str] = []
        for p in self._phonemes:
            if isinstance(p, DummyPhone):
                rl.append("d0")
            else:
                rl.append(self._ph_ref_dict[p])
        
        return tuple(rl)