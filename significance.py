import numpy as np

def get_significance(values, index):
    """
    Calculates the significance of the given frequency in the Fourier transform given in values
    This is calculated by taking the proportion of the peak with the first (default) peak, which is 2 for data without noise, and
    then subtracting. The closer to 0, the more significant the frequency is. 

    Parameters:
    -----------
        domain: np.array
            Domain of the fourier transform
        values: np.array
            Value for data points of the fourier transform
        index: int
            Index of frequency for which you want the significance

    Output:
    -------
        significance: float
            Float indicating the significance of the indicated frequency in the data
    """
    return ((values[0] / values[index]) / 2) - 1