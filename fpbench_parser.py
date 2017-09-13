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
        p[0] = p[1]+p[2]
    

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
    s = ''';; -*- mode: scheme -*-

;; These two appear in the text of the FPTaylor paper

(FPCore (t)
  :name "intro-example"
  :cite (solovyev-et-al-2015)
  :pre (<= 0 t 999)
  (/ t (+ t 1)))

(FPCore (x y)
  :name "sec4-example"
  :cite (solovyev-et-al-2015)
  :precision binary64
  :pre (and (<= 1.001 x 2) (<= 1.001 y 2))
  (let ([t (* x y)])
    (/ (- t 1) (- (* t t) 1))))

;; From the FPTaylor project <https://github.com/soarlab/FPTaylor>,
;; all `*.txt` files in the directory `benchmarks/tests/`.

(FPCore (x0 x1 x2)
  :name "test01_sum3"
  :precision binary32
  :pre (and (< 1 x0 2) (< 1 x1 2) (< 1 x2 2))
  (let ([p0 (- (+ x0 x1) x2)]
        [p1 (- (+ x1 x2) x0)]
        [p2 (- (+ x2 x0) x1)])
    (+ (+ p0 p1) p2)))

(FPCore (x0 x1 x2 x3 x4 x5 x6 x7 x8)
  :name "test02_sum8"
  :precision binary64
  :pre (and (< 1 x0 2) (< 1 x1 2) (< 1 x2 2)
            (< 1 x3 2) (< 1 x4 2) (< 1 x5 2)
            (< 1 x6 2) (< 1 x7 2))
  (+ (+ (+ (+ (+ (+ (+ x0 x1) x2) x3) x4) x5) x6) x7))

(FPCore (x y)
  :name "test03_nonlin2"
  :precision binary64
  :pre (and (< 0 x 1) (< -1 y -0.1))
  (/ (+ x y) (- x y)))

(FPCore (m0 m1 m2 w0 w1 w2 a0 a1 a2)
  :name "test04_dqmom9"
  :precision binary64
  :pre (and (< -1 m0 1) (< -1 m1 1) (< -1 m2 1)
            (< 0.00001 w0 1) (< 0.00001 w1 1) (< 0.00001 w2 1)
            (< 0.00001 a0 1) (< 0.00001 a1 1) (< 0.00001 a2 1))
  (let ([v2 (* (* w2 (- 0 m2)) (* -3 (* (* 1 (/ a2 w2)) (/ a2 w2))))]
        [v1 (* (* w1 (- 0 m1)) (* -3 (* (* 1 (/ a1 w1)) (/ a1 w1))))]
        [v0 (* (* w0 (- 0 m0)) (* -3 (* (* 1 (/ a0 w0)) (/ a0 w0))))])
    (+ 0.0 (+ (* v0 1) (+ (* v1 1) (+ (* v2 1) 0.0))))))

(FPCore (x)
  :name "test05_nonlin1, r4"
  :precision binary64
  :pre (< 1.00001 x 2)
  (let ([r1 (- x 1)] [r2 (* x x)])
    (/ r1 (- r2 1))))

(FPCore (x)
  :name "test05_nonlin1, test2"
  :precision binary64
  :pre (< 1.00001 x 2)
  (/ 1 (+ x 1)))

(FPCore (x0 x1 x2 x3)
  :name "test06_sums4, sum1"
  :precision binary32
  :pre (and (< -1e-5 x0 1.00001) (< 0 x1 1) (< 0 x2 1) (< 0 x3 1))
  (+ (+ (+ x0 x1) x2) x3))

(FPCore (x0 x1 x2 x3)
  :name "test06_sums4, sum2"
  :precision binary32
  :pre (and (< -1e-5 x0 1.00001) (< 0 x1 1) (< 0 x2 1) (< 0 x3 1))
(+ (+ x0 x1) (+ x2 x3)));; -*- mode: scheme -*-

;; These two appear in the text of the FPTaylor paper

(FPCore (t)
  :name "intro-example"
  :cite (solovyev-et-al-2015)
  :pre (<= 0 t 999)
  (/ t (+ t 1)))

(FPCore (x y)
  :name "sec4-example"
  :cite (solovyev-et-al-2015)
  :precision binary64
  :pre (and (<= 1.001 x 2) (<= 1.001 y 2))
  (let ([t (* x y)])
    (/ (- t 1) (- (* t t) 1))))

;; From the FPTaylor project <https://github.com/soarlab/FPTaylor>,
;; all `*.txt` files in the directory `benchmarks/tests/`.

(FPCore (x0 x1 x2)
  :name "test01_sum3"
  :precision binary32
  :pre (and (< 1 x0 2) (< 1 x1 2) (< 1 x2 2))
  (let ([p0 (- (+ x0 x1) x2)]
        [p1 (- (+ x1 x2) x0)]
        [p2 (- (+ x2 x0) x1)])
    (+ (+ p0 p1) p2)))

(FPCore (x0 x1 x2 x3 x4 x5 x6 x7 x8)
  :name "test02_sum8"
  :precision binary64
  :pre (and (< 1 x0 2) (< 1 x1 2) (< 1 x2 2)
            (< 1 x3 2) (< 1 x4 2) (< 1 x5 2)
            (< 1 x6 2) (< 1 x7 2))
  (+ (+ (+ (+ (+ (+ (+ x0 x1) x2) x3) x4) x5) x6) x7))

(FPCore (x y)
  :name "test03_nonlin2"
  :precision binary64
  :pre (and (< 0 x 1) (< -1 y -0.1))
  (/ (+ x y) (- x y)))

(FPCore (m0 m1 m2 w0 w1 w2 a0 a1 a2)
  :name "test04_dqmom9"
  :precision binary64
  :pre (and (< -1 m0 1) (< -1 m1 1) (< -1 m2 1)
            (< 0.00001 w0 1) (< 0.00001 w1 1) (< 0.00001 w2 1)
            (< 0.00001 a0 1) (< 0.00001 a1 1) (< 0.00001 a2 1))
  (let ([v2 (* (* w2 (- 0 m2)) (* -3 (* (* 1 (/ a2 w2)) (/ a2 w2))))]
        [v1 (* (* w1 (- 0 m1)) (* -3 (* (* 1 (/ a1 w1)) (/ a1 w1))))]
        [v0 (* (* w0 (- 0 m0)) (* -3 (* (* 1 (/ a0 w0)) (/ a0 w0))))])
    (+ 0.0 (+ (* v0 1) (+ (* v1 1) (+ (* v2 1) 0.0))))))

(FPCore (x)
  :name "test05_nonlin1, r4"
  :precision binary64
  :pre (< 1.00001 x 2)
  (let ([r1 (- x 1)] [r2 (* x x)])
    (/ r1 (- r2 1))))

(FPCore (x)
  :name "test05_nonlin1, test2"
  :precision binary64
  :pre (< 1.00001 x 2)
  (/ 1 (+ x 1)))

(FPCore (x0 x1 x2 x3)
  :name "test06_sums4, sum1"
  :precision binary32
  :pre (and (< -1e-5 x0 1.00001) (< 0 x1 1) (< 0 x2 1) (< 0 x3 1))
  (+ (+ (+ x0 x1) x2) x3))

(FPCore (x0 x1 x2 x3)
  :name "test06_sums4, sum2"
  :precision binary32
  :pre (and (< -1e-5 x0 1.00001) (< 0 x1 1) (< 0 x2 1) (< 0 x3 1))
(+ (+ x0 x1) (+ x2 x3)))'''
    import pprint
    for p in parser.parse(s):
        parsed = p
        print(parsed['props'])
        print(repr(parsed['prog']))
        print(parsed['prog'].infix())
        print('-'*80)
