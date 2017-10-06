from trace import Trace
from state import State
from action import Action


class Sensor():
    neg = "-"
    lor = "v"
    land = "^"

    def __init__(self,lhs, rhs = None, op = None):
        if(isinstance(lhs,tuple)):
            self.lhs = lhs[0]
            self.rhs = lhs[2]
            self.op = lhs[1]
        else:
            self.lhs = lhs
            self.rhs = rhs
            self.op = op

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


def models(sigma, t, s, A):
    # type: (Sensor, Trace, State, object) -> bool
    assert isinstance(sigma, Sensor)
    assert isinstance(t, Trace)
    assert isinstance(s, State)
    if sigma.is_atom():
        return sigma.lhs is True or sigma in s
    elif sigma.is_negated():
        return sigma not in s
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
                assert isinstance(a, Action)
                tp = t[1:]
                sp = a.result(s)
                if models(sigma.lhs, t, s, A):
                    if not models(Sensor(sigma.rhs), t, s, A):
                        return models(Sensor(True, sigma.op -1, sigma.rhs), tp, sp, A)
                    else:
                        return True
                else:
                    return models(sigma,tp,sp,A)
        else:
            raise Exception