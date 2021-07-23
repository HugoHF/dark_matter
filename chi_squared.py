import numpy as np
from scipy.fft import fft
from scipy.stats import chi2
import matplotlib.pyplot as plt

def get_prob(signal, idx, plot=False):
    if idx % 2 == 0:
        idx = idx // 2          # for some weird reason, we have to divide by two if the detected frequency is even

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

    if plot:
        cdf_array=[]
        
        for i in range(len(transform)): 
            temp_amp = transform[i]
            temp     = np.abs(temp_amp) * 2 /avg_std
            temp_cdf = chi2.cdf(temp,2)
            cdf_array.append(temp_cdf)
        
        plt.plot(cdf_array)
        plt.show()

    return chi