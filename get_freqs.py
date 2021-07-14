def get_freqs(signal, dt, threshold):
    """
    Returns the most significant frequencies found in noisy signal. 
    Using the data from create_data.py, the threshold needs to be low (~0.001) because of the amplitude factor.
    For normal trigonometric functions, the threshold can be higher (~100).
    
    Parameters:
    -----------
        signal: np.array
            Noisy signal
        dt: int
            Interval between each point of the domain
        threshold: int
            Magnitude threshold to get rid of noise frequencies
            
    Output:
    -------
        frequencies: np.array
            Array with most significant frequencise found
    """
    n    = len(signal)
    fhat = fft(signal)
    psd  = fhat * np.conj(fhat) / n
    freq = (1 / (dt * n)) * np.arange(n)
    L    = np.arange(0, np.floor(n/2), dtype='int') # half of the domain since we know FT is symmetric

    freqs = []
    for i in L:
        if psd[i] >= threshold:
            freqs.append(i)
            
    return np.array(freqs)
