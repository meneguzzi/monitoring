
class State():

    def __init__(self,facts=None):
        ## A state has a dictionary of facts
        self.facts = set([])
        if facts is not None:
            self.facts |= set(facts)

    def models(self, other):
        if isinstance(other,State):
            return other.facts.issubset(self.facts)
        elif isinstance(other,set):
            return other.issubset(self.facts)
        else:
            return other in self.facts

    def __contains__(self, item):
        return item in self.facts

    def __eq__(self, other):
        if isinstance(other,State):
            return self.facts == other.facts
        else:
            return False

    def __add__(self, other):
        if isinstance(other,State):
            self.facts |= other.facts
        else:
            self.facts |= set([other])
        return self

    def __setitem__(self, key, value):
        if key in self.facts and value is False:
            self.facts.remove(key)
        elif key not in self.facts and value:
            self.facts.add(key)
        else: # all other cases require nothing to be done
            pass


    def __getitem__(self, item):
        return item in self.facts

    def __sub__(self, other):
        if isinstance(other,State):
            self.facts -= other.facts
        else:
            self.facts.remove(other)
        return self

    def __str__(self):
        return str("State: "+str(list(self.facts)))

    def __repr__(self):
        return str(list(self.facts))


if __name__ == '__main__':
    s = State(['p','q'])
    print s

    s1 = State(['p','q'])
    s2 = State(['p','q'])
    s3 = State(['q'])

    print s1 == s2
    print s1 == s3
    print s3 == s1
    print s1.models(s2)
