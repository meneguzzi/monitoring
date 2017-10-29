import structures.sensor

class Node:
    """arity: spath 3, sand/sor 2, snot 1, terminal 0"""
    def __init__(self,parent,contents,arity):
        self.parent=parent
	self.contents=contents
	self.arity=arity
	self.children=[-1,-1,-1]
	self.compiled=False

    """index 0 - LHS, 1 - RHS, 2 - CENTER (only for SPATH)"""
    def setChild(self,index,child):
        self.children[index]=child

    def children():
        return self.children[0:arity]

    """returns the sensor represented by this node"""
    def compile(self):
        """ already compiled """
        if self.compiled!=False:
		return self.compiled
	if self.arity==0:
		return self.contents
	else:
		ch=[c.compile() for c in self.children[0:self.arity]]
		return self.contents(*ch)

    """clear compiled sensor as needed. We go upwards rather than downwards as mutation/crossover won't affect stuff below"""
    def resetCompilation(self):
       self.compiled=False
       if self.parent!=None:
           self.parent.resetCompilation()

