from clck.lexer.tokenizer import Tokenizer


formula = "a|b|c"  # Choose one from "/a/", "/b/", or "/c/"

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
print(my_tokenizer.get_tokens())