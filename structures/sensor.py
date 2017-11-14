import structures.domain
import re
import random

cache={}

class Sensor():
    neg = "-"
    lor = "v"
    land = "^"

    valid_ops = set([neg,lor,land])

    def __init__(self,lhs, op = None, rhs = None):
        # if(isinstance(lhs,tuple)):
        #     self.lhs = lhs[0]
        #     self.rhs = lhs[2]
        #     self.op = lhs[1]
        # else:
        #     self.lhs = lhs
        #     self.rhs = rhs
        #     self.op = op
        self.lhs = lhs
        self.rhs = rhs
        self.op = op

        if(self.op != None and self.op not in self.valid_ops and not isinstance(self.op, int)):
            print "***",self.op.func
            raise Exception("Invalid op "+ self.op)

    """used to generate terminal sensors for GP"""
    @classmethod
    def generate_sensor(cls, domain, depth):
        af=[d[0] for d in domain.all_facts]
        if depth==0:
            return Sensor(random.choice(af))
        else:
            op=random.choice([Sensor.neg,Sensor.lor,Sensor.land,"spath","terminal"])
            if op==Sensor.neg:
                return Sensor(Sensor.generate_sensor(domain, depth - 1), Sensor.neg)
            if op==Sensor.lor or op==Sensor.land:
                return Sensor(Sensor.generate_sensor(domain, depth - 1), op, Sensor.generate_sensor(domain, depth - 1))
            if op=="spath":
                return Sensor(Sensor.generate_sensor(domain, depth - 1), random.randint(1, 10), Sensor.generate_sensor(domain, depth - 1))
            if op=="terminal":
                return Sensor((random.choice(af),))


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

    def is_model_of(self, trace, state):
        #global cache
        #if (str(self),trace,state) in cache:
        #        return cache[(str(self),trace,state)]
        #cache[(str(self),trace,state)]=models(self,trace,state)
        #return cache[(str(self),trace,state)]
        return models(self, trace, state)

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

    def __hash__(self):
        return hash((self.lhs,self.op,self.rhs))

    def __repr__(self):
        s = "("
        if self.is_negated():
            s += self.print_op()
            s += str(self.lhs)
        else:
            # s += str(self.lhs) if isinstance(self.lhs, Sensor) else str(self.lhs[0])
            if isinstance(self.lhs, Sensor) or isinstance(self.lhs, bool):
                s += str(self.lhs)
            elif isinstance(self.lhs, tuple):
                s += self.lhs[0]
            else:
                s += self.lhs
            s += " "+str(self.print_op())+" " if self.op != None else ""
            s += str(self.rhs) if self.rhs!= None else ""

        s += ")"
        return s
        # return (str(self.lhs) if self.lhs != None else "") + (" "+str(self.print_op())+" " if self.op != None else "") + (str(self.rhs) if self.rhs!= None else "")

    def __str__(self):
        return repr(self)

    def __eq__(self, other):
        if isinstance(other, Sensor):
            return repr(self) == repr(other)
        else:
            return False

true = Sensor(True)



#sensor, trace,state
def models(sigma, t, s):
    # assert isinstance(sigma, Sensor)
    # assert isinstance(t, structures.domain.Trace)
    assert isinstance(s, structures.domain.State)
    if sigma.is_atom():
        return sigma.lhs is True or sigma.lhs in s
    elif sigma.is_negated():
        return not models(sigma.lhs, t, s)
    else:
        if sigma.op == sigma.land:
            return models(sigma.lhs, t, s) and models(sigma.rhs, t, s)
        elif sigma.op == sigma.lor:
            return models(sigma.lhs, t, s) or models(sigma.rhs, t, s)
        elif sigma.is_path_formula():
            if sigma.op == 0 or len(t) == 0:
                return models(sigma.lhs, t, s) and models(sigma.rhs, t, s)
            else:
                a = t[0]
                assert isinstance(a, structures.domain.Action)
                tp = t[1:]
                sp = a.result(s)
                if models(sigma.lhs, t, s):
                    if not models(sigma.rhs, t, s):
                        return models(Sensor(true, sigma.op - 1, sigma.rhs), tp, sp)
                    else:
                        return True
                else:
                    return models(sigma, tp, sp)
        else:
            raise Exception


# def models(sigma, t, s):
#     # assert isinstance(sigma, Sensor)
#     # assert isinstance(t, structures.domain.Trace)
#     global cache
#     if (sigma,tuple(t),s) in cache:
#             print "hitc"
#             return cache[(sigma,t,s)]
#
#     assert isinstance(s, structures.domain.State)
#     if sigma.is_atom():
#         cache[(sigma,t,s)]= sigma.lhs is True or sigma.lhs in s
#         return cache[(sigma,t,s)]
#         #return sigma.lhs is True or sigma.lhs in s
#     elif sigma.is_negated():
#         cache[(sigma,t,s)]=not models(sigma.lhs,t,s)
#         return cache[(sigma,t,s)]
#         #return not models(sigma.lhs, t, s)
#     else:
#         if sigma.op == sigma.land:
#             cache[(sigma,t,s)]=models(sigma.lhs, t, s) and models(sigma.rhs, t, s)
#             return cache[(sigma,t,s)]
#             #return models(sigma.lhs, t, s) and models(sigma.rhs, t, s)
#         elif sigma.op == sigma.lor:
#             cache[(sigma,t,s)]=models(sigma.lhs, t, s) or models(sigma.rhs, t, s)
#             return cache[(sigma,t,s)]
#             #return models(sigma.lhs, t, s) or models(sigma.rhs, t, s)
#         elif sigma.is_path_formula():
#             if sigma.op == 0 or len(t) == 0:
#                 cache[(sigma,t,s)]=models(sigma.lhs, t, s) and models(sigma.rhs, t, s)
#                 return cache[(sigma,t,s)]
#                 #return models(sigma.lhs, t, s) and models(sigma.rhs, t, s)
#             else:
#                 a = t[0]
#                 assert isinstance(a, structures.domain.Action)
#                 tp = t[1:]
#                 sp = a.result(s)
#                 if models(sigma.lhs, t, s):
#                     if not models(sigma.rhs, t, s):
#                         #return models(Sensor(true, sigma.op - 1, sigma.rhs), tp, sp)
#                         cache[(sigma,t,s)]=models(Sensor(true, sigma.op - 1, sigma.rhs), tp, sp)
#                         return cache[(sigma,t,s)]
#                     else:
#                         #cache[(sigma,t,s)]=True
#                         #return cache[(sigma,t,s)]
#                         return True
#                 else:
#                     cache[(sigma,t,s)]=models(sigma,tp,sp)
#                     return cache[(sigma,t,s)]
#                     #return models(sigma, tp, sp)
#         else:
#             raise Exception
#         return cache[(sigma,t,s)]

class Sensor_Parser():

    def __init__(self):
        self.true = Sensor(True)

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
        for t in re.findall(r'[()]|[^\s()]+', str.lower()):
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
            raise Exception('Malformed expression: '+str)
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
            raise Exception("Invalid operator "+str)

    def parse_sensor(self, str):
        tokens = self.scan_tokens(str)
        if type(tokens) is list:
            return self.build_sensor(tokens)
        else:
            raise Exception('Expression ' + str + ' does not match a sensor')

    def build_sensor(self,tokens):
        # TODO Fix the nasty bit of code below...
        if isinstance(tokens,list) and len(tokens) == 1:  # This should be a symbol
            # t = tokens.pop(0)
            # if t is list:
            #     return self.build_sensor(t)
            # else:
            #     return Sensor(self.parse_symbol(t))
            return Sensor(self.parse_symbol(tokens))
        elif isinstance(tokens,str):
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
            raise 'Expression ' + str(tokens) + ' does not match a sensor'

    def parse_symbol(self,str):
        if str == "true":
            return True
        elif str == "false":
            return False
        else:
            return tuple(str)


# TODO Move this into the parser class?
def sensor_for_action(action):
    precond = ""
    pos_precond = "{0}" if len(action.positive_preconditions) > 0 else "True"
    neg_precond = "{0}" if len(action.negative_preconditions) > 0 else "True"
    for i in range(0, len(action.positive_preconditions)):
        if i == len(action.positive_preconditions) - 1:
            pos_precond = pos_precond.format(str(action.positive_preconditions[i]))
        else:
            pos_precond = "({0} ^ {1})".format(pos_precond.format(str(action.positive_preconditions[i])),"{0}")

    for i in range(0, len(action.negative_preconditions)):
        if i == len(action.negative_preconditions) - 1:
            neg_precond = neg_precond.format("(-"+str(action.negative_preconditions[i])+")")
        else:
            neg_precond = "({0} ^ {1})".format(neg_precond.format("(-"+str(action.negative_preconditions[i]))+")","{0}")

    precond = "({0} ^ {1})".format(pos_precond,neg_precond)

    pos_precond = "{0}" if len(action.add_effects) > 0 else "True"
    neg_precond = "{0}" if len(action.del_effects) > 0 else "True"
    for i in range(0, len(action.add_effects)):
        if i == len(action.add_effects) - 1:
            pos_precond = pos_precond.format(str(action.add_effects[i]))
        else:
            pos_precond = "({0} ^ {1})".format(pos_precond.format(str(action.add_effects[i])), "{0}")

    for i in range(0, len(action.del_effects)):
        if i == len(action.del_effects) - 1:
            neg_precond = neg_precond.format("(-" + str(action.del_effects[i])+")")
        else:
            neg_precond = "({0} ^ {1})".format(neg_precond.format("(-" + str(action.del_effects[i]))+")", "{0}")

    effect = "({0} ^ {1})".format(pos_precond,neg_precond)
    return "({0} [1] {1})".format(precond,effect).replace(",","").replace("'","");

def sand(s1,s2):
    return Sensor(s1,"^",s2)


def sor(s1,s2):
    return Sensor(s1,"v",s2)

def snot(s1):
    return Sensor(s1,"-")


def spath(s1,s2,i):
    assert isinstance(i,int)
    return Sensor(s1,i,s2)
