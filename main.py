from LexicoAnalyzer import LexicoAnalyzer

filepath = 'data/exemplo1.lcc'

with open(filepath) as file:
    stream = file.read()

la = LexicoAnalyzer(stream)
tokens_list, symbol_table = la.run()

print("#### TOKENS ####")
for token in tokens_list:
    print(token)

print("#### TABELA DE SIMBOLOS ####")
for symbol in symbol_table.keys():
    print(f'Simbolo:{symbol}, OCORRENCIAS: {symbol_table[symbol]}')






    











