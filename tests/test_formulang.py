import time
from clck.formulang.common import Formulang


"""
{
	"folders": [
		{
			"path": "CL-CK"
		}
	],
	"settings": {
		"cSpell.words": [
			"clck",
			"formulang"
		],
		"python.analysis.diagnosticSeverityOverrides": {
			"reportUnusedImport": "warning",
			"reportUninitializedInstanceVariable": "warning",
			"reportIncompatibleMethodOverride": "warning",
			"reportIncompatibleVariableOverride": "warning",
			"reportImportCycles": "warning",
			"reportAssertAlwaysTrue": "warning",
			"reportInconsistentConstructor": "warning",
			"reportUnboundVariable": "warning",
			"reportUnusedVariable": "warning",
			"reportInvalidStringEscapeSequence": "warning",
			"reportUnnecessaryCast": "warning",
			"reportUnnecessaryContains": "warning",
			"reportUnusedClass": "warning",
			"reportWildcardImportFromLibrary": "warning",
		}
	}
}
"""


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
result = Formulang.generate("{m | n | p} + {a | e | i | o | u} + {t | g | m}")
stop = time.time()

print(f"{stop - start} elapsed time for {iters} iterations")
print(result.output)