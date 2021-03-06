from ply import yacc

from fpbench_lexer import lexer
from fpbench_lexer import tokens
from fpbench_lexer import ops
from fpbench_classes import *

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
    '''expr_number : OPERATION NUMBER
                   | NUMBER'''
    if len(p) == 3:
        if p[1] != '-':
            print("Illegal token before number:", p[1])
        p[0] = number(p[1]+p[2])
    else:
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
    '''let_expr : LPAREN LET LPAREN assigns RPAREN expr RPAREN'''
    p[0] = let(p[4], p[6])
    

def p_while_expr(p):
    '''while_expr : LPAREN WHILE expr LPAREN iter_assigns RPAREN expr RPAREN'''
    p[0] = ("WHILE", p[3], p[5], p[7])

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
        p[0] = p[1]+p[2]
    

def p_assign(p):
    '''assign : LBRACK SYMBOL expr RBRACK
              | LPAREN SYMBOL expr RPAREN'''
    p[0] = ((p[2],p[3]),)
    

def p_iter_assigns(p):
    '''iter_assigns : iter_assign
                    | iter_assigns iter_assign'''
    if len(p) == 2:
        p[0] = (p[1],)
    else:
        p[0] = p[1]+p[2]
    

def p_iter_assign(p):
    '''iter_assign : LBRACK SYMBOL expr expr RBRACK
                   | LPAREN SYMBOL expr expr RPAREN'''
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
            | SYMBOL LPAREN symbols RPAREN
            | SYMBOL LPAREN assigns RPAREN'''
    if p[1][0] != ':' or len(p[1]) == 1:
        print("Invalid property:", p[1])
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
    print("Parsing failed", p)
        
# Build the parser
parser = yacc.yacc()

if __name__ == '__main__':
    s = ('(FPCore (x1 x2 x3)\n' +
         ' :name "hartman3"\n' +
         ' :precision binary64\n' +
         ' :pre (and (<= 0 x1 1) (<= 0 x2 1) (<= 0 x3 1))\n' +
         '   (let ([exp1 e1])\n' +
         '     (- (+ (+ (+ (* 1.0 exp1) (* 1.2 exp21))\n' +
         '              (* 3.0 exp3)) (* 3.2 exp4)))))\n')

    import pprint
    for p in parser.parse(s):
        parsed = p
        print(parsed['props'])
        print(repr(parsed['prog']))
        print(parsed['prog'].infix())
        print('-'*80)
