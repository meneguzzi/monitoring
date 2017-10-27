from structures.domain import Domain, Action, State, Trace
from structures.sensor import Sensor, Sensor_Parser
from structures import sensor
from deap import gp,creator,base,tools,algorithms
from monitoring import monitor
import random,numpy

from pddl.PDDL import PDDL_Parser

def getTerminalSensors(domain,num):
    return Sensor.generate_sensor(domain, num)


parser = PDDL_Parser()
parser.parse_domain('examples/simple/simple.pddl')
parser.parse_problem('examples/simple/pb1.pddl')
domain = parser.domain.groundify()

"""create the pset"""
pset=gp.PrimitiveSetTyped("Main",[],Sensor)
pset.addPrimitive(sensor.sand,[Sensor,Sensor],Sensor)
pset.addPrimitive(sensor.sor,[Sensor,Sensor],Sensor)
pset.addPrimitive(sensor.snot,[Sensor],Sensor)
pset.addPrimitive(sensor.spath,[int,Sensor,Sensor],Sensor)

NUMTERMINALS=20
NUMSTEPS=5

for ts in getTerminalSensors(domain,NUMTERMINALS):
    pset.addTerminal(ts,Sensor)

for i in range(1,NUMSTEPS+1):
    pset.addTerminal(i,int)

creator.create("FitnessMax",base.Fitness,weights=(1.0,))
creator.create("Individual",gp.PrimitiveTree,fitness=creator.FitnessMax)

toolbox = base.Toolbox()
toolbox.register("expr", gp.genHalfAndHalf, pset=pset, min_=1, max_=2)
toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.expr)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("compile", gp.compile, pset=pset)

TRACES=monitor.generate_all_traces("examples/simple/simple.pddl")
MODELSENSOR=Sensor(True)

def evalSensor(sensor):
    desired=monitor.evaluate_sensor_on_traces(TRACES,MODELSENSOR)
    actual=monitor.evaluate_sensor_on_traces(TRACES,sensor)

    tp=set(desired[0]) & set(actual[0])
    tn=set(desired[1]) & set(actual[1])

    fp=set(actual[0]) - set(desired[1])
    fn=set(actual[1]) - set(desired[0])

    return (len(tp)+len(tn)-len(fp)-len(fn)),

toolbox.register("evaluate",evalSensor)

toolbox.register("select", tools.selTournament, tournsize=3)
toolbox.register("mate", gp.cxOnePoint)
toolbox.register("expr_mut", gp.genFull, min_=0, max_=2)
toolbox.register("mutate", gp.mutUniform, expr=toolbox.expr_mut, pset=pset)

def main():
    random.seed(10)
    pop=toolbox.population(n=100)
    hof=tools.HallOfFame(1)

    stats=tools.Statistics(lambda ind: ind.fitness.values)

    stats.register("avg", numpy.mean)
    stats.register("std", numpy.std)
    stats.register("min", numpy.min)
    stats.register("max", numpy.max)

    algorithms.eaSimple(pop, toolbox, 0.5, 0.2, 40, stats, halloffame=hof)
    return pop, stats, hof

if __name__ == "__main__":
        main()

