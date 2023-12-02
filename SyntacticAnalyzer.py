"""
Bruno da Silva Castilho;
Leonardo Seishi Yamazaki;
Rafael Francisco Réus;
Rafael Begnini de Castilhos.
"""

from Grammar import Grammar


class SyntacticAnalyzer():
    """
        Uma classe para representar um analisador sintático LL(1).

        ...

        Atributos
        ---------
        grammar: Grammar()
            Gramática utilizada.

        table: dict
            Tabela do analisador.

        Métodos
        -------
        check(productions_list: list, first: dict, follow: dict) -> None:
            Checa se a interseção de First e Follow para todos os não terminais que derivam ε é diferente de vazio.

        generate_table() -> None:
            Gera a tabela do analisador.

        run(tokens: list) -> str:
            Executa o analisador.
    """

    def __init__(self):
        self.grammar = Grammar('ConvCC-2023-1.txt')
        self.table = {}

        self.generate_table()

    def check(self,productions_list, first, follow):
        for production in productions_list:
            if production[1][0] == '&' and first[production[0]] & follow[production[0]] != set():
                print(production)
                raise Exception("interseção de First e Follow para um não terminal que deriva ε é diferente de vazio")
                
    def generate_table(self):
        self.table = {}
        productions_list = []
        productions = self.grammar.get_productions()
        first = self.grammar.get_first()
        follow = self.grammar.get_follow()
        terminal = self.grammar.get_terminal()
        
        for production_head, prs in productions.items():
            for production in prs:
                productions_list.append((production_head, production))


        self.check(productions_list, first, follow)
        
        for n in productions.keys():
            self.table[n] = {"$":'-'}
            for t in terminal:
                self.table[n][t] = '-'
        

        for i in range(len(productions_list)):

            if productions_list[i][1][0] == '&':
                for b in follow[productions_list[i][0]]:
                    self.table[productions_list[i][0]][b] = productions_list[i][1]

            else:
                for token in productions_list[i][1]:
                    if token[0].isupper():
                        for t in first[token]:
                            if t != '&':
                                self.table[productions_list[i][0]][t] = productions_list[i][1]
                        
                        if not '&' in first[token]:
                            break

                        elif token == productions_list[i][1][-1]:
                            for b in follow[productions_list[i][0]]:
                                self.table[productions_list[i][0]][b] = productions_list[i][1]
                    else:
                        self.table[productions_list[i][0]][token] = productions_list[i][1]
                        break

    def run(self, tokens):
        stack = ['$', self.grammar.get_start()]
        queue = []
        for token in tokens: 
            queue.append(token)
        queue.append('$')

        
        current_token = queue.pop(0)
        last_token = current_token
        while True:
            t = '$' if current_token == '$' else current_token.type

            if stack[-1] == '$' and t == '$':
                return "Código sem erro sintático"
            elif stack[-1] == t:
                last_token = current_token
                current_token = queue.pop(0)
                stack.pop()
            elif stack[-1][0].isupper():
                
                production = self.table[stack[-1]][t]
                if production[0] != '-':
                    stack.pop()
                    if production[0] != '&':
                        for i in range(len(production)-1,-1,-1):
                            stack.append(production[i])
                else:
                    break
            else:
                break


        return f"Código com erro sintático LEXEMA:{last_token.value} , LINHA:{last_token.lineno} , POSIÇÃO:{last_token.lexpos} "
