from LexicalAnalyzer import LexicalAnalyzer
from SyntacticAnalyzer import SyntacticAnalyzer



filepath = 'data/exemplo1.lcc'

with open('data/exemplo1.lcc') as file:
    stream = file.read()

la = LexicalAnalyzer(stream)
sa = SyntacticAnalyzer()

tokens_list, symbol_table = la.run()
print(sa.run(tokens_list))





