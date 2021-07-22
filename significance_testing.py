from significance import get_significance
from hff import get_hff, get_fft
from create_data import create_data 
import numpy as np

# Variables to vary the value of density in the data function
# To leave the density constant set the variables to 1, 2,1
d_start = 1
d_end   = 2
d_inter = 1

# Variables to vary the frequency of the data function
f_start = 2
f_end   = 10
f_inter = 1

time_interval = 0.001 
total_time    = 1
deviation     = 0.01

for i in np.arange(f_start, f_end, f_inter):
    for j in np.arange(d_start, d_end, d_inter):
        signal       = create_data(m_phi = i * np.pi, density = j, use_noise=True, deviation=deviation, time_interval=time_interval, total_time=total_time)
        idx, freq    = get_hff(signal) 
        dom, ran     = get_fft(signal[1] ** 2, time_interval)
        significance = get_significance(ran, idx)

        print(f'Calculated significance of frequency {freq}: {significance}')