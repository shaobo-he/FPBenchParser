from ply import yacc

from fpbench_lexer import lexer
from fpbench_lexer import tokens
from fpbench_classes import *

# Artificially requires FPCore as a keyword.
def p_programs(p):
    '''programs : program
                | programs program'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[1].append(p[2])
        p[0] = p[1]
        
def p_program(p):
    '''program : LPAREN SYMBOL LPAREN symbols RPAREN props expr RPAREN
               | LPAREN SYMBOL LPAREN symbols RPAREN expr RPAREN'''
    if p[2] != "FPCore":
        print("Not a valid program: no FPCore")
        p[0] = None
    if len(p) == 9:
        args = p[4]
        props = p[6]
        prog = p[7]
    else:
        args = p[4]
        props = None
        prog = p[6]

    p[0] = {'args'  : args,
            'props' : props,
            'prog'  : prog}


def p_expr(p):
    '''expr : expr_number
            | expr_constant
            | expr_symbol
            | LPAREN op RPAREN
            | if_expr
            | let_expr
            | while_expr'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[2]

def p_expr_number(p):
    '''expr_number : NUMBER'''
    p[0] = number(p[1])

def p_expr_constant(p):
    '''expr_constant : CONSTANT'''
    p[0] = constant(p[1])

def p_expr_symbol(p):
    '''expr_symbol : SYMBOL'''
    p[0] = var(p[1])

    
def p_op(p):
    '''op : OPERATION exprs'''
    p[0] = op(p[1], p[2])

def p_if_expr(p):
    '''if_expr : LPAREN IF expr expr expr RPAREN'''
    p[0] = ("IF", p[3], p[4], p[5])
    

def p_let_expr(p):
    '''let_expr : LPAREN LET RPAREN assigns LPAREN expr RPAREN'''
    p[0] = ("LET", p[4], p[6])
    

def p_while_expr(p):
    '''while_expr : LPAREN WHILE LPAREN iter_assigns RPAREN expr RPAREN'''
    p[0] = ("WHILE", p[4], p[6])

def p_exprs(p):
    '''exprs : expr
             | exprs expr'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[1].append(p[2])
        p[0] = p[1]

def p_assigns(p):
    '''assigns : assign
               | assigns assign'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[1]+p[2:]
    

def p_assign(p):
    '''assign : LBRACK expr expr RBRACK'''
    p[0] = ((p[2],p[3]),)
    

def p_iter_assigns(p):
    '''iter_assigns : iter_assign
                    | iter_assigns iter_assign'''
    if len(p) == 2:
        p[0] = (p[1],)
    else:
        p[0] = p[1]+p[2]
    

def p_iter_assign(p):
    '''iter_assign : LBRACK SYMBOL expr expr RBRACK'''
    p[0] = ((p[2],p[3],p[4]),)
    

def p_props(p):
    '''props : prop
             | props prop'''
    if len(p) == 2:
        p[0] = (p[1],)
    else:
        p[0] = p[1]+(p[2],)
    
    
def p_prop(p):
    '''prop : SYMBOL expr
            | SYMBOL STRING
            | SYMBOL LPAREN symbols RPAREN'''
    if p[1][0] != ':' or len(p[1]) == 1:
        print("Invalid proprty:", p[1])
        assert(0)
    p[1] = p[1][1:]
    if len(p) == 3:
        p[0] = (p[1], p[2])
    else:
        p[0] = (p[1], p[3])
    

def p_symbols(p):
    '''symbols : SYMBOL
               | symbols SYMBOL'''
    if len(p) == 2:
        p[0] = (p[1],)
    else:
        p[0] = p[1] + (p[2],)
    
def p_error(p):
    print("Parsing failed")
        
# Build the parser
parser = yacc.yacc()

if __name__ == '__main__':
    s = '''(FPCore (x y)
 :name "NMSE example 3.1"
 :cite (hamming-1987)
 :pre (>= x 0)
 (fma x x (- (sqrt (+ x (- 1))) (sqrt x))))'''
    import pprint
    parsed = parser.parse(s)
    print(repr(parsed['prog']))
    print(parsed['prog'].infix())
