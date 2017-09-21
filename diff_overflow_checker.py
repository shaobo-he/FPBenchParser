from fpbench_parser import parser 
from fpbench_classes import *
from z3 import *
import sys

#ex1 = '''
#(FPCore (x y)
#  :name "((x+y)/2.0)*((x+y)/2.0)"
#  (* (/ (+ x y) 2.0) (/ (+ x y) 2.0)))
#'''
#ex1 = '''
#(FPCore (r x)
#  :name "r*x-r*x^2"
#  (- (* r x) (* r (* x x))))
#'''
ex1 = '''
(FPCore (x)
  :name "(2.0 / ( x * ((x* x) - 1.0)))"
  (/ 2.0 (* x (- (* x x) 1.0))))
'''
ex2 = '''
(FPCore (x) (/ 2.0 (* (- (* x x) 1.0) x)))
'''
#ex2 = '''
#(FPCore (x y) (+ (* x (+ (* x 0.25) (* y 0.5))) (* 0.25 (* y y))))
#'''
#(FPCore (r x) (* (- r (* r x)) x))
#ex2 = '''
#(FPCore (r x) (/ r x))
#'''

s = Solver()

sort = Float64()

def flAdd(o1, o2):
   return fpAdd(RNE(), o1, o2)
                  
def flSub(o1, o2):
   return fpSub(RNE(), o1, o2)

def flMul(o1, o2):
   return fpMul(RNE(), o1, o2)

def flDiv(o1, o2):
   return fpDiv(RNE(), o1, o2)

def flSqrt(o):
   return fpSqrt(RNE(), o)

def NO(r):
  return Not(Or(fpEQ(r, fpPlusInfinity(sort)), fpEQ(r, fpMinusInfinity(sort))))

BINOPS = {'+' : flAdd,\
       '-' : flSub,\
       '*' : flMul,\
       '/' : flDiv \
      }

UNOPS = {'sqr' : (lambda x: flMul(x, x)),
      }

VARS = dict()

VAR_COUNT = -1

def getBinOpFunc(op):
  if op in BINOPS.keys():
    return BINOPS[op]
  else:
    raise RuntimeError("Operation not handled")

def getUnOpFunc(op):
  if op in UNOPS.keys():
    return UNOPS[op]
  else:
    raise RuntimeError("Operation not handled")

def mkVar():
  global VAR_COUNT
  VAR_COUNT += 1
  return FP('VAR@'+ str(VAR_COUNT), sort)
  
def getVar(e):
  if not e in VARS.keys():
    VARS[e] = mkVar()
  return VARS[e]

def mkEq(e, ops):
  nary = len(e.args)
  op = e.op
  if nary == 1:
    func = getUnOpFunc(op)
    s.add(fpEQ(getVar(e), func(ops[0])))
  elif nary == 2:
    func = getBinOpFunc(op)
    s.add(fpEQ(getVar(e), func(ops[0], ops[1])))
  else:
    raise RuntimeError("Operation not handled")

def visit(e, res_vars):
  if isinstance(e, op):
    ops = []
    res = getVar(e)
    for arg in e.args:
      if isinstance(arg, var):
        ops.append(VARS[arg.val]) 
      elif isinstance(arg, number):
        ops.append(sort.cast(float(arg.val)))
      elif isinstance(arg, op):
        ops.append(getVar(arg))
        visit(arg, res_vars)
      else:
        raise RuntimeError("Expression not handled")
    if e.op == '+' or e.op == '-' or e.op == '*' or e.op == '/':
    #if e.op == '/':
      res_vars.append(res)
    mkEq(e, ops)
  elif isinstance(e, var) or isinstance(e, number):
    pass
  else:
    raise RuntimeError("Expression not handled")

def assertValid(e):
  s.add(Not(e))

def assertNO(res_vars):
  if len(res_vars) > 1:
    return reduce((lambda x, y: And(x, y)), [NO(x) for x in res_vars])
  elif len(res_vars) == 1:
    return NO(res_vars[0])
  else:
    return True

def assertRelNO(e1, e2):
  return Implies(e1, e2)

def evalExpr(e, arg_vals):
  if not sort == Float64() and False:
    raise RuntimeError("Cannot evaluate other precisions")
  else:
    prog = ''
    for arg in arg_vals.keys():
      arg_val = arg_vals[arg]
      prog += '{0} = float({1})\n'.format(arg, arg_val)
    prog += ('print ' + e.infix())
    exec(prog)

def readProg(fn):
  with open(fn, 'r') as f:
    return f.read()

def check(args):
  status = s.check()
  if status == sat:
    m = s.model()
    #print m
    print {arg:eval(m[getVar(arg)].__str__()) for arg in args}
    #print reduce((lambda x, y: x+y), (eval(m[getVar(arg)].__str__()) for arg in args))
    evalExpr(prog1, {arg:m[getVar(arg)].__str__() for arg in args})
    evalExpr(prog2, {arg:m[getVar(arg)].__str__() for arg in args})
    for arg in args:
      s.add(Not(fpEQ(m[getVar(arg)], getVar(arg))))
  return status

if __name__ == '__main__':
  import pprint
  #sort = Float64()
  sort = FPSort(11, 26)
  ex1 = readProg(sys.argv[1])
  ex2 = readProg(sys.argv[2])
  for p1, p2 in zip(parser.parse(ex1), parser.parse(ex2)):
    args1 = p1['args']
    for arg in args1:
      VARS[arg] = FP(arg, sort)
    prog1 = p1['prog']
    prog2 = p2['prog']
    res_vars1 = list()
    res_vars2 = list()
    visit(prog1, res_vars1)
    visit(prog2, res_vars2)
    assertValid(assertRelNO(assertNO(res_vars1), assertNO(res_vars2)))
    #print s
    for i in range(1):
      status = check(args1)
