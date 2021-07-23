import numpy as np
from scipy.fft import fft
from scipy.stats import chi2

def get_prob(signal, idx):
    transform  = fft(signal[1])
    peak_value = transform[idx]

    real_std  = np.std(np.real(transform))
    imag_std  = np.std(np.imag(transform))
    avg_std   = (real_std + imag_std) / 2

    print(f"Real std: {real_std}. Imag std: {imag_std}")

    dof = 2
    x   = (np.abs(peak_value) ** 2) / (avg_std ** 2)
    chi =  chi2.cdf(x, 2)
    print(f"Prob: {chi}")