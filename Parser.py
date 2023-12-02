"""
Bruno da Silva Castilho;
Leonardo Seishi Yamazaki;
Rafael Francisco Réus;
Rafael Begnini de Castilhos.
"""

import ply.lex as lex
import ply.yacc as yacc
from structures import ScopeStack, EntryTable, Scope, TreeNode
from typing import List, Tuple

expressions: List[Tuple[TreeNode, int]] = []
scopes = ScopeStack()

class Parser():
    """
        Classe responsável pela análise léxica (funcional) e análise semântica, 
        utilizando um analisador sintático LALR(1) (com problemas nas regras semânticas).

        Documentação da biblioteca utilizada:
        https://github.com/dabeaz/ply

    """

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

    def t_COMMENT(self, t):
        r'\//.*'
        pass

    def t_error(self, t):
        print("Código com erro lexico '%s'" % t.value[0])


    def __init__(self, string):
        self.lexer = lex.lex(debug=0, module=self)
        self.lexer.input(string)


    def lexical(self):
        tokens_list = []
        symbol_table = []

        for tok in self.lexer:
            tokens_list.append(tok)

            if tok.type == 'ident': 
                symbol_table.append(tok)

        
        return (tokens_list, symbol_table)


    def p_error(self, t):
        pass

    # Produção inicial
    def p_program(self, p):
        """program : program1
                    | epsilon
        """
        p[0] = p[1]

    def p_program1(self, p):
        """program1 : new_scope statement
                    | new_scope funclist
                    | epsilon
        """
        p[0] = {"scopes": scopes.pop().as_dict(), "expressions": numexpression_as_dict()}

    def p_funclist(self, p):
        """funclist : funcdef funclist1
        """
        pass

    def p_funclist1(self, p):
        """funclist1 : funclist
                    | epsilon
        """
        pass

    def p_funcdef(self, p):
        """funcdef : def ident new_scope lparen paramlist rparen lbrace statelist rbrace
        """
        scopes.pop()
        current_scope = scopes.seek()

        # Get function info to use in entry table
        func_IDENT = p[2]
        func_line_number = p.lineno(2)

        new_func = EntryTable(IDENT=func_IDENT, datatype="function", values=[], lineno=func_line_number)

        # Add function to current scope entry table
        if current_scope is not None:
            current_scope.add_entry(new_func)

    def p_paramlist(self, p):
        """paramlist : paramlist1
                    | epsilon
        """
        pass

    def p_paramlist1(self, p):
        """paramlist1 : type ident paramlist2
        """
        if len(p) > 2:
            current_scope = scopes.seek()

            paramlist_type = p[1]
            paramlist_IDENT = p[2]
            paramlist_lineno = p.lineno(2)

            paramlist = EntryTable(
                IDENT=paramlist_IDENT,
                datatype=paramlist_type,
                values=[],
                lineno=paramlist_lineno,
            )
            if current_scope is not None:
                current_scope.add_entry(paramlist)

    def p_paramlist2(self, p):
        """paramlist2 : comma paramlist
                    | epsilon
        """
        pass

    def p_statement(self, p):
        """statement : vardecl semicolumn
                    | atribstat semicolumn
                    | printstat semicolumn
                    | readstat semicolumn
                    | returnstat semicolumn
                    | ifstat
                    | forstat
                    | lbrace statelist rbrace
                    | break semicolumn
                    | semicolumn
        """
        pass

    # def p_break(self, p):
    #     """
    #     break :
    #     """
    #     current_scope = scopes.seek()

    #     while True:
    #         if current_scope is None or current_scope.loop:
    #             break
    #         else:
    #             current_scope = current_scope.outer_scope

    #             # If there is no outer scope then it's an error
    #             if current_scope is None:
    #                 # Get error line number and raise an error
    #                 error_lineno = p.lineno(2)
    #                 raise InvalidBreakError(
    #                     f"Operador 'break' inválido na linha {error_lineno}"
    #                 )

    def p_statelist(self, p):
        """statelist : statement statelist1
        """
        pass

    def p_statelist1(self, p):
        """statelist1 : new_scope statelist
                    | epsilon
        """
        pass

    def p_vardecl(self, p):
        """vardecl : type ident vardecl1
        """
        variable_type = p[1]
        variable_IDENT = p[2]
        variable_values = p[3]
        variable_lineno = p.lineno(2)

        # save variable as entry table
        variable = EntryTable(
            IDENT=variable_IDENT,
            datatype=variable_type,
            values=variable_values,
            lineno=variable_lineno,
        )
        # get current scope
        current_scope = scopes.seek()
        # add variable to current scope
        if current_scope is not None:
            current_scope.add_entry(variable)
        pass

    def p_vardecl1(self, p):
        """vardecl1 : lbracket int_constant rbracket vardecl1
                    | epsilon
        """
        if len(p) > 2:
            p[0] = [p[2], *p[4]]
        else:
            p[0] = []
        pass

    def p_atribstat(self, p):
        """atribstat : ident lvalue assign atribstat1
                    | epsilon
        """
        pass

    def p_atribstat1(self, p):
        """atribstat1 : atribstat2
                    | allocexpression
                    | ident atribstat4
                    | factor term numexpression expression1
        """
        pass

    def p_atribstat2(self, p):
        """atribstat2 : plus atribstat3
                    | minus atribstat3
        """
        pass

    def p_atribstat3(self, p):
        """atribstat3 : factor term numexpression expression1
                    | ident lvalue term numexpression expression1
        """
        pass

    def p_atribstat4(self, p):
        """atribstat4 : funccall
                    | lvalue term numexpression expression1
        """
        pass

    def p_funccall(self, p):
        """funccall : lparen paramlistcall rparen
        """
        pass

    def p_paramlistcall(self, p):
        """paramlistcall : paramlistcall1
                    | epsilon
        """
        pass

    def p_paramlistcall1(self, p):
        """paramlistcall1 : ident paramlistcall2
        """
        pass

    def p_paramlistcall2(self, p):
        """paramlistcall2 : comma paramlistcall
                    | epsilon
        """
        pass

    def p_printstat(self, p):
        """printstat : print unaryexpr printstat1
        """
        pass

    def p_printstat1(self, p):
        """printstat1 : factor term numexpression expression1
                    | ident lvalue term numexpression expression1
        """
        pass

    def p_readstat(self, p):
        """readstat : read ident lvalue
        """
        pass

    def p_returnstat(self, p):
        """returnstat : return
        """
        pass

    def p_ifstat(self, p):
        """ifstat : if lparen ifstat1
        """
        pass

    def p_ifstat1(self, p):
        """ifstat1 : unaryexpr ifstat2
        """
        pass

    def p_ifstat2(self, p):
        """ifstat2 : factor term numexpression expression1 rparen lbrace statelist rbrace else
                    | ident lvalue term numexpression expression1 rparen lbrace statelist rbrace else
        """
        pass

    # def p_else(self, p):
    #     """else : else
    #                 | epsilon
    #     """
    #     pass

    def p_forstat(self, p):
        """forstat : for lparen atribstat semicolumn forstat1
        """
        pass

    def p_forstat1(self, p):
        """forstat1 : unaryexpr forstat2
        """
        pass

    def p_forstat2(self, p):
        """forstat2 : factor term numexpression expression1 semicolumn atribstat rparen statement
                    | ident lvalue term numexpression expression1 semicolumn atribstat rparen statement
        """
        pass

    def p_allocexpression(self, p):
        """allocexpression : new type allocexpression1
        """
        pass

    def p_allocexpression1(self, p):
        """allocexpression1 : lbracket unaryexpr allocexpression2
        """
        pass

    def p_allocexpression2(self, p):
        """allocexpression2 : factor term numexpression rbracket allocexpression3
                    | ident lvalue term numexpression rbracket allocexpression3
        """
        pass

    def p_allocexpression3(self, p):
        """allocexpression3 : lbracket unaryexpr allocexpression2
                    | epsilon
        """
        pass

    def p_expression1(self, p):
        """expression1 : expression2
                    | epsilon
        """
        pass

    def p_expression2(self, p):
        """expression2 : expression3 unaryexpr expression4
        """
        pass

    def p_expression3(self, p):
        """expression3 : less
                    | greater
                    | lessequal
                    | greaterequal
                    | equal
                    | diff
        """
        pass

    def p_expression4(self, p):
        """expression4 : factor term numexpression
                    | ident lvalue term numexpression
        """
        pass

    def p_numexpression(self, p):
        """numexpression : numexpression2 unaryexpr numexpression1
                    | epsilon
        """
        pass

    def p_numexpression1(self, p):
        """numexpression1 : factor term numexpression
                    | ident lvalue term numexpression
        """
        pass

    def p_numexpression2(self, p):
        """numexpression2 : plus
                    | minus
        """
        pass

    def p_term(self, p):
        """term : term2 unaryexpr term1
                    | epsilon
        """
        pass

    def p_term1(self, p):
        """term1 : factor term
                    | ident lvalue term
        """
        pass

    def p_term2(self, p):
        """term2 : times
                    | divide
                    | mod
        """
        pass

    def p_unaryexpr(self, p):
        """unaryexpr : plus
                    | minus
                    | epsilon
        """
        pass

    def p_factor(self, p):
        """factor : int_constant
                    | float_constant
                    | string_constant
                    | null
                    | lparen numexpression rparen
        """

    def p_type(self, p):
        """type : int
                    | float
                    | string
        """
        p[0] = p[1]

    def p_lvalue(self, p):
        """lvalue : lbracket lvalue1
                    | epsilon
        """
        pass

    def p_lvalue1(self, p):
        """lvalue1 : factor term numexpression rbracket lvalue
                    | ident lvalue term numexpression rbracket lvalue
        """
        pass

    # Produção vazia
    def p_epsilon(self, p):
        "epsilon :"
        pass

    def create_scope(self, loop):
        """
        Scope management list
        """
        top = scopes.seek()
        new = Scope(outer_scope=top, loop=loop)
        if top:
            top.add_inner_scope(new)
        scopes.push(new)

    def p_new_scope(self, p):
        """
        new_scope :
        """
        self.create_scope(False)


    def p_new_scope_loop(self, p):
        """
        new_loop_scope :
        """
        self.create_scope(True)

    def get_variable_type(IDENT: str, lineno: int):
        """
        Get variable type
        Used during TreeNode construction in LVALUEs
        """
        scope = scopes.seek()
        while True:
            for entry in scope.entry_table:
                if entry.IDENT == IDENT:
                    return entry.datatype

            scope = scope.outer_scope
            if scope is None:
                break
        raise VariableNotDeclared(f"Variável não declarada '{IDENT}' na linha: {lineno})")


    def numexpression_as_dict():
        exp_dict = []

        for exp, lineno in expressions:
            if exp.left == None and exp.right == None:
                continue

            exp_dict.append({"Node Id:": str(exp.id), "lineno": lineno, "tree": exp.as_dict()})

        return exp_dict

    def semantic(self, src):
        parser = yacc.yacc(start="program", module=self, check_recursion=True, debug=True)
        parser.parse(src, debug=True)