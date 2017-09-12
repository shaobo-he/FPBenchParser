class expr:
    def __repr__(self):
        return type(self).__name__ + '(' + repr(self.val) + ')'
    def __str__(self):
        return str(self.val)
    def infix(self):
        return str(self.val)
    
class var(expr):
    def __init__(self, val):
        self.val = val
    
class constant(expr):
    def __init__(self, val):
        self.val = val

class number(expr):
    def __init__(self, val):
        self.val = val

class op(expr):
    def __init__(self, op, args):
        self.op = op
        self.args = args
        
    def __repr__(self):
        return '{}({},{})'.format(type(self).__name__,self.op, ",".join(list(map(repr,self.args))))
    def __str__(self):
        return '({} {})'.format(self.op, " ".join(list(map(str, self.args))))

    def infix(self):
        if len(self.args) == 1:
            return "{}({})".format(self.op, self.args[0].infix())
        elif len(self.args) == 2:
            return "({}{}{})".format(self.args[0].infix(),
                                     self.op,
                                     self.args[1].infix())
        else:
            return "{}({})".format(self.op, ','.join(list(map(lambda x: x.infix(),
                                                              self.args))))
            
