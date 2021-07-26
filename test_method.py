import json

from main import method_2 as func # PUT IN HERE THE CORRECT METHOD

from mpl_toolkits import mplot3d
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

np.seterr(all="ignore")

X, Y = [], []

with open('test_samples.json', "r") as file:
    testing_samples = json.load(file)

domain, signals = testing_samples["domain"], testing_samples["signals"]

results = {"freqs":{"0.0":{"0.0":0}}, "errors":{"0.0":{"0.0":0}}}

for freq in signals.keys():
    results["freqs"][freq] = {"0":0}
    results["errors"][freq] = {"0":0}
    for stdev in signals[freq].keys():
        resulting_freqs, errors = 0, 0

        for i in range(3):
            resulting_freq, error = func(np.array([domain, signals[freq][stdev][str(i)]]))
            resulting_freqs += resulting_freq
            errors += error

        results["freqs"][freq][stdev], results["errors"][freq][stdev] = resulting_freqs/3, errors/3


freq_mat = np.array([np.array([results["freqs"][frequency][deviation] for deviation in results["freqs"][frequency].keys()]) for frequency in results["freqs"].keys()])
error_mat = np.array([np.array([results["errors"][frequency][deviation] for deviation in results["errors"][frequency].keys()]) for frequency in results["errors"].keys()])

X, Y = list(results["freqs"].keys()), list(results["freqs"]["0.0"].keys())
X, Y = [float(i) for i in X], [float(i) for i in Y]
# Make matrices
X, Y = np.array([X for i in range(len(Y))]), np.array([Y for i in range(len(X))])
X = X.T

fig = plt.figure()
ax = fig.gca(projection='3d')
fig.tight_layout()
# X = np.tile(X, len(Y))
# Y = np.tile(Y, len(X))

ax.plot_wireframe(X,Y,error_mat)

ax.set_xlabel("original frequencies")
ax.set_ylabel("original error deviations")
ax.set_zlabel("calculated significance")
plt.show()

fig = plt.figure()
ax = fig.gca(projection='3d')
fig.tight_layout()
# X = np.tile(X, len(Y))
# Y = np.tile(Y, len(X))

ax.plot_wireframe(X,Y,freq_mat)

ax.set_xlabel("original frequencies")
ax.set_ylabel("original error deviations")
ax.set_zlabel("calculated frequencies")
plt.show()

# fig, ax = plt.subplots(1,2)
#
# ax[0].matshow(freq_mat, label="output frequencies")
# ax[0].set_xlabel("input frequencies")
# ax[0].set_ylabel("standard deviations")
#
# ax[1].matshow(error_mat, label="significances")
# ax[1].set_xlabel("input frequencies")
# ax[1].set_ylabel("standard deviations")
#
# ax[0].legend()
# ax[1].legend()
#
# cmaps = ['RdBu_r', 'viridis']
# pcm = ax[0].pcolormesh(freq_mat, cmap=cmaps[0])
# fig.colorbar(pcm, ax=ax[0])
# pcm = ax[1].pcolormesh(freq_mat, cmap=cmaps[1])
# fig.colorbar(pcm, ax=ax[1])
#
# # for col in range(2):
# #     for row in range(2):
# #         ax = axs[row, col]
#
#
# fig.suptitle("results for method _")
# plt.tight_layout()
# plt.show()
