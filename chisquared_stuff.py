import numpy as np
from scipy.stats import chi2
from scipy.special import binom


def get_significance(fourier, deviation):

    maximum = max(fourier)
    index_max = list(fourier).index(maximum)

    fourier_without_peak = np.delete(fourier, np.argwhere(fourier==maximum))


    real = np.real(fourier_without_peak)
    imag = np.imag(fourier_without_peak)

    std_total = (np.std(real) + np.std(imag))/2

    fourier_conj = np.conj(fourier)
    fourier2 = [np.real(fourier[i]*fourier_conj[i]) for i in range(len(fourier))]

    cdf_result = cdf_of_chi2(max(fourier2), deviation)

    #print("CDF", cdf_result, binom(len(fourier2),1)* cdf_result * ((1-cdf_result)**(len(fourier2) - 1)))
    '''
    IS THIS CORRECT?
    '''
    actual_probability = binom(len(fourier2),1)* cdf_result * ((1-cdf_result)**(len(fourier2) - 1))

    return cdf_result

def cdf_of_chi2(peak_height, sdt_x):
    # sdt_x is (std(Re[Fourier]) + std(Im[Fourier]))/2
    x = peak_height/(sdt_x**2)
    return chi2.cdf(x, 2)
    # returns P("peak of height peak_height is not a statistical error")
