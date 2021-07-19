# Code adapted from: https://github.com/mmezache/HFFTest
# Based on the work by Mathieu Mezache, Marc Hoffmann, Human Rezaei, and Marie Doumic
# Mathieu Mezache, Marc Hoffmann, Human Rezaei, Marie Doumic. Testing for high frequency features in a noisy signal. 2019. ffhal-02263522v2f

import numpy as np
from scipy.fft import rfft, rfftfreq

def get_fft(signal, dt):
    """
    Computes the Fourier transform of a data signal. Only the first, real, half of the FT is computed and further manipulated.

    Parameters:
    -----------
        signal: np.array
            Signal in the following format: [domain, values]
        dt: int
            Interval between each sampling point

    Output:
    -------
        freq: np.array
            Frequencies corresponding to magnitudes
        mag: np.array
            Spectrum magnitude
    """
    n         = len(signal[0])
    noisy_fft = rfft(signal[1])
    freq      = rfftfreq(n, dt)
    mag       = np.abs(noisy_fft) * 2 / n # multiply by two since we removed the second half of spectrum and energy must be conserved
                                          # divide by n to normalize
    return freq, mag

def get_freq_ampl(domain, values):
    """
    Numerical procedure to get estimated amplitude of the data points and the most signficant frequency.
    The data passed into this function should have already go through a FT.
    
    Parameters:
    -----------
        domain: np.array
            Domain of the data to plot
        values: np.array
            Value for each point in domain
        
    Output:
    -------
        amplitude: float
            Estimated amplitude of the signal with removed noise
        frequency: float
            Frequency with the most significance found
    """
    n = len(domain)
    a = np.zeros((n,), dtype=int)
    b = np.zeros((n,), dtype=int)
    
    sorted_vals = values.copy() # create copy of unsorted data points
    sorted_vals.sort()          # sort the data points

    for i in range(n):
        a[i]  = np.where(values <= sorted_vals[i])[0][0]      # smallest index where values <= sorted_vals
        after = values[int(a[i]):]                            # slice values after the index above
        b[i]  = len(after) - np.argmax(after[::-1]) -1 + a[i] # index of the peak after index a[i]
    
    peaks   = np.unique(b)[1::] # indeces of all detected peaks, ommiting first peak from FT
    n_peaks = len(peaks)
    
    if n_peaks > 0:                                 # if peaks were detected
        index_freq = np.zeros((n_peaks,),dtype=int) # most relevant frequency/peak
        index_avg  = np.zeros((n_peaks,),dtype=int) # initialization min between trend and peak
        
        for i in range(n_peaks):
            index_freq[i] = peaks[i]
            index_avg[i]  = max(np.where(values == min(values[:int(index_freq[i])]))[0])
            
        rel_ampls = values[index_freq] - values[index_avg] # relative amplitudes
        amplitude = max(rel_ampls)                         # max of relative amplitudes; estimated amplitude of signal
        frequency = int(index_freq[np.argmax(rel_ampls)])  # most relevant frequency
        
    else:                                               
        raise Exception('No peaks detected in the data')
        
    return amplitude, frequency

def get_hff(signal, dt):
    """
    Estimates the frequency and amplitude of some data points using the High Frequency Features (HFF) detection method.
    Note: this procedure will only work when all the values in the signal are positive. Taking the absolute value of a signal with negative components
    also works, but some modification may need to be done to the frequency returned.

    Parameters:
    ------------
        signal: np.array
            Signal in the following format: [domain, values]
        dt: int
            Interval between each sampling point

    Output:
    -------
        amplitude: float
            Estimated amplitude of the signal with removed noise
        frequency: float
            Frequency with the most significance found
    """

    domain, mag = get_fft(np.array(signal), dt)
    ampl, freq  = get_freq_ampl(domain, mag)
    return ampl, freq