import pickle as pkl
import pandas as pd
import copy

line_template = "\multicolumn{ 1 }{ l }{\\begin{tabular}[l]{@{}l@{}}domain_instance\end{tabular}} \
                & \multicolumn{ 1 }{ l }{n_predicates} & \multicolumn{1}{l}{n_actions} \
                & gp_ss_accuracy\% & rl_ss_accuracy\% & gp_ss_tpr\% & rl_ss_tpr\% & gp_ss_f1score\% & rl_ss_f1score\% \
                && gp_cs_accuracy\% & rl_cs_accuracy\% & gp_cs_tpr\% & rl_cs_tpr\% & gp_cs_f1score\% & rl_cs_f1score\% \
                && gp_as_accuracy\% & rl_as_accuracy\% & gp_as_tpr\% & rl_as_tpr\% & gp_as_f1score\% & rl_as_f1score\% \\\\ "

with open('results.pkl', 'r+') as f:
    results = pkl.load(f)

tables = dict()
for domain in sorted(results.keys()):
    tables[domain] = list()
    for instance in sorted(results[domain].keys()):
        # Skip the ones without result
        if domain == 'barter-world' and instance == '03': continue
        if domain == 'tpp' and instance == '04': continue
        # Make a copy of line template
        line = copy.copy(line_template)
        # Replace values that are common for sensors and approaches
        if domain == 'barter-world': domain_name = 'BTW'
        elif domain == 'bridges': domain_name = 'BD'
        elif domain == 'psr-small': domain_name = 'PSR'
        elif domain == 'tpp': domain_name = 'TPP'
        line = line.replace('domain_instance', str(domain_name+"-"+instance.replace('0', '')))
        line = line.replace('n_predicates', str(int(results[domain][instance]['ss']['gp']['n_predicates'])))
        line = line.replace('n_actions', str(int(results[domain][instance]['ss']['gp']['n_actions'])))
        for sensor in sorted(results[domain][instance].keys()):
            for approach in sorted(results[domain][instance][sensor].keys(), reverse=True):
                for metric in results[domain][instance][sensor][approach].keys():
                    to_replace = "{0}_{1}_{2}".format(approach, sensor, metric.lower())
                    if to_replace in line: line = line.replace(to_replace, "%.2f"%results[domain][instance][sensor][approach][metric])
        tables[domain].append(line)

for domain in tables:
    with open('{0}-table-lines.tex'.format(domain), 'w+') as f:
        f.write("\n".join(tables[domain]))
