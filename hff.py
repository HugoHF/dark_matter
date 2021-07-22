# Code adapted from: https://github.com/mmezache/HFFTest
# Based on the work by Mathieu Mezache, Marc Hoffmann, Human Rezaei, and Marie Doumic
# Mathieu Mezache, Marc Hoffmann, Human Rezaei, Marie Doumic. Testing for high frequency features in a noisy signal. 2019. ffhal-02263522v2f

import numpy as np
from numpy import linalg as LA

def get_fft(y, dt):
    """
    Computes the Fourier transform of a data signal. Only the first, real, half of the FT is computed and further manipulated.

    Parameters:
    -----------
        y: np.array
            Array with the value of the points in the signal
        dt: int
            Interval between each sampling point

    Output:
    -------
        rfreqs: np.array
            Frequencies corresponding to magnitudes
        fft_mag: np.array
            Spectrum magnitude
    """
    n  = len(y)                         # Get the signal length

    fft_output = np.fft.rfft(y)         # Perform real fft
    rfreqs     = np.fft.rfftfreq(n, dt) # Calculate frequency bins
    fft_mag    = np.abs(fft_output)     # Take only magnitude of spectrum

    # Normalize the amplitude by number of bins and multiply by 2
    # because we removed second half of spectrum and energy must be preserved
    fft_mag = fft_mag * 2 / n           

    return rfreqs, fft_mag

def smooth_fft(f, amp, delta=1):
    """
    Compute the L2 norm of the Fourier transform of a signal on specifics bandwidth

    Parameters:
    -----------
        f: np.array
            Frequencies array, which is left unmodified
        amp: np.array
            Array with frequencies amplitudes

    Output:
    -------
        f: np.array
            Same frequency array as the input
        ampl: np.array
            Smoothed out frequencies amplitudes
    """
    ampl = np.zeros((len(amp), 1))
    for i in range(len(amp)):
        if i > delta // 2 and i < (len(amp) - delta // 2):
            if delta <= 1:
                ampl[i] = amp[i]
            else:
                ampl[i] = LA.norm(amp[(i - delta // 2):(i + delta // 2)], 2) / np.sqrt(delta)
        elif(i <= delta // 2):
            ampl[i] = LA.norm(amp[:delta], 2) / np.sqrt(delta)
        if (i >= len(amp) - delta // 2):
            ampl[i] = LA.norm(amp[len(amp) - delta:len(amp)], 2) / np.sqrt(delta)
    return f, ampl

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
        frequency: int
            Index of the frequency with the most significance found
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
        frequency = int(index_freq[np.argmax(rel_ampls)])  # most relevant frequency
        
    else:                                               
        raise Exception('No peaks detected in the data')
        
    return frequency

def get_hff(signal, delta = 1):
    """
    Estimates the frequency and amplitude of some data points using the High Frequency Features (HFF) detection method.
    Note: this procedure will only work when all the values in the signal are positive. Taking the absolute value of a signal with negative components
    also works, but some modification may need to be done to the frequency returned.

    Parameters:
    ------------
        signal: np.array
            Signal in the following format: [domain, values]
        delta: int
            Function smoothing parameter

    Output:
    -------
        idx: int
            Index of the most significant frequency
        frequency: float
            Frequency with the most significance found
    """
    x = signal[0]    # get signal domain
    y = signal[1]**2 # get signal data values squared

    dt      = x[int(len(x) / 2)] - x[int(len(x) / 2 - 1)]
    f, amp  = get_fft(y, dt)
    f, amps = smooth_fft(f, amp, delta) 
    idx     = get_freq_ampl(f, np.power(amps, 2))
    return idx, f[idx]