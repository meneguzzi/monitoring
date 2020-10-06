import pickle as pkl
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


""" ATTENTION!

    If you are facing an error "ImportError: cannot import name Sensor" while reading files,
    comment line "from structures.sensor import Sensor" in file "structures/domain.py".
"""

approaches = ['gp', 'rl']
domains = ['barter-world', 'bridges', 'psr-small', 'tpp']
instances = ['01', '02', '03', '04', '05']
sensors = ['ss', 'cs', 'as']
results = dict()

for domain in domains:
    results[domain] = dict()
    for instance in instances:
        results[domain][instance] = dict()
        for sensor in sensors:
            results[domain][instance][sensor] = dict()
            for approach in approaches:
                results[domain][instance][sensor][approach] = dict()
                directory = '{0}/output/'.format(approach)
                filename_history = '{0}-{1}{2}-history.pkl'.format(domain, sensor, instance)
                filename_stats = '{0}-{1}{2}.txt'.format(domain, sensor, instance)
                path_history = directory + filename_history
                path_stats = directory + filename_stats
                try:
                    with open(path_history, 'r') as f:
                        history = pkl.load(f)
                    results[domain][instance][sensor][approach]["history"] = [v for v, s in history]
                except:
                    print("File {0} does not exist.".format(path_history))
                try:
                    with open(path_stats, 'r') as f:
                        stats = pd.read_csv(f, sep=' ')
                    # Compute metrics
                    tpr = stats["TPR,"][0]
                    tnr = stats["TNR,"][0]
                    fpr = stats["FPR,"][0]
                    fnr = stats["FNR"][0]
                    accuracy = (tpr+tnr)/(tpr+tnr+fpr+fnr)
                    precision = (tpr)/(tpr+fpr)
                    recall = (tpr)/(tpr+fnr)
                    f1score = (2*precision*recall)/(precision+recall)
                    # Store in dictionary
                    results[domain][instance][sensor][approach]["n_predicates"] = stats["#Predicates,"][0]
                    results[domain][instance][sensor][approach]["n_actions"] = stats["#Actions,"][0]
                    results[domain][instance][sensor][approach]["n_states"] = stats["#States,"][0]
                    results[domain][instance][sensor][approach]["n_traces"] = stats["#Traces,"][0]
                    results[domain][instance][sensor][approach]["TPR"] = tpr
                    results[domain][instance][sensor][approach]["TNR"] = tnr
                    results[domain][instance][sensor][approach]["FPR"] = fpr
                    results[domain][instance][sensor][approach]["FNR"] = fnr
                    results[domain][instance][sensor][approach]["accuracy"] = accuracy
                    results[domain][instance][sensor][approach]["precision"] = precision
                    results[domain][instance][sensor][approach]["recall"] = recall
                    results[domain][instance][sensor][approach]["f1score"] = f1score
                except:
                    print("File {0} does not exist.".format(path_stats))

with open('results.pkl', 'w+') as f:
    pkl.dump(results, f)
