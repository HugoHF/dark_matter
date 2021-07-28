import numpy as np
from hff import get_hff
from get_freqs import get_freqs
from create_data import create_data
from chisquared_stuff import get_significance
from autocorrelation import autocorrelation
import matplotlib.pyplot as plt
from scipy.fft import fftfreq

test_stds     = [0.001, 0.03, 0.1]
test_freqs    = np.arange(2, 100, 1)
time_interval = 0.001

detected_1 = []
detected_2 = []
detected_3 = []
detected   = [detected_1, detected_2, detected_3]

significance_1 = []
significance_2 = []
significance_3 = []
significance   = [significance_1, significance_2, significance_3]

for idx, test_freq in enumerate(test_freqs):
    for idx2, std in enumerate(test_stds):
        sig          = create_data(m_phi=test_freq * np.pi, deviation=std, time_interval=time_interval)
        # sig          = autocorrelation(sig, i=1) # uncomment this to do autocorrelation plus HFF
        idx, freq    = get_hff(sig)
        freqs_domain = fftfreq(len(sig[1]), time_interval)[:len(sig[1])//2]
        idx          = np.where(np.isclose(freqs_domain, freq / 2, atol=0.5))
        fhat, _, _   = get_freqs(sig, 0.5)
        prob         = get_significance(fhat, idx[0][0])

        detected[idx2].append(freq)
        significance[idx2].append(prob)

fig, ax = plt.subplots(2, 3)
fig.tight_layout(h_pad=2)    # figure spacing

for j in range(3):
    ax[0, j].plot(test_freqs, detected[j])
    ax[0, j].set_title(fr"Detected frequencies with $\sigma={test_stds[j]}$")
    ax[0, j].set_xlabel('Frequency of clean signal')
    ax[0, j].set_ylabel('Frequency detected with HFF')

for j in range(3):
    ax[1, j].plot(test_freqs, significance[j])
    ax[1, j].set_title(fr"Confidence of detected frequencies with $\sigma={test_stds[j]}$")
    ax[1, j].set_xlabel('Frequency of clean signal')
    ax[1, j].set_ylabel('Confidence of signal detected with HFF')

plt.show()