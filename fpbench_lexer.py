from ply import lex

tokens = (
    "LPAREN",
    "RPAREN",
    "LBRACK",
    "RBRACK",
    "IF",
    "LET",
    "WHILE",
    "NUMBER",
    "CONSTANT",
    "SYMBOL",
    "STRING",
    "OPERATION"
)

def t_OPERATION(t):
    r'\+|\-|\*|/|fabs|fma|exp|exp2|expm1|log|log10|log2|log1p|pow|sqrt|cbrt|hypot|sin|cos|tan|asin|acos|atan|atan2|sinh|cosh|tanh|asinh|acosh|atanh|erf|erfc|tgamma|lgamma|ceil|floor|fmod|remainder|fmax|fmin|fdim|copysign|trunc|round|nearbyint|<=|>=|==|!=|<|>|and|or|not|isfinite|isinf|isnan|isnormal|signbit'
    return t

def t_CONSTANT(t):
    r'E|LOG2E|LOG10E|LN2|LN10|PI|PI_2|PI_4|1_PI|2_PI|2_SQRTPI|SQRT2|SQRT1_2|INFINITY|NAN|TRUE|FALSE'
    return t

def t_IF(t):
    r'if'
    return t

def t_LET(t):
    r'let'
    return t

def t_WHILE(t):
    r'while'
    return t

def t_COMMENT(t):
    r';.*\n'
    pass

t_ignore = ' \t\r\n\f\v'

t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACK = r'\['
t_RBRACK = r'\]'
t_NUMBER = r'[-+]?[0-9]+(\.[0-9]+(e[-+]?[0-9]+)?)?'
t_SYMBOL = r'[a-zA-Z~!@$%^&*_\-+=<>.?/:][a-zA-Z0-9~!@$%^&*_\-+=<>.?/:]*'
t_STRING = r'"([\x20-\x5b\x5d-\x7e]|\\["\\])+?"'

# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

lexer = lex.lex()
    
# Test cases
if __name__ == '__main__':
    
    lex.lex()

    lex.input('''(FPCore (t)
  :name "intro-example"
  :cite (solovyev-et-al-2015)
  :pre (<= 0 t 999)
(/ t (+ t 1)))''')
    for tok in iter(lex.token, None):
        print(repr(tok.type), repr(tok.value))
