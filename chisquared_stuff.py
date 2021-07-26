import numpy as np
from scipy.stats import chi2
from scipy.special import binom
import matplotlib.pyplot as plt
from decimal import Decimal

def get_significance(fourier, index_freq, plot=False):

    fourier_without_peak = np.delete(fourier, np.argwhere(fourier==fourier[index_freq]))


    real = np.real(fourier_without_peak)
    imag = np.imag(fourier_without_peak)

    std_total = (np.std(real) + np.std(imag))/2

    fourier_conj = np.conj(fourier)
    fourier2 = [np.real(fourier[i]*fourier_conj[i]) for i in range(len(fourier))]

    cdf_result = cdf_of_chi2(fourier2[index_freq], std_total**2)

    actual_probability =  cdf_result**(len(fourier2))

    if plot:
        cdf_array  = []
        domain_arr = []
        
        for i in range(len(fourier2)): 
            cdf_result = cdf_of_chi2(fourier2[i], std_total**2)
            cdf_array.append(cdf_result)
            domain_arr.append(i)
        
        plt.plot(domain_arr, cdf_array)
        plt.xlabel('Frequency')
        plt.ylabel('Significance')
        plt.title(r'Chi$^2$ function')
        plt.show()

    return actual_probability

def cdf_of_chi2(peak_height, sdt_x):
    # sdt_x is (std(Re[Fourier]) + std(Im[Fourier]))/2
    x = peak_height/sdt_x
    return chi2.cdf(x, 2)
    # returns P("peak of height peak_height is not a statistical error")
