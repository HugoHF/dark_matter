from create_data import create_data
from get_freqs import get_freqs
from autocorrelation import autocorrelation
from hff import get_hff, get_fft, smooth_fft
# from significance import get_significance
from chisquared_stuff import get_significance
import numpy as np
import matplotlib.pyplot as plt

#############################
# # # C O N S T A N T S # # #
#############################
total_time    = 1           # Generating signal
time_interval = 0.001       # Generating signal
m_phi         = 10 * np.pi   # Generating signal
m_e           = 1           # Generating signal
g_gamma       = 1           # Generating signal
g_e           = 1           # Generating signal
alpha         = 1           # Generating signal
density       = 1           # Generating signal
c             = 1           # Generating signal
h_bar         = 1           # Generating signal
mean          = 0           # Generating signal
deviation     = 0.01         # Generating signal
use_noise     = True        # Generating signal
i             = 1           # Autocorrelation
threshold     = 0.5         # Dft and psd

##---------------------------##
##------ CHOOSE METHOD ------##
##---------------------------##
method = 1                  # Run method 1 or 2
                            # Method 1: Correlate noisy function and apply FT
                            # Method 2: High Frequency Features (HFF) detection method

##---------------------------##
##---- GENERATING SIGNAL ----##
##---------------------------##
signal = create_data(total_time=total_time, time_interval=time_interval, m_phi=m_phi, m_e=m_e, g_gamma=g_gamma, g_e=g_e, alpha=alpha, density=density,
                    c=c, h_bar=h_bar, mean=mean, deviation=deviation, use_noise=use_noise)

plt.plot(signal[0], signal[1])
plt.title("Raw signal")
plt.ylabel("Energy")
plt.xlabel("Time")
plt.show()

if method == 1:
    ##----------------------------##
    ##---- AUTOCORRELATING IT ----##
    ##----------------------------##
    autocorrelated_signal = autocorrelation(signal, i=i)

    plt.plot(autocorrelated_signal[0], autocorrelated_signal[1])
    plt.title("Signal after autocorrelation")
    plt.ylabel("Correlation")
    plt.xlabel("Shift amount [t]")
    plt.show()

    ##---------------------------##
    ##---- FOURIER TRANSFORM ----##
    ##---------------------------##
    fhat, psd, freqs = get_freqs(signal, threshold)

    fig, ax = plt.subplots(2,1)
    ax[0].plot(np.arange(len(fhat)), fhat, label="Power spectrum density")
    ax[0].set_xlabel("Frequency")
    ax[0].set_ylabel("Magnitude")

    ax[1].scatter(freqs, np.ones(len(freqs)), label="peaks")
    ax[1].set_xlabel("Frequency")

    ax[0].legend()
    ax[1].legend()
    ax[0].set_title("Dft results")

    plt.show()

    fourier_conj = np.conj(fhat)
    fourier2 = [np.real(fhat[i]*fourier_conj[i]) for i in range(len(fhat))]

    plt.plot(np.arange(len(fourier2)), fourier2)
    plt.title("fourier^2")
    plt.show()

    significance = get_significance(fhat, deviation)

elif method == 2:
    idx, freq = get_hff(np.array(signal))

    print(f'Estimated frequency: {freq}')

    f, amp   = get_fft(signal[1]**2, time_interval)
    dom, ran = smooth_fft(f, amp)

    fig, ax = plt.subplots(1)
    ax.plot(dom, ran)
    ax.plot(dom[idx], ran[idx], 'bD')            # plot blue square corresponding to most significant frequency peak
    ax.set_yscale('log')
    ax.set_xlabel('Freq')
    ax.set_ylabel('FT coefficient')
    ax.set_title("Detected frequencies with HFF")

    # significance = get_significance(ran, idx)
    # print(f'Significance of frequency {freq}: {significance}')

    plt.show()
