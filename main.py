"""
Bruno da Silva Castilho;
Leonardo Seishi Yamazaki;
Rafael Francisco Réus;
Rafael Begnini de Castilhos.
"""

import argparse
from Parser import Parser
from SyntacticAnalyzer import SyntacticAnalyzer
import ply.yacc as yacc

parser = argparse.ArgumentParser(description="Source file input")
args = parser.add_argument("--src", dest="src", help="Source file input", type=str)
args = parser.add_argument("--semantic", dest="semantic", help="Run semantic analyzer?", type=bool)
args = parser.parse_args()

with open(args.src) as file:
    stream = file.read()

parser = Parser(stream)
sa = SyntacticAnalyzer()

tokens_list, symbol_table = parser.lexical()

syntax_analyzer = sa.run(tokens_list)
print(syntax_analyzer)
print(args.semantic)
if(syntax_analyzer and args.semantic):
    sm = parser.semantic(stream)
    print(sm)

