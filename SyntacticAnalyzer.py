import pandas as pd
from Grammar import Grammar

class SyntacticAnalyzer():
        def __init__(self):
            self.grammar = Grammar('ConvCC-2023-1.txt')
            self.productions_list = []
            self.table = {}

            self.generate_table()

            pd.set_option('colheader_justify', 'center')
            pd.set_option('display.max_rows', None)  # Mostra todas as linhas
            pd.set_option('display.max_columns', None) 
            data = pd.DataFrame(self.table)
            data = data.transpose()

            print(data)


        def check(self, first, follow):
            for production in self.productions_list:
                if production[1][0] == '&' and first[production[0]] & follow[production[0]] != set():
                    print(production)
                    raise Exception("interseção de First e Follow para um não terminal que deriva ε é diferente de vazio")
                    
        def generate_table(self):
            self.table = {}
            self.productions_list = []
            productions = self.grammar.get_productions()
            first = self.grammar.get_first()
            follow = self.grammar.get_follow()
            terminal = self.grammar.get_terminal()
            
            for production_head, prs in productions.items():
                for production in prs:
                    self.productions_list.append((production_head, production))


            self.check(first, follow)
            for n in productions.keys():
                self.table[n] = {"$":'-'}
                for t in terminal:
                    self.table[n][t] = '-'
            

            for i in range(len(self.productions_list)):

                if self.productions_list[i][1][0] == '&':
                    for b in follow[self.productions_list[i][0]]:
                        self.table[self.productions_list[i][0]][b] = self.productions_list[i][1]

                else:
                    for token in self.productions_list[i][1]:
                        if token[0].isupper():
                            for t in first[token]:
                                if t != '&':
                                    self.table[self.productions_list[i][0]][t] = self.productions_list[i][1]
                            
                            if not '&' in first[token]:
                                break

                            elif token == self.productions_list[i][1][-1]:
                                for b in follow[self.productions_list[i][0]]:
                                    self.table[self.productions_list[i][0]][b] = self.productions_list[i][1]
                        else:
                            self.table[self.productions_list[i][0]][token] = self.productions_list[i][1]
                            break

        def run(self, tokens):
            stack = ['$', self.grammar.get_start()]
            queue = []
            for token in tokens: 
                queue.append(token)
            queue.append('$')

            current_token = queue.pop(0)
            while True:
                print([current_token] + queue)
                print(stack)
                print()

                if stack[-1] == '$' and current_token == '$':
                    break
                elif stack[-1] == current_token:

                    current_token = queue.pop(0)
                    stack.pop()
                elif stack[-1][0].isupper():
                    
                    production = self.table[stack[-1]][current_token]
                    if production[0] != '-':
                        stack.pop()
                        if production[0] != '&':
                            for i in range(len(production)-1,-1,-1):
                                stack.append(production[i])
                    else:
                        break
                else:
                    break

            if stack[-1] == '$' and current_token == '$':
                return "Análise Sintática bem sucedida"
            else:
                return "Análise Sintática com problemas"
