"""
Bruno da Silva Castilho;
Leonardo Seishi Yamazaki;
Rafael Francisco Réus;
Rafael Begnini de Castilhos.
"""
import copy

class Grammar():
    """
        Uma classe para representar uma gramática.

        ...

        Atributos
        ---------
        start: str
            Símbolo inicial da gramática.

        productions: dict
            Lista de produções da gramática.

        first_dict: dict
            Conjunto dos firsts.

        follow_dict: dict
            Conjunto dos follows.

        non_terminal: set
            Conjunto de não-terminais.

        terminal: set
            Conjunto de terminais.


        Métodos
        -------
        read(filename: str) -> None:
            Lê a gramática de um arquivo.

        calculate_first() -> None:
            Calcula os firsts.

        calculate_follow() -> None:
            Calcula os follows.

    """

    def __init__(self, filename):
        self.start = ''
        self.productions = dict()
        self.first_dict = dict()
        self.follow_dict = dict()
        self.non_terminal = set()
        self.terminal = set()

        self.read(filename)
        self.calculate_first()
        self.calculate_follow()


        ## Apresenta FIRST e FOLLOW
        #print('###FIRST###')
        #for production_head, productions in self.first_dict.items():
        #    print(production_head,productions)

        #print('')
        #print('###FOLLOW###')
        #for production_head, productions in self.follow_dict.items():
        #    print(production_head,productions)

    def read(self, filename):
        with open(filename, 'r') as arquivo:
            begin = True

            for line in arquivo:
                chars_list = line.strip().split()
                
                left = chars_list[0]
                right = chars_list[2:]
                self.non_terminal = self.non_terminal.union({left})

                if begin:
                    self.start = left
                    begin = False

                productions_set = set()

                production = []
 
                for chars in right:
                    if chars != '|':
                        production.append(chars)
                        if not chars[0].isupper():
                            if chars[0] != '&':
                                self.terminal = self.terminal.union({chars})
                    else:
                        productions_set.add(tuple(production))
                        production = []

                productions_set.add(tuple(production))
                self.productions[left] = productions_set

    def calculate_first(self):
        for production_head, productions in self.productions.items():
            self.first_dict[production_head] = set()
        
        while True:
            pre_dict = copy.deepcopy(self.first_dict)
            for production_head, productions in self.productions.items():
                for production in productions: 
                    lenght = len(production)
                    for i in range(lenght):
                        if production[i][0].isupper():
                            self.first_dict[production_head] = self.first_dict[production_head].union(self.first_dict[production[i]])
                            if '&' in self.first_dict[production[i]]:
                                if i < lenght - 1: 
                                    self.first_dict[production_head] -= {'&'}
                            else:
                                break

                        else:
                            self.first_dict[production_head] = self.first_dict[production_head].union({production[i]})
                            break



            if self.first_dict == pre_dict:
                break
                    
    def calculate_follow(self):
        for production_head in self.productions:
            self.follow_dict[production_head] = set()

        self.follow_dict[self.start] = {'$'}

        for production_head, productions in self.productions.items():
            for production in productions:
                length = len(production)
                for i in range(length):
                    token = production[i]
                    if token[0].isupper():
                        for j in range(i+1,length):
                            if not production[j][0].isupper():
                                self.follow_dict[token] = self.follow_dict[token].union({production[j]})
                                break
                            else:
                                self.follow_dict[token] = self.follow_dict[token].union(self.first_dict[production[j]]) - {'&'}
                                if not '&' in self.first_dict[production[j]]:
                                    break


        #Enquanto houvere mudançã em follow_dict
        while True:
            pre_dict = copy.deepcopy(self.follow_dict)
            for production_head, productions in self.productions.items():
                for production in productions:
                    length = len(production)
                    for i in range(length-1, -1, -1):
                        token = production[i]
                        if token[0].isupper():
                            self.follow_dict[token] = self.follow_dict[token].union(self.follow_dict[production_head])
                            if not '&' in self.first_dict[token]:
                                    break
                        else:
                            break
            if self.follow_dict == pre_dict:
                break
   
    #GET
    def get_first(self):
        return self.first_dict
    
    def get_follow(self):
        return self.follow_dict
    
    def get_non_terminal(self):
        return self.non_terminal
    
    def get_terminal(self):
        return self.terminal
    
    def get_productions(self):
        return self.productions
    
    def get_start(self):
        return self.start