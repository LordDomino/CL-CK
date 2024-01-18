import time
from clck.common.component import ComponentBlueprint
from clck.common.structure import Structure
from clck.formulang.common import Formulang
from clck.formulang.parsing.parse_tree import FormulangStructure
from clck.phonology.phonemes import DummyPhoneme
from clck.phonology.syllabics import SyllabicComponent



"(a)((yu)bc)(d)"  # Example

"a|b|c"
    # SELECTOR. Choose one from "a", "b", or "c"

"a + b"
    # CONCATENATOR. Concatenate "a" and "b"

"a - b"
    # SUBTRACTOR. Remove "b" from "a" (if possible)

"a -> b"
    # MUTATOR. Change "a" into "b"

"? a + b = ab => c"
    # CONDITIONAL. If "a" is equal to "b" then perform "c"

# DEMONSTRATION
# iters: int = 10
# start = time.time()
# result = Formulang.generate("{m | n | p} + {a | e | i | o | u} + {t | g | m}")
# stop = time.time()

# # print(f"{stop - start} elapsed time for {iters} iterations")
# # if result != None:
# #     print(result.output)

# c1 = ComponentBlueprint("C")
# b1 = ComponentBlueprint((c1,c1))
# a1 = ComponentBlueprint((b1,"A"))

# print(a1._structure)
# a1.subset("{A + {B + C} + D}")


"""
{ { A + B } + C }
{ { ... + B }  + C}



"""


s = Structure((DummyPhoneme(),))
print(s)

s = SyllabicComponent(s)
print(s)

s = FormulangStructure(s, 1)
print(s)