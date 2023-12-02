"""
Bruno da Silva Castilho;
Leonardo Seishi Yamazaki;
Rafael Francisco Réus;
Rafael Begnini de Castilhos.
"""

import argparse
from Parser import Parser
from SyntacticAnalyzer import SyntacticAnalyzer
import pandas as pd


def print_symbol_table(symbol_table):
    symbol_table_data = []
    # Imprimir linhas da tabela
    for tok in symbol_table:
        symbol_table_data.append({'TOKEN': tok.value, 'LINHA': tok.lineno, 'POSIÇÃO': tok.lexpos})

    pd.set_option('display.max_rows', None)  # Mostra todas as linhas
    df = pd.DataFrame(symbol_table_data)
    
    print()
    print('TABELA DE SÍMBOLOS:')
    print(df)  
    print() 

parser = argparse.ArgumentParser(description="Source file input")
args = parser.add_argument("--src", dest="src", help="Source file input", type=str)
args = parser.add_argument("--semantic", dest="semantic", help="Run semantic analyzer?", type=bool)
args = parser.parse_args()

## Lê código-fonte
with open(args.src) as file:
    string = file.read()

parser = Parser(string)

## Análise Léxica
tokens_list, symbol_table = parser.lexical()
print('Código sem erro lexico')
print_symbol_table(symbol_table)

## Análise Sintática
sa = SyntacticAnalyzer()
result = sa.run(tokens_list)
print(result)

## Análise Semântica
if(result and args.semantic):
    sm = parser.semantic(string)
    print(sm)

