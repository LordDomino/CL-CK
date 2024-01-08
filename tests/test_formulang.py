import time
from clck.formulang.common import generate_multiple

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
start = time.time()
generate_multiple("{m | n | p} + {a | e | i | o | u} + {t | g | m}", iters)
stop = time.time()

print(f"{stop - start} elapsed time for {iters} iterations")