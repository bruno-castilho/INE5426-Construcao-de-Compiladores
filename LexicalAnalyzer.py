import ply.lex as lex

class LexicalAnalyzer():
       
        reserved = {
                'def' : 'def',
                'int' : 'int',
                'float' : 'float',
                'string' : 'string',
                'break' : 'break',
                'print' : 'print',
                'read': 'read',
                'return' : 'return',
                'if': 'if',
                'else': 'else',
                'for': 'for',
                'new' : 'new',
                'null' : 'null',
            }

        tokens = [
                'ident', 'int_constant', 'float_constant', 'string_constant',
                'rparen', 'lparen', 'rbracket', 'lbracket', 'rbrace', 'lbrace', 'comma', 'semicolumn',
                'equal', 'diff', 'less', 'greater', 'lessequal', 'greaterequal',
                'plus', 'minus', 'mod', 'times', 'divide', 'assign'
        ] + list(reserved.values())

        t_ignore 		= ' \t'

        t_rparen		= r'\)'
        t_lparen		= r'\('

        t_rbracket		= r'\]'
        t_lbracket 		= r'\['

        t_rbrace		= r'}'
        t_lbrace		= r'{'

        t_comma			= r','
        t_semicolumn	= r';'

        t_equal		    = r'=='
        t_diff			= r'!='
        t_lessequal	    = r'<='
        t_greaterequal 	= r'>='
        t_less			= r'<'
        t_greater	    = r'>'

        t_plus   		= r'\+'
        t_minus			= r'-'
        t_mod			= r'%'
        t_times			= r'\*'
        t_divide		= r'/'
        t_assign		= r'='


        t_string_constant = r'\"([^\\\n]|(\\.))*?\"'


        def t_ident(self, t):
            r'[a-zA-Z_][a-zA-Z_0-9]*'
            t.type = self.reserved.get(t.value, 'ident')
            return t

        def t_float_constant(self, t):
            r'(\d+).(\d+)'
            t.value = float(t.value)
            return t

        def t_int_constant(self, t):
            r'\d+'
            t.value = int(t.value)
            return t

        def t_newline(self, t):
            r'\n+'
            t.lexer.lineno += len(t.value)

        def t_comment(self):
            r'\//.*'
            pass

        def t_error(self, t):
            raise Exception("Illegal character '%s'" % t.value[0])

        def __init__(self, stream):
                self.lexer = lex.lex(module=self)
                self.lexer.input(stream)

        def run(self):
            tokens_list = []
            symbol_table = {}

            for tok in self.lexer:
                tokens_list.append(tok.type)

                if tok.type == 'ident': 
                    params = {
                             'line': tok.lineno,
                             'position': tok.lexpos
                        }
                    if not tok.value in symbol_table.keys():
                        symbol_table[tok.value] = [params]
                    else:
                         symbol_table[tok.value].append(params)
            
            return (tokens_list, symbol_table)

