import numpy as np
from hff import get_hff
from create_data import create_data
from chi_squared import get_prob

test_stds = np.arange(0.4, 0.5, 0.01)
freq      = 5

for std in test_stds:
    print(f"Error deviation: {std}")
    signal    = create_data(m_phi=np.pi * freq, deviation=std)
    idx, freq = get_hff(np.array(signal))
    print(f'Estimated frequency: {freq}') 
    get_prob(signal, idx)  
    print() # new line