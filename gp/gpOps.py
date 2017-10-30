class GPOps:
  def __init__(self,terminals,minSpath,maxSpath,minDepth,maxDepth):
    self.terminals=terminals
    self.minSpath=minSpath
    self.maxSpath=maxSpath
    self.minDepth=minDepth
    self.maxDepth=maxDepth

  def pickNode(self,root):
    nodeList=[]
    toVisit=[root]
    while True:
	  if len(toVisit)==0:
		  break
	  c=toVisit.pop()
	  nodeList.append(c)
	  if c.children()!=[]:
	    toVisit.append(c.children())
    return random.choice(nodeList) 

  def mutate(self,root):
    ng=NodeGenerator(self.terminals,self.minSpath,self.maxSpath,self.minDepth,self.maxDepth)
    root=root.copyNode(None)
    r=pickNode(root)
    if r.parent.children.index(r)==2:
	    r=ng.terminalInt(r.parent)
    else:   
      r=ng.addNode(r.parent,1)
    r.resetCompilation()
    return root

  def crossOver(self,root1,root2):
    okNodes=False
    root1=root1.CopyNode(None)
    root2=root2.CopyNode(None)
    while not okNodes:
      n1=pickNode(root1)
      n2=pickNode(root2)
      if (not n1.parent.children[2]==n1) and (not n2.parent.children[2]==n2):
	      okNodes=True
    n1.parent.children[n1.parent.children.index(n1)]=n2
    n2.parent.children[n2.parent.children.index(n2)]=n1
    t=n1.parent
    n1.parent=n2.parent
    n2.parent=t
    n1.resetCompilation()
    n2.resetCompilation()
    return [root1,root2]

