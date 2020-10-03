from structures.domain import Domain, Action, State, Trace
from structures.sensor import Sensor, Sensor_Parser, sensor_for_action
from pddl.PDDL import PDDL_Parser
from nodeGenerator import NodeGenerator
from population import Population
from gpOps import GPOps
import monitoring.monitor
from monitoring.monitor import MonitorSynthesizer
from pddl.propositional_planner import Propositional_Planner
import numpy as np
import pickle


class GP(object):
    def __init__(self,verbose=True):
        self.verbose = verbose
        self.state_space = []
        self.ms = MonitorSynthesizer()


    def build_sensor(self, domain, domain_name, instance, modelSensor, traces, terms, popSize=100, nGens=100, 
                    reproducePercent=0.8,mutatePercent=0.05,crossOverPercent=0.1, sensorDepth=1, tag=None):
        ng = NodeGenerator(terms, 1, 5, 2, 5)
        gpo = GPOps(terms, 1, 5, 1, 4)
        sp = Sensor_Parser()

        pop = Population(domain_name, instance, popSize, ng, reproducePercent, mutatePercent, crossOverPercent, gpo, sp.parse_sensor(modelSensor), traces, self.ms, tag)

        for i in range(0, nGens):
            if self.verbose: print "g", i
            f = pop.generation()
            m = 0
            p = None
            for k, v in f.iteritems():
                if v > m:
                    m = v
                    p = k
            if m > 0:
                print m, p.compile()
            pop.updateGen(f)

        m = 0
        p = None
        for k, v in pop.generation().iteritems():
            if v > m:
                m = v
                p = k

        d = self.ms.evaluate_sensor_on_traces(traces, sp.parse_sensor(modelSensor))
        a = self.ms.evaluate_sensor_on_traces(traces, p.compile())

        total = len(traces)
        tp = set(d[0]) & set(a[0])
        tn = set(d[1]) & set(a[1])
        fp = set(a[0]) & set(d[1])
        fn = set(a[1]) & set(d[0])
        tpr = len(tp) / float(total)
        tnr = len(tn) / float(total)
        fpr = len(fp) / float(total)
        fnr = len(fn) / float(total)
        print "TPR: {0}".format(tpr)
        print "TNR: {0}".format(tnr)
        print "FPR: {0}".format(fpr)
        print "FNR: {0}".format(fnr)

        return (tpr,tnr,fpr,fnr)


def gp_generate(domain_filename, domain_name, instance, problem_filename, traces, terms, popSize, nGens, sensor_depth=1):
    ss_stats = np.zeros((1, 9))  # Stats for the simple sensor
    cs_stats = np.zeros((1, 9))  # Stats for the complex sensor
    as_stats = np.zeros((1, 9))  # Stats for the action sensor

    print "Processing ", domain_filename
    pp = PDDL_Parser()
    pp.parse_domain(domain_filename)
    pp.parse_problem(problem_filename)
    pp.domain.groundify()

    simple_sensor = "({0} v {1})".format(pp.initial_state[1], pp.positive_goals[-1]).replace(",", "").replace("\'", "")
    print "Simple sensor: " + simple_sensor
    gp = GP(True)
    tpr, tnr, fpr, fnr = 0, 0, 0, 0
    tpr, tnr, fpr, fnr = gp.build_sensor(pp.domain, domain_name, instance, simple_sensor, traces, terms, popSize, nGens, sensorDepth=sensor_depth, tag="ss")

    ss_stats[0] = [instance,
                       len(pp.domain.all_facts),
                       len(pp.domain.actions),
                       len(pp.domain.state_space),
                       len(traces),
                       tpr, tnr, fpr, fnr]

    # Saving files in the middle of the loop in case of process kills
    print "Writing stats to ", domain_name + "-ss{0}.txt".format("%02d" % instance)
    np.savetxt('gp/output/' + domain_name + "-ss{0}.txt".format("%02d" % instance), ss_stats,
               fmt='%d %d %d %d %d %.4f %.4f %.4f %.4f', delimiter=" ", newline="\n",
               header="Index, #Predicates, #Actions, #States, #Traces, TPR, TNR, FPR, FNR", footer="", comments="")

    planner = Propositional_Planner(time_limit=0.3)
    print "Solving sample problem for " + problem_filename
    plan = planner.solve(pp.domain, pp.initial_state, pp.goal)
    traces.append((tuple(pp.initial_state),tuple(plan) ,(tuple(pp.goal[0]), tuple(pp.goal[1]))))
    print "Plan length: ", len(plan)

    complex_sensor = "({0} [{2}] {1})".format(pp.initial_state[1],
                                              pp.positive_goals[-1], len(plan) + 1).replace(",","").replace("\'", "")
    print "Complex sensor: " + complex_sensor
    gp = GP(True)
    tpr, tnr, fpr, fnr = 0, 0, 0, 0
    tpr, tnr, fpr, fnr = gp.build_sensor(pp.domain, domain_name, instance, complex_sensor, traces, terms, popSize, nGens, sensorDepth=sensor_depth, tag="cs")

    cs_stats[0] = [instance,
                       len(pp.domain.all_facts),
                       len(pp.domain.actions),
                       len(pp.domain.state_space),
                       len(traces),
                       tpr, tnr, fpr, fnr]

    # Saving files in the middle of the loop in case of process kills
    print "Writing stats to ", domain_name + "-cs{0}.txt".format("%02d" % instance)
    np.savetxt('gp/output/' + domain_name + "-cs{0}.txt".format("%02d" % instance), cs_stats,
               fmt='%d %d %d %d %d %.4f %.4f %.4f %.4f', delimiter=" ", newline="\n",
               header="Index, #Predicates, #Actions, #States, #Traces, TPR, TNR, FPR, FNR", footer="", comments="")

    action_sensor = sensor_for_action(plan[0])
    print "Action sensor: " + action_sensor
    gp = GP(True)
    tpr, tnr, fpr, fnr = 0, 0, 0, 0
    tpr, tnr, fpr, fnr = gp.build_sensor(pp.domain, domain_name, instance, action_sensor, traces, terms, popSize, nGens, sensorDepth=sensor_depth, tag="as")

    as_stats[0] = [instance,
                   len(pp.domain.all_facts),
                   len(pp.domain.actions),
                   len(pp.domain.state_space),
                   len(traces),
                   tpr, tnr, fpr, fnr]

    # Saving files in the middle of the loop in case of process kills
    print "Writing stats to ", domain_name + "-as{0}.txt".format("%02d" % instance)
    np.savetxt('gp/output/' + domain_name + "-as{0}.txt".format("%02d" % instance), as_stats,
               fmt='%d %d %d %d %d %.4f %.4f %.4f %.4f', delimiter=" ", newline="\n",
               header="Index, #Predicates, #Actions, #States, #Traces, TPR, TNR, FPR, FNR", footer="", comments="")


def main(argv): 
    sensor_depth = 3
    popSize = 100
    nGens = 100

    if len(argv) > 1:
        domain_name = str(argv[1])
        instance = int(argv[2])
        domain_filename = 'examples/' + domain_name + '/domain-' + str(instance) + '.pddl'
        problem_filename = 'examples/' + domain_name + '/task-' + str(instance) + '.pddl'
        traces_filename = 'resources/' + domain_name + '-' + str(instance) + '/traces.json'
        terms_filename = 'resources/' + domain_name + '-' + str(instance) + '/terms.json'
        
        # Load traces
        with open(traces_filename, 'r') as f:
            traces = pickle.load(f)

        # Load terms
        with open(terms_filename, 'r') as f:
            terms = pickle.load(f)

        # Execute
        gp_generate(domain_filename, domain_name, instance, problem_filename, traces, terms, popSize, nGens, sensor_depth)
        exit(0)
    else:
        print("Specify both the domain name and the number!")
        exit(1)


if __name__ == '__main__':
    import sys
    main(sys.argv)
