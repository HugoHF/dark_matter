import numpy as np
from scipy.stats import chi2
from scipy.special import binom
from decimal import Decimal

def get_significance(fourier, index_freq):

    fourier_without_peak = np.delete(fourier, np.argwhere(fourier==fourier[freq]))


    real = np.real(fourier_without_peak)
    imag = np.imag(fourier_without_peak)

    std_total = (np.std(real) + np.std(imag))/2

    fourier_conj = np.conj(fourier)
    fourier2 = [np.real(fourier[i]*fourier_conj[i]) for i in range(len(fourier))]

    cdf_result = cdf_of_chi2(fourier2[freq], std_total**2)


    actual_probability =  cdf_result**(len(fourier2))
    return actual_probability

def cdf_of_chi2(peak_height, sdt_x):
    # sdt_x is (std(Re[Fourier]) + std(Im[Fourier]))/2
    x = peak_height/sdt_x
    return chi2.cdf(x, 2)
    # returns P("peak of height peak_height is not a statistical error")
