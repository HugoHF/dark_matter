import numpy as np
import json
from whatever import whatever as func
import matplotlib.pyplot as plt

with open('testing_samples.json', r) as file:
    testing_samples = json.load(file)

domain, signals = testing_samples["domain"], testing_samples["signals"]

results = {"freqs":{"0":{"0":0}}, "errors":{"0":{"0":0}}}

for freq in signals.keys():
    results["freqs"][freq] = {"0":0}
    results["errors"][freq] = {"0":0}
    for stdev in signals[freq].keys():
        resulting_freqs, errors = 0, 0

        for i in range(3):
            resulting_freq, error = func(np.array(domain, signals[freq][stdev][i]))
            resulting_freqs += resulting_freq
            errors += error

        results["freqs"][freq][stdev], results["errors"][freq][stdev] = resulting_freqs/3, errors/3

fig, ax = plt.subplots(1,2)
ax[0].matshow(results["freqs"], label="output frequencies")
ax[0].set_xlabel("input frequencies")
ax[0].set_ylabel("standard deviations")

ax[1].matshow(results["errors"], label="significances")
ax[1].set_ylabel("input frequencies")
ax[1].set_ylabel("standard deviations")

ax[0].legend()
ax[1].legend()

plt.title("results for method _")
plt.tight_layout()
plt.show()
