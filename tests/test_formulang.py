from clck.common.component import ComponentBlueprint
from clck.phonology.phonemes import ConsonantPhoneme, DummyPhoneme, Phoneme



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
iters: int = 10
# result = Formulang.generate("(a) + ((yu) + bc) + (d)")

# if result != None:
#     print(result.output)
#     print(result.blueprint)

a = ComponentBlueprint((DummyPhoneme(), Phoneme))
b = ComponentBlueprint((Phoneme, ConsonantPhoneme))

if b == a:
    print("Equal blueprints")
else:
    print("Unequal blueprints")

if isinstance(DummyPhoneme(), ConsonantPhoneme):
    print("Isintance")