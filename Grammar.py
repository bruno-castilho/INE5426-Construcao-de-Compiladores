class Grammar():

    def __init__(self, filename):
        self.start = ''
        self.grammar = dict()
        self.first_dict = dict()
        self.follow_dict = dict()

        self.read(filename)
        self.calculate_first()
        self.calculate_follow()

        #print(self.start)
        print(self.grammar)
        #print(self.first_dict)
        #print(self.follow_dict)


    def read(self, filename):
        with open(filename, 'r') as arquivo:
            begin = True

            for line in arquivo:
                chars_list = line.strip().split()
                
                left = chars_list[0]
                right = chars_list[2:]

                if begin:
                    self.start = left
                    begin = False

                productions_set = set()

                production = []
 
                for chars in right:
                    if chars != '|':
                        production.append(chars)
                    else:
                        productions_set.add(tuple(production))
                        production = []

                productions_set.add(tuple(production))
                self.grammar[left] = productions_set
            
    
    def get_first(self):
        first = set()
                    

        return first
    
    
    
    def calculate_first(self):
        for production_head in self.grammar:
            self.first_dict[production_head] = self.get_first()
    
    def calculate_follow(self):
        return


        
        
        
    
