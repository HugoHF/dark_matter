import numpy as np
from hff import get_hff
from create_data import create_data
from chi_squared import get_prob
import csv

test_stds  = np.arange(0, 0.6, 0.01)
test_freqs = np.arange(2, 1000, 1)

csv_freqs = []
csv_ampl  = []
csv_std   = []
csv_dfreq = []
csv_prob  = []

for test_freq in test_freqs:
    for std in test_stds:
        amp       = (3 * np.sqrt(2)) / (test_freq * np.pi)  # calculate amplitude of functin with default values
        signal    = create_data(m_phi=test_freq * np.pi, deviation=std)
        try:
            idx, freq = get_hff(signal)
            prob      = get_prob(signal, idx)
        except Exception:
            freq = -1
            prob = -1

        csv_freqs.append(test_freq)
        csv_ampl.append(amp)
        csv_std.append(std)
        csv_dfreq.append(freq)
        csv_prob.append(prob)

with open('general_tests.csv', mode='w') as test_results:
    writer = csv.writer(test_results, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    writer.writerow(['Real frequency', 'Amplitude', 'Error deviation', 'Detected frequency', 'Chi2 probability'])
    for i in range(len(csv_freqs)):
        writer.writerow([csv_freqs[i], csv_ampl[i], csv_std[i], csv_dfreq[i], csv_prob[i]])