from clck.lexer.parser import Parser
from clck.lexer.tokenizer import Tokenizer


formula = "(a)((yu)bc)(d)"  # Example

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

my_tokenizer = Tokenizer(formula)
my_tokenizer.analyze()

tokens = my_tokenizer.get_tokens()

my_parser = Parser(tokens)
my_parser.parse()