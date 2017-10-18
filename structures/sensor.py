import structures.domain


class Sensor():
    neg = "-"
    lor = "v"
    land = "^"

    valid_ops = set([neg,lor,land])

    def __init__(self,lhs, op = None, rhs = None):
        if(isinstance(lhs,tuple)):
            self.lhs = lhs[0]
            self.rhs = lhs[2]
            self.op = lhs[1]
        else:
            self.lhs = lhs
            self.rhs = rhs
            self.op = op

        if(self.op != None and self.op not in self.valid_ops and not isinstance(self.op, int)):
            raise Exception("Invalid op "+ self.op)



    @property
    def lhs(self):
        return self.lhs

    @property
    def rhs(self):
        return self.rhs

    @property
    def op(self):
        # assert isinstance(self.op, object)
        return self.op

    def is_atom(self):
        return self.op is None and self.rhs is None

    def is_negated(self):
        return self.op == self.neg

    def is_path_formula(self):
        return isinstance(self.op, int)

    def is_model_of(self, trace, state, actions):
        return models(self, trace, state, actions)

    def __getitem__(self, item):
        if item == 0:
            return self.lhs
        elif item == 1:
            return self.op
        elif item == 2:
            return self.rhs
        else:
            raise IndexError("Sensor formulas have at most 3 components")

    def print_op(self):
        if self.op is not None and isinstance(self.op, int):
            return "["+str(self.op)+"]"

        return self.op

    def __repr__(self):
        return (str(self.lhs) if self.lhs != None else "") + (" "+str(self.print_op())+" " if self.op != None else "") + (str(self.rhs) if self.rhs!= None else "")

    def __str__(self):
        return repr(self)

true = Sensor(True)


def sand(s1,s2):
    return Sensor(s1,"^",s2)


def sor(s1,s2):
    return Sensor(s1,"v",s2)


def snot(s1):
    return Sensor(s1,"-")


def spath(i,s1,s2):
    assert isinstance(i,int)
    return Sensor(s1,i,s2)


def models(sigma, t, s, A):
    # assert isinstance(sigma, Sensor)
    # assert isinstance(t, structures.domain.Trace)
    assert isinstance(s, structures.domain.State)
    assert isinstance(A, structures.domain.Domain)
    if sigma.is_atom():
        return sigma.lhs is True or sigma.lhs in s
    elif sigma.is_negated():
        return sigma.lhs not in s
    else:
        if sigma.op == sigma.land:
            return models(sigma.lhs, t, s, A) and models(sigma.rhs, t, s, A)
        elif sigma.op == sigma.lor:
            return models(sigma.lhs, t, s, A) or models(sigma.rhs, t, s, A)
        elif sigma.is_path_formula():
            if sigma.op == 0:
                return models(sigma.lhs, t, s, A) and models(sigma.rhs, t, s, A)
            else:
                a = t[0]
                assert isinstance(a, structures.domain.Action)
                tp = t[1:]
                sp = a.result(s)
                if models(sigma.lhs, t, s, A):
                    if not models(Sensor(sigma.rhs), t, s, A):
                        return models(Sensor(true, sigma.op -1, sigma.rhs), tp, sp, A)
                    else:
                        return True
                else:
                    return models(sigma,tp,sp,A)
        else:
            raise Exception


import re


class Sensor_Parser():

    def read_file(self,filename):
        str = ""

        with open(filename, 'r') as f:
            # Remove single line comments
            str = re.sub(r';.*$', '', f.read(), flags=re.MULTILINE).lower()

        return str
    # ------------------------------------------
    # Tokens
    # ------------------------------------------

    def scan_tokens(self, str):
        # Tokenize
        stack = []
        list = []
        for t in re.findall(r'[()]|[^\s()]+', str):
            if t == '(':
                stack.append(list)
                list = []
            elif t == ')':
                if stack:
                    l = list
                    list = stack.pop()
                    list.append(l)
                else:
                    raise Exception('Missing open parentheses')
            else:
                list.append(t)
        if stack:
            raise Exception('Missing close parentheses')
        if len(list) != 1:
            raise Exception('Malformed expression')
        return list[0]

    def parse_sensor_file(self, filename):
        return self.parse_sensor(self.read_file(filename))

    def parse_op(self,str):
        if str[0]=="[" and str[-1]=="]":
            return int(str[1:-1])
        elif str == "&":
            return Sensor.land
        elif str == "|":
            return Sensor.lor
        elif str == "~":
            return Sensor.neg
        elif str in Sensor.valid_ops:
            return str
        else:
            raise "Invalid operator "+str

    def parse_sensor(self, str):
        tokens = self.scan_tokens(str)
        if type(tokens) is list:
            return self.build_sensor(tokens)
        else:
            raise 'Expression ' + str + ' does not match a sensor'

    def build_sensor(self,tokens):
        if (tokens is list and len(tokens) == 1):  # This should be a symbol
            t = tokens.pop(0)
            if t is list:
                return self.build_sensor(t)
            else:
                return Sensor(self.parse_symbol(t))
        elif (isinstance(tokens,str)):
            return Sensor(self.parse_symbol(tokens))
        elif len(tokens) == 2:  # This should be a negation
            op = tokens.pop(0)
            lhs = tokens.pop(0)
            return Sensor(lhs=self.build_sensor(lhs),op=self.parse_op(op))
        elif len(tokens) == 3:
            lhs = tokens.pop(0)
            op = tokens.pop(0)
            rhs = tokens.pop(0)
            return Sensor(self.build_sensor(lhs),self.parse_op(op),self.build_sensor(rhs))
        else:
            raise 'Expression ' + tokens + ' does not match a sensor'

    def parse_symbol(self,str):
        if str == "True":
            return True
        elif str == "False":
            return False
        else:
            return str