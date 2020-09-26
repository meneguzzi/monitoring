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
import gc

class GP(object):
    def __init__(self,verbose=True):
        self.verbose = verbose
        self.state_space = []
        self.ms = MonitorSynthesizer()

    def build_sensor_for_domain(self, pddl, model_sensor, samples, popSize=100, nGens=100):
        parser = PDDL_Parser()
        parser.parse_domain(pddl)
        domain = parser.domain.groundify()

        traces = []
        if samples > 0:
            print "Sampling {0} traces for domain {1}".format(samples, pddl)
            traces = monitoring.monitor.sample_traces(pddl, samples)
            print "Generated {0} valid traces from a sample of {1}".format(len(traces), samples)
        else:
            print "Generating all traces for domain {0}".format(pddl)
            traces = monitoring.monitor.generate_all_traces(pddl)
            print "Generated {0} traces".format(len(traces))

        return self.build_sensor(domain, model_sensor, traces, popSize, nGens)

    def build_sensor(self, domain, modelSensor, traces,
                     popSize=100, nGens=100, reproducePercent=0.8,mutatePercent=0.05,crossOverPercent=0.1,
                     sensorDepth=1):
        terms = []
        for i in range(0, 15):
            terms.append(Sensor.generate_sensor(domain, sensorDepth))
        print terms

        ng = NodeGenerator(terms, 1, 5, 2, 5)

        sp = Sensor_Parser()
        gpo = GPOps(terms, 1, 5, 1, 4)

        pop = Population(popSize, ng, reproducePercent, mutatePercent, crossOverPercent, gpo, sp.parse_sensor(modelSensor), traces, self.ms)

        for i in range(0, nGens):
            if self.verbose: print "g", i
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

        d = self.ms.evaluate_sensor_on_traces(traces, sp.parse_sensor(modelSensor))
        a = self.ms.evaluate_sensor_on_traces(traces, p.compile())

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


def gp_generate(domain_filename, domain_name, i, problem_filename, samples, popSize, nGens, planner_time_limit=0.0, max_length=0, sensor_depth=1):
    ss_stats = np.zeros((1, 9))  # Stats for the simple sensor
    cs_stats = np.zeros((1, 9))  # Stats for the complex sensor
    as_stats = np.zeros((1, 9))  # Stats for the action sensor
    pp = PDDL_Parser()
    pp.parse_domain(domain_filename)
    pp.parse_problem(problem_filename)
    pp.domain.groundify()
    print "Processing ", domain_filename

    traces = []
    print "Sampling {0} traces for domain {1}".format(samples, domain_filename)
    # traces = monitoring.monitor.sample_traces(domain_filename, samples, planner=Propositional_Planner(time_limit=planner_time_limit, max_length=max_length))
    for s in range(0,samples):
        traces.append(monitoring.monitor.sample_trace(pp.domain, planner=Propositional_Planner(time_limit=planner_time_limit, max_length=max_length)))
        # traces.append(monitoring.monitor.sample_trace_from_file(domain_filename,
        #                                               planner=Propositional_Planner(time_limit=planner_time_limit,
        #                                                                             max_length=max_length)))
	gc.collect()

    print "Generated {0} valid traces from a sample of {1}".format(len(traces), samples)

    simple_sensor = "({0} v {1})".format(pp.initial_state[1], pp.positive_goals[-1]).replace(",", "").replace("\'", "")
    print "Simple sensor: " + simple_sensor
    gp = GP(False)
    tpr, tnr, fpr, fnr = 0, 0, 0, 0
    tpr, tnr, fpr, fnr = gp.build_sensor(pp.domain, simple_sensor, traces, popSize, nGens, sensorDepth=sensor_depth)

    ss_stats[0] = [i,
                       len(pp.domain.all_facts),
                       len(pp.domain.actions),
                       len(pp.domain.state_space),
                       len(traces),
                       tpr, tnr, fpr, fnr]

    # Saving files in the middle of the loop in case of process kills
    print "Writing stats to ", domain_name + "-ss{0}.txt".format("%02d" % i)
    np.savetxt(domain_name + "-ss{0}.txt".format("%02d" % i), ss_stats,
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
    gp = GP(False)
    tpr, tnr, fpr, fnr = 0, 0, 0, 0
    tpr, tnr, fpr, fnr = gp.build_sensor(pp.domain, complex_sensor, traces, popSize, nGens, sensorDepth=sensor_depth)

    cs_stats[0] = [i,
                       len(pp.domain.all_facts),
                       len(pp.domain.actions),
                       len(pp.domain.state_space),
                       len(traces),
                       tpr, tnr, fpr, fnr]

    # Saving files in the middle of the loop in case of process kills
    print "Writing stats to ", domain_name + "-cs{0}.txt".format("%02d" % i)
    np.savetxt(domain_name + "-cs{0}.txt".format("%02d" % i), cs_stats,
               fmt='%d %d %d %d %d %.4f %.4f %.4f %.4f', delimiter=" ", newline="\n",
               header="Index, #Predicates, #Actions, #States, #Traces, TPR, TNR, FPR, FNR", footer="", comments="")

    action_sensor = sensor_for_action(plan[0])
    print "Action sensor: " + action_sensor
    gp = GP(False)
    tpr, tnr, fpr, fnr = 0, 0, 0, 0
    tpr, tnr, fpr, fnr = gp.build_sensor(pp.domain, action_sensor, traces, popSize, nGens, sensorDepth=sensor_depth)

    as_stats[0] = [i,
                   len(pp.domain.all_facts),
                   len(pp.domain.actions),
                   len(pp.domain.state_space),
                   len(traces),
                   tpr, tnr, fpr, fnr]

    # Saving files in the middle of the loop in case of process kills
    print "Writing stats to ", domain_name + "-as{0}.txt".format("%02d" % i)
    np.savetxt(domain_name + "-as{0}.txt".format("%02d" % i), as_stats,
               fmt='%d %d %d %d %d %.4f %.4f %.4f %.4f', delimiter=" ", newline="\n",
               header="Index, #Predicates, #Actions, #States, #Traces, TPR, TNR, FPR, FNR", footer="", comments="")

def main(argv): 
    experiments = 20
    samples = 200
    popSize = 100
    nGens = 100
    planner_time_limit = 0.02
    max_length = 10
    sensor_depth = 3

    domain_name = ''
    if len(argv) > 1:
        domain_name = str(argv[1])
        i = int(argv[2])
        domain_filename = 'examples/' + domain_name + '/domain-' + str(i) + '.pddl'
        problem_filename = 'examples/' + domain_name + '/task-' + str(i) + '.pddl'
        gp_generate(domain_filename, domain_name, i, problem_filename, samples, popSize, nGens, planner_time_limit, max_length, sensor_depth)
        exit(0)

    # ipreds,iactions,istate_space,traces, itpr,itnr,ifpr,ifnr = 1, 2, 3, 4, 5, 6, 7, 8
    ss_stats = np.zeros((experiments, 9))  # Stats for the simple sensor
    cs_stats = np.zeros((experiments, 9))  # Stats for the complex sensor

    skip = []
    # skip = [2,20]

    for i in range(1, experiments + 1):
        if i in skip: print "Skipping {0}".format(i); continue  # Skipping overlong domains
        domain_filename = 'examples/' + domain_name + '/domain-' + str(i) + '.pddl'
        problem_filename = 'examples/' + domain_name + '/task-' + str(i) + '.pddl'
        pp = PDDL_Parser()
        pp.parse_domain(domain_filename)
        pp.parse_problem(problem_filename)
        print "Processing ", domain_filename

        # if len(pp.domain.actions) > 20 : print "Skipping overlong domain"; continue
        if len(pp.domain.all_facts) > 20: print "Skipping overlong domain"; continue

        traces = []
        print "Sampling {0} traces for domain {1}".format(samples, domain_filename)
        traces = monitoring.monitor.sample_traces(domain_filename, samples, planner=Propositional_Planner(time_limit=planner_time_limit, max_length=max_length))
        print "Generated {0} valid traces from a sample of {1}".format(len(traces), samples)

        simple_sensor = "({0} v {1})".format(pp.initial_state[1], pp.positive_goals[-1]).replace(",", "").replace("\'",
                                                                                                                  "")
        print "Simple sensor: " + simple_sensor
        gp = GP(False)
        tpr, tnr, fpr, fnr = 0, 0, 0, 0
        tpr, tnr, fpr, fnr = gp.build_sensor(pp.domain, simple_sensor, traces, popSize, nGens, sensorDepth=sensor_depth)

        ss_stats[i - 1] = [i,
                           len(pp.domain.all_facts),
                           len(pp.domain.actions),
                           len(pp.domain.state_space),
                           len(traces),
                           tpr, tnr, fpr, fnr]

        # Saving files in the middle of the loop in case of process kills
        print "Writing stats to " + domain_name + "-ss.txt"
        np.savetxt(domain_name + "-ss.txt", ss_stats,
                   fmt='%d %d %d %d %d %.4f %.4f %.4f %.4f', delimiter=" ", newline="\n",
                   header="Index, #Predicates, #Actions, #States, #Traces, TPR, TNR, FPR, FNR", footer="", comments="")

        planner = Propositional_Planner()
        print "Solving sample problem for " + problem_filename
        plan = planner.solve(pp.domain, pp.initial_state, pp.goal)
        print "Plan length: ", len(plan)

        complex_sensor = "({0} [{2}] {1})".format(pp.initial_state[1], pp.positive_goals[-1], len(plan) + 1).replace(
            ",", "").replace("\'", "")
        print "Complex sensor: " + complex_sensor
        gp = GP(False)
        tpr, tnr, fpr, fnr = 0, 0, 0, 0
        tpr, tnr, fpr, fnr = gp.build_sensor(pp.domain, complex_sensor, traces, popSize, nGens, sensorDepth=sensor_depth)

        cs_stats[i - 1] = [i,
                           len(pp.domain.all_facts),
                           len(pp.domain.actions),
                           len(pp.domain.state_space),
                           len(traces),
                           tpr, tnr, fpr, fnr]

        # Saving files in the middle of the loop in case of process kills
        print "Writing stats to " + domain_name + "-cs.txt"
        np.savetxt(domain_name + "-cs.txt", cs_stats,
                   fmt='%d %d %d %d %d %.4f %.4f %.4f %.4f', delimiter=" ", newline="\n",
                   header="Index, #Predicates, #Actions, #States, #Traces, TPR, TNR, FPR, FNR", footer="", comments="")

if __name__ == '__main__':
    import sys
    main(sys.argv)

