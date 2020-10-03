import monitoring.monitor
from structures.sensor import Sensor
from pddl.PDDL import PDDL_Parser
from pddl.propositional_planner import Propositional_Planner
import os
import pickle

def main(): 
    num_traces = 1000
    num_terms = 15
    planner_time_limit = 0.02
    max_length = 10
    sensor_depth = 3

    domain_names = ['tpp']  #['barter-world', 'bridges', 'psr-small', 'tpp']
    instances = [3,4,5]  #[1, 2, 3, 4, 5]

    # Iterate each domain and problem
    for domain_name in domain_names:
        for instance in instances:
            domain_filename = os.path.join('examples', domain_name, 'domain-' + str(instance) + '.pddl')
            problem_filename = os.path.join('examples', domain_name, 'task-' + str(instance) + '.pddl')
            
            # Prepare folder to save files
            dump_folder = os.path.join('resources', domain_name + '-' + str(instance))
            if not os.path.exists(dump_folder): os.makedirs(dump_folder)

            # Parse domain and problem
            print("Processing", domain_filename)
            pp = PDDL_Parser()
            pp.parse_domain(domain_filename)
            pp.parse_problem(problem_filename)
            pp.domain.groundify()
            
            # Sample traces
            print("Sampling {0} traces for domain {1}".format(num_traces, domain_filename))
            traces = []
            for _ in range(0, num_traces):
                traces.append(monitoring.monitor.sample_trace(pp.domain, planner=Propositional_Planner(time_limit=planner_time_limit, max_length=max_length)))

            # Dump traces to file
            traces_file = os.path.join(dump_folder, 'traces.json')
            print("Dumping traces to file {0}".format(traces_file))
            with open(traces_file, 'w+') as f: pickle.dump(traces, f)

            # Sample terms
            print("Sampling {0} terms for domain {1}".format(num_terms, domain_filename))
            terms = []
            for _ in range(0, num_terms):
                terms.append(Sensor.generate_sensor(pp.domain, sensor_depth))
            
            # Dump terms to file
            terms_file = os.path.join(dump_folder, 'terms.json')
            print("Dumping terms to file {0}".format(terms_file))
            with open(terms_file, 'w+') as f: pickle.dump(terms, f)



if __name__ == '__main__':
    main()
