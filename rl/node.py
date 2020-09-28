import structures.sensor

class Node:
    """arity: spath 3, sand/sor 2, snot 1, terminal 0"""
    def __init__(self,parent,contents,arity):
        self.parent=parent
        self.contents=contents
        self.arity=arity
        self.children=[-1]*arity
        self.compiled=False

    
    def copyNode(self,parent):
        n=Node(parent,self.contents,self.arity)
        for i in range(0,self.arity):
                n.children[i]=self.children[i].copyNode(n)
        #if self.arity>0:
        #    n.children=[c.copyNode(n) for c in self.getChildren()]
        
        return n

    """only works if invoked on root of tree"""
    def __deepcopy__(self,memo):
        return self.copyNode(None)


    """index 0 - LHS, 1 - RHS, 2 - CENTER (only for SPATH)"""
    def setChild(self,index,child):
        self.children[index]=child

    def getChildren(self):
        return self.children[0:self.arity]

    """returns the sensor represented by this node"""
    def compile(self):
        """ already compiled """
        if self.compiled!=False:
            return self.compiled
        if self.arity==0:
            return self.contents
        elif self.contents==None:
            return self.children[0].compile()
        else:
            ch = []
            for c in self.children[0:self.arity]:
                ch.append(c.compile())
            return self.contents(*ch)

    """clear compiled sensor as needed. We go upwards rather than downwards as mutation/crossover won't affect stuff below"""
    def resetCompilation(self):
       self.compiled=False
       if self.parent!=None:
           self.parent.resetCompilation()

