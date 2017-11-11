from structures.domain import Domain, Action, State, Trace
from structures.sensor import Sensor, Sensor_Parser
import structures.sensor
from pddl.PDDL import PDDL_Parser
from nodeGenerator import NodeGenerator
from population import Population
from gpOps import GPOps
import monitoring.monitor
from monitoring.monitor import evaluate_sensor_on_traces

class GP(object):
    def __init__(self):
        pass

    def build_sensor_for_domain(self,pddl,modelSensor,sample_traces):
        parser = PDDL_Parser()
        parser.parse_domain(pddl)
        domain = parser.domain.groundify()

        traces = []
        if sample_traces > 0:
            print "Sampling {0} traces for domain {1}".format(sample_traces,pddl)
            traces = monitoring.monitor.sample_traces(pddl, sample_traces)
            print "Generated {0} valid traces from a sample of {1}".format(len(traces), sample_traces)
        else:
            print "Generating all traces for domain {0}".format(pddl)
            traces = monitoring.monitor.generate_all_traces(pddl)
            print "Generated {0} traces".format(len(traces))

        return self.build_sensor(domain,modelSensor, traces)

    def build_sensor(self, domain, modelSensor, traces, popSize=100, nGens=100, reproducePercent=0.8,mutatePercent=0.05,crossOverPercent=0.1):
        terms = []
        for i in range(0, 15):
            terms.append(Sensor.generate_sensor(domain, 1))
        print terms
        ng = NodeGenerator(terms, 1, 5, 2, 5)

        sp = Sensor_Parser()
        gpo = GPOps(terms, 1, 5, 1, 4)

        pop = Population(popSize, ng, reproducePercent, mutatePercent, crossOverPercent, gpo, sp.parse_sensor(modelSensor), traces)

        for i in range(0, nGens):
            print "g", i
            f = pop.generation()
            m = 0
            p = None
            for k, v in f.iteritems():
                if v > m:
                    m = v
                    p = k
                    #                       print p.compile()
            if m > 0:
                print m, p.compile()
            pop.updateGen(f)

        m = 0
        p = None
        for k, v in pop.generation().iteritems():
            if v > m:
                m = v
                p = k
        d = evaluate_sensor_on_traces(traces, sp.parse_sensor(modelSensor))
        a = evaluate_sensor_on_traces(traces, p.compile())

        total = len(traces)
        tp = set(d[0]) & set(a[0])
        tn = set(d[1]) & set(a[1])
        fp = set(a[0]) & set(d[1])
        fn = set(a[1]) & set(d[0])
        # print len(tp)
        # print len(fp)
        # print len(tn)
        # print len(fn)
        # print len(tp) + len(tn) - len(fp) - len(fn)
        tpr = len(tp) / float(total)
        tnr = len(tn) / float(total)
        fpr = len(fp) / float(total)
        fnr = len(fn) / float(total)
        print "TPR: {0}".format(tpr)
        print "TNR: {0}".format(tnr)
        print "FPR: {0}".format(fpr)
        print "FNR: {0}".format(fnr)

        return (tpr,tnr,fpr,fnr)

if __name__ == '__main__':
    # TPR: 0.957627118644
    # TNR: 0.0
    # FPR: 0.0423728813559
    # FNR: 0.0
    gp = GP()
    gp.build_sensor_for_domain('examples/psr-small/domain01.pddl',"((NOT-UPDATED-CB1) v (UPDATED-CB1))",1000)


