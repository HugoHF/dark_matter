import numpy as np
from hff import get_hff
from get_freqs import get_freqs
from create_data import create_data
from chisquared_stuff import get_significance
from chi_squared import get_prob
import csv
from scipy import signal
test_stds     = np.arange(0, 0.5, 0.01)
test_freqs    = np.arange(2, 100, 0.5)
time_interval = 0.001
total_time  = 1
csv_freqs = []
csv_ampl  = []
csv_std   = []
csv_dfreq = []
csv_prob  = []
csv_unc   = []

for test_freq in test_freqs:
    for std in test_stds:
        print(f"{test_freq} with {std}")
        amp       = (3 * np.sqrt(2)) / (test_freq * np.pi)  # calculate amplitude of functin with default values
        sig,sig1    = create_data(m_phi=test_freq * np.pi, deviation=std, time_interval=time_interval)
        corr = signal.correlate(sig, sig1, mode='full', method='fft')
        domain     = np.arange(0, total_time, time_interval)
        corr1 = np.array([domain,corr])
        try:        
            idx, freq = get_hff(corr)
            if idx % 2 == 0:
                idx = idx // 2 # again, idk why this is but my guess is that it is because i take the real fft in hff
                
            fhat, _, _ = get_freqs(signal, 0.5)
            prob       = get_significance(fhat, idx)
            unc        = np.sqrt((prob * (1 - prob)) / len(fhat)) 

            # Previous method
            # prob, unc = get_prob(signal, idx)
        
        except Exception:
            freq = -1
            prob = -1
            unc  = -1

        csv_freqs.append(test_freq)
        csv_ampl.append(amp)
        csv_std.append(std)
        csv_dfreq.append(freq)
        csv_prob.append(prob)
        csv_unc.append(unc)

with open('general_tests_cross_correlation.csv', mode='w') as test_results:
    writer = csv.writer(test_results, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    writer.writerow(['Real frequency', 'Amplitude', 'Error deviation', 'Detected frequency', 'Chi2 prob', 'Uncertainty'])
    for i in range(len(csv_freqs)):
        writer.writerow([csv_freqs[i], csv_ampl[i], csv_std[i], csv_dfreq[i], csv_prob[i], csv_unc[i]])
