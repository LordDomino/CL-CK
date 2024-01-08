from clck.formulang import generate_multiple

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
for r in generate_multiple("{m | n | p} + {a | e | i | o | u} + {t | g | m}", 10):
    if r != None:
        print(r, r.output)