import json
from clck.lexer.proto_parser import ProtoParser

my_parser = ProtoParser("5689")

ast = my_parser.parse()

print(json.dumps(ast, indent=4))