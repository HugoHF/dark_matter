import statsmodels.api as sm
import numpy as np

def autocorrelation(signal, i=1):
    ''' Here signal will be autocorrelated i times.
        input:
            signal:
                np.array([domain, noisy signal])
            i:
                int (or float)
        output:
            np.array([domain, signal autocorrelated i times])

        Always autocorrelates at least 1 time, even with i == 0 or i < 0.
    '''
    
    domain, signal = signal

    h = 1

    def autocorrelate(signal, h):
        autocorrelated_signal = sm.tsa.acf(signal, nlags=len(signal))
        if h<i:
            h+=1
            return autocorrelate(autocorrelated_signal, h)
        return autocorrelated_signal, h

    autocorrelated_signal, h  = autocorrelate(signal, h)

    return np.array([domain, autocorrelated_signal])
