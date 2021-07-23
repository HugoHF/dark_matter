import numpy as np
from scipy.fft import fft
from scipy.stats import chi2

def get_prob(signal, idx):
    transform  = fft(signal[1]) # gets the FT of the values of the signal
    peak_value = transform[idx] # gets the FT coefficient for the detected frequency found by HFF

    real_std  = np.std(np.real(transform))
    imag_std  = np.std(np.imag(transform))
    avg_std   = (real_std + imag_std) / 2  # calculate deviation of real and imaginary part of the Ft and average them

    print(f"Real std: {real_std}. Imag std: {imag_std}")

    dof = 2
    x   = (np.abs(peak_value) ** 2) / (avg_std ** 2)
    chi =  chi2.cdf(x, dof)
    print(f"Prob: {chi}")