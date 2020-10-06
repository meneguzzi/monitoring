import pickle as pkl
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams.update({'font.size': 10})


with open('results.pkl', 'r+') as f:
    results = pkl.load(f)

for domain in results.keys():
    total_instances = len(list(results[domain].keys()))
    total_sensors = 3
    # Initialize plot
    fig, plots = plt.subplots(total_instances, total_sensors, constrained_layout=True, figsize=(25, 15))
    for i, instance in enumerate(sorted(results[domain].keys())):
        for s, sensor in enumerate(sorted(results[domain][instance].keys(), reverse=True)):
            # Skip the ones without result
            if domain == 'barter-world' and instance == '03': 
                plots[i][s].plot([0])
            elif domain == 'tpp' and instance == '04': 
                plots[i][s].plot([0])
            else:
                plots[i][s].plot(pd.rolling_mean(pd.DataFrame(results[domain][instance][sensor]["gp"]["history"]), window=25), label="GP")
                plots[i][s].plot(pd.rolling_mean(pd.DataFrame(results[domain][instance][sensor]["rl"]["history"]), window=25), label="RL")
            plots[i][s].set_ylabel("Score (TP+TN-FP-FN)")
            plots[i][s].set_xlabel("Explored sensors")
            plots[i][s].set_title(str(domain).upper()+'-'+str(instance)+' '+sensor.upper())
            plots[i][s].legend()
    # plt.show()
    plt.savefig("{0}-plot.pdf".format(domain))
    plt.close()
