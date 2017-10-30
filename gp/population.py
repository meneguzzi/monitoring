import random
from nodeGenerator import NodeGenerator
import gpOps
from monitoring.monitor import evaluate_sensor_on_traces


class Population:
  """ng is the initial population generator"""
  def __init__(self,num,ng,reproducePercent,mutatePercent,crossOverPercent,gpOps,modelSensor,traces):
    self.num=num
    self.ng=ng
    self.pop=[]
    for i in range(0,num):
        self.pop.append(ng.addNode(None,1))
    self.reproducePercent=reproducePercent #percent of pure copy
    self.mutatePercent=mutatePercent #percent which will be mutated
    self.crossOverPercent=crossOverPercent #percent of pop generated using crossover

    self.modelSensor=modelSensor
    self.traces=traces
    self.gpOps=gpOps

     
  def iterate(self):
    fitness={}
    for p in self.pop:
        desired=evaluate_sensor_on_traces(self.traces,self.modelSensor)
        actual=evaluate_sensor_on_traces(self.traces,p.compile())


        tp=set(desired[0]) & set(actual[0])
        tn=set(desired[1]) & set(actual[1])

        fp=set(actual[0]) - set(desired[1])
        fn=set(actual[1]) - set(desired[0])

        fitness[p]=(len(tp)+len(tn)-len(fp)-len(fn))
    return fitness

  def pickIndividual(self,fitness):
      r=random.random()
      s=0
      for ind in fitness:
          s+=fitness[ind]
          if s>=r:
              return ind
      return random.choice(fitness.keys()) #return random individual otherwise


  def generation(self):
      fitness=self.iterate() #a ind:fitnessValue map

      #normalize
      s=reduce((lambda x,y: x+y),fitness.values())
      if s!=0:
          fitness={k:(v/s) for k,v in fitness.items()}  
      else:
          fitness={k:0 for k,v in fitness.items()}    

      newGen=[]
      for i in range(0,int(self.num*self.reproducePercent)):
          newGen.append(self.pickIndividual(fitness))
      #print "r", len(newGen)
      for i in range(0,int(self.num*self.mutatePercent)):
          newGen.append(self.gpOps.mutate(self.pickIndividual(fitness)))
      #print "m", len(newGen)
      for i in range(0,int(self.num*self.crossOverPercent*0.5)):
          newGen.extend(self.gpOps.crossOver(self.pickIndividual(fitness),self.pickIndividual(fitness)))
      #print "c",len(newGen)
      for i in range(0,self.num-int(self.num*(self.reproducePercent+self.mutatePercent+self.crossOverPercent))):
          newGen.append(self.ng.addNode(None,1))
      #print "n",len(newGen)
      self.pop=newGen
      return fitness
      
