import numpy as np
from create_data import create_data
from hff import get_hff
import matplotlib.pyplot as plt

error_std  = [0, 0.01, 0.02, 0.03, 0.04, 0.05]
test_freqs = np.arange(2, 100, 1)

fig, ax = plt.subplots(6, figsize=(15, 40))

for i, err_std in enumerate(error_std):
    real_freqs     = []
    detected_freqs = []

    for test_freq in test_freqs:
        signal    = create_data(m_phi = np.pi * test_freq, deviation=err_std, total_time=1, time_interval=0.001, simple=True)
        idx, freq = get_hff(signal)

        real_freqs.append(test_freq)
        detected_freqs.append(freq)

    ax[i].set_title(f'Error deviation: {err_std}')
    ax[i].scatter(real_freqs, detected_freqs)

for a in ax.flat:
    a.set(xlabel='Real frequencies', ylabel='HFF detected frequencies')

# fig.savefig('fig.png')
plt.show()