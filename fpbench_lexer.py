from ply import lex
import re

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

ops = ["+","-","*","/","fabs","fma","exp","exp2","expm1","log","log10","log2",
       "log1p","pow","sqrt","cbrt","hypot","sin","cos","tan","asin","acos",
       "atan","atan2","sinh","cosh","tanh","asinh","acosh","atanh","erf","erfc",
       "tgamma","lgamma","ceil","floor","fmod","remainder","fmax","fmin","fdim",
       "copysign","trunc","round","nearbyint","=>","<=",">=","==","!=","<",">",
       "and","or","not","isfinite","isinf","isnan","isnormal","signbit"]

consts = ["E","LOG2E","LOG10E","LN2","LN10","PI","PI_2","PI_4","1_PI","2_PI",
          "2_SQRTPI","SQRT2","SQRT1_2","INFINITY","NAN","TRUE","FALSE"]

keywords = {
    'if' : 'IF',
    'let' : 'LET',
    'while' : 'WHILE'
}

__num_re = re.compile(r'[-+]?[0-9]+(((\.)?|(\.[0-9]+)?)(e[-+]?[0-9]+)?)?')

__nums = {str(i) for i in range(10)}

def t_COMMENT(t):
    r';.*\n'
    t.lexer.lineno += 1
    pass

def t_SYMBOL(t):
    r'[a-zA-Z0-9~!@$%^&*_\-\+=<>\.\?/:][a-zA-Z0-9~!@$%^&*_\-+=<>\.\?/:]*'
    if t.value in ops:
        t.type = "OPERATION"
    elif t.value in consts:
        t.type = "CONSTANT"
    elif t.value in keywords.keys():
        t.type = keywords[t.value]
    # Actually a number
    elif __num_re.fullmatch(t.value):
        try:
            float(t.value)
        except:
            print("Floating point expression is wrong")
            assert(0)
        t.type = "NUMBER"
    # Tentatively a symbol
    else:
        if str(t.value)[0] in __nums:
            print("Symbol starts with number:", t.value)
            assert(0)
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

t_ignore = ' \t\r\f\v'

t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACK = r'\['
t_RBRACK = r'\]'
t_STRING = r'"([\x20-\x5b\x5d-\x7e]|\\["\\n])+?"'

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
