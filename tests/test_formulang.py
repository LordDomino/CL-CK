from clck.formulang.parsing.parser import Parser
from clck.formulang.lexer.tokenizer import Tokenizer

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
my_tokenizer = Tokenizer("ɳ")
my_tokenizer.analyze()

ast = Parser(my_tokenizer.get_tokens()).parse()
result = ast.eval()