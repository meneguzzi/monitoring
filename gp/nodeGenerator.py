from node import Node
import random
import structures.sensor

class NodeGenerator:
    def __init__(self,terminals,minSpath,maxSpath,minDepth,maxDepth):
        """minimum and maximum values passed to the SPATH int. """
        self.minSpath=minSpath
	self.maxSpath=maxSpath
	self.minDepth=minDepth
	self.maxDepth=maxDepth

	self.terminals=terminals

    def growNone(self,parent,curDepth):
      n=Node(parent,None,1)
      n.setChild(0,self.addNode(n,curDepth)) 
      return n

    def growSnot(self,parent,curDepth):
       n=Node(parent,structures.sensor.snot,1)
       n.setChild(0,self.addNode(n,curDepth+1)) 
       return n

    def growSand(self,parent,curDepth):
       n=Node(parent,structures.sensor.sand,2)
       n.setChild(0,self.addNode(n,curDepth+1))
       n.setChild(1,self.addNode(n,curDepth+1))
       return n

    def growSor(self,parent,curDepth):
       n=Node(parent,structures.sensor.sor,2)
       n.setChild(0,self.addNode(n,curDepth+1))
       n.setChild(1,self.addNode(n,curDepth+1))
       return n

    def growSpath(self,parent,curDepth):
       n=Node(parent,structures.sensor.spath,3)
       n.setChild(0,self.addNode(n,curDepth+1))
       n.setChild(1,self.addNode(n,curDepth+1))
       n.setChild(2,self.terminalInt(n))
       return n

    def terminalInt(self,parent):
       return Node(parent,random.randint(self.minSpath,self.maxSpath),0)

    def pickTerminal(self,parent,_):
       t=random.choice(self.terminals)
       n=Node(parent,t,0)
       return n

    def addNode(self,parent,curDepth):
       choices=[self.growSand, self.growSor, self.growSpath, self.growSnot, self.pickTerminal]
       sel=None

       if parent==None:
               return self.growNone(None,curDepth)

       if curDepth<self.minDepth:
	       choices.remove(self.pickTerminal)
       if curDepth>=self.maxDepth:
	       sel=self.pickTerminal
       else:
	       sel=random.choice(choices)
       return sel(parent,curDepth)


