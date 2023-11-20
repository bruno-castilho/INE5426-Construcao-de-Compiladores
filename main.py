import argparse
from LexicalAnalyzer import LexicalAnalyzer
from SyntacticAnalyzer import SyntacticAnalyzer

parser = argparse.ArgumentParser(description="Source file input")
args = parser.add_argument("--src", dest="src", help="Source file input", type=str)
args = parser.parse_args()

with open(args.src) as file:
    stream = file.read()

la = LexicalAnalyzer(stream)
sa = SyntacticAnalyzer()

tokens_list, symbol_table = la.run()
print(sa.run(tokens_list))





