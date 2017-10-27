from structures.domain import Domain, Action, State, Trace
from structures.sensor import Sensor, Sensor_Parser
from deap import gp,creator,base,tools


from pddl.PDDL import PDDL_Parser

def getTerminalSensors(domain,num):
    return Sensor.generate_sensor(domain, num)


"""create the pset"""
pset=gp.PrimitiveSetTyped("Main",[],Sensor)
pset.addPrimitive(Sensor.sand,[Sensor,Sensor],Sensor)
pset.addPrimitive(Sensor.sor,[Sensor,Sensor],Sensor)
pset.addPrimitive(Sensor.snot,[Sensor],Sensor)
pset.addPrimitive(Sensor.spath,[int,Sensor,Sensor],Sensor)

pset.addTerminal()