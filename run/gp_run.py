
from structures.domain import Domain, Action, State, Trace
from structures.sensor import Sensor, Sensor_Parser
from pddl.PDDL import PDDL_Parser
from gp.nodeGenerator import NodeGenerator
from gp.population import Population
from gp.gpOps import GPOps
import monitoring.monitor
from monitoring.monitor import evaluate_sensor_on_traces



def test_randomsensor():
        parser=PDDL_Parser()
        simplePDDL='examples/simple/simple.pddl'
        parser.parse_domain(simplePDDL)
        parser.parse_problem('examples/simple/pb1.pddl')
        domain = parser.domain.groundify()
        terms=[]
        for i in range(0,15):
          terms.append(Sensor.generate_sensor(domain, 2))
        print terms
        ng=NodeGenerator(terms,1,5,2,5)

        traces=monitoring.monitor.generate_all_traces(simplePDDL)

        sp=Sensor_Parser()
        gpo=GPOps(terms,1,5,1,4)

        pop=Population(100,ng,0.8,0.05,0.1,gpo,sp.parse_sensor("(p v q)"),traces)

        for i in range(0,100):
                print "g",i
                f=pop.generation()
                m=0
                p=None
                for k,v in f.iteritems():
                        if v>m:
                                m=v
                                p=k
                print m,p,len(pop.pop)


        print pop.generation()



if __name__ == '__main__':
        test_randomsensor()
