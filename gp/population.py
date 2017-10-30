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
      for ind in fitness: #return first individual if all fitnesses are 0
              return ind


  def generation(self):
      fitness=self.iterate() #a ind:fitnessValue map

      #normalize
      s=reduce((lambda x,y: x+y),fitness.values())
      if s!=0:
          fitness={k:(v/s) for k,v in fitness.items()}  
      else:
          fitness={k:0 for k,v in fitness.items()}    

      newGen=[]
      for i in range(0,int(len(self.pop)*self.reproducePercent)):
          newGen.append(self.pickIndividual(fitness))
      for i in range(0,int(len(self.pop)*self.mutatePercent)):
          newGen.append(self.gpOps.mutate(self.pickIndividual(fitness)))
      for i in range(0,int(len(self.pop)*self.crossOverPercent)):
          newGen.extend(self.gpOps.crossOver(self.pickIndividual(fitness),self.pickIndividual(fitness)))
      for i in range(0,len(self.pop)-int(len(self.pop)*self.reproducePercent+self.mutatePercent+self.crossOverPercent)):
          newGen.append(self.ng.addNode(None,1))
      self.pop=newGen
      return fitness
      
