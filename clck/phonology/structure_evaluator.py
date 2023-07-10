from clck.config import printdebug
from clck.phonology.phonemes import DummyPhoneme, Phoneme
from clck.skeleton.structure import Structure


class StructureEvaluator:
    def __init__(self, s: Structure) -> None:
        self.s = s
        self.phonemes = s.phonemes

        self._ph_ref_dict = self._create_phoneme_reference_dictionary()
        self._struct_comps = self._get_structure_components()
        self._struct_ids = self._get_structure_ids()

        printdebug(self.phonemes)
        printdebug(self._struct_comps)
        printdebug(self._struct_ids)

    def _create_phoneme_reference_dictionary(self) -> dict[Phoneme, str]:
        d: dict[Phoneme, str] = {}

        print(set(self.phonemes))

        for i, p in enumerate(set(self.phonemes)):
            if not isinstance(p, DummyPhoneme):
                d[p] = f"p{i+1}"

        return d

    def _get_structure_ids(self) -> tuple[str]:
        rl: list[str] = []
        for i, c in enumerate(self._struct_comps):
            rl.append(f"{i+1}{c}")
        
        return tuple(rl)

    def _get_structure_components(self) -> tuple[str]:
        rl: list[str] = []
        for p in self.phonemes:
            if isinstance(p, DummyPhoneme):
                rl.append("d0")
            else:
                rl.append(self._ph_ref_dict[p])
        
        return tuple(rl)