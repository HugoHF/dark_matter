from scipy import signal
from ipynb.fs.full.create_data import create_data
import numpy as np
import matplotlib.pyplot as plt
rng = np.random.default_rng()
#############################
total_time=1                #Generating signal
time_interval=0.001         #Generating signal
m_phi=10                    #Generating signal
theta=1                     #Generating signal
c_gamma=1                   #Generating signal
alpha=1                     #Generating signal
v=1                         #Generating signal
density=1                   #Generating signal
c=1                         #Generating signal
h_bar=1                     #Generating signal
mean=0                      #Generating signal
deviation=0.001             #Generating signal
use_noise=False             #Generating signal
i=1                         #Autocorrelation
threshold=0.5               #Dft and psd
K  = np.sqrt((2 * density) / c**2)
omega  = ((m_phi * (c**2)) / h_bar)
first   = ((np.sin(theta) / v) - ((2 * c_gamma * (alpha ** 2) * np.sin(theta)) / (np.pi * v)))
func = lambda t: first * ((K / omega) * np.cos(omega * t) ** 2)
data = []
for i in range(0,1024):
    data.append(func(i/1024))
sig_noise = data + rng.standard_normal(len(data))
sig = np.repeat([0., 1., 1., 0., 1., 0., 0., 1.], 128)
# print(data[np.arange(0, 1024, 100)])
corr = signal.correlate(sig_noise, data, mode='same') / 1024
clock = np.arange(64, 1024, 128)
fig, (ax_orig, ax_noise, ax_corr) = plt.subplots(3, 1, sharex=True)
ax_orig.plot(data)
# ax_orig.plot(clock, sig[clock], 'ro')
ax_orig.set_title('Original signal')
ax_noise.plot(sig_noise)
ax_noise.set_title('Signal with noise')
ax_corr.plot(corr)
ax_corr.plot(clock, corr[clock], 'ro')
ax_corr.axhline(0.5, ls=':')
ax_corr.set_title('Cross-correlated with rectangular pulse')
ax_orig.margins(0, 0.1)
fig.tight_layout()
plt.show()
sig = data
corr = signal.correlate(sig_noise, sig)
lags = signal.correlation_lags(len(sig), len(sig_noise))
corr /= np.max(corr)
fig, (ax_orig, ax_noise, ax_corr) = plt.subplots(3, 1, figsize=(4.8, 4.8))
ax_orig.plot(sig)
ax_orig.set_title('Original signal')
ax_orig.set_xlabel('Sample Number')
ax_noise.plot(sig_noise)
ax_noise.set_title('Signal with noise')
ax_noise.set_xlabel('Sample Number')
ax_corr.plot(lags, corr)
ax_corr.set_title('Cross-correlated signal')
ax_corr.set_xlabel('Lag')
ax_orig.margins(0, 0.1)
ax_noise.margins(0, 0.1)
ax_corr.margins(0, 0.1)
fig.tight_layout()
plt.show()
# ax_orig.plot(clock, sig[clock], 'ro')
ax_orig.set_title('Original signal')
ax_noise.plot(sig_noise)
ax_noise.set_title('Signal with noise')
ax_corr.plot(corr)
ax_corr.plot(clock, corr[clock], 'ro')
ax_corr.axhline(0.5, ls=':')
ax_corr.set_title('Cross-correlated with rectangular pulse')
ax_orig.margins(0, 0.1)
fig.tight_layout()
plt.show()
sig = data
corr = signal.correlate(sig_noise, sig)
lags = signal.correlation_lags(len(sig), len(sig_noise))
corr /= np.max(corr)
fig, (ax_orig, ax_noise, ax_corr) = plt.subplots(3, 1, figsize=(4.8, 4.8))
ax_orig.plot(sig)
ax_orig.set_title('Original signal')
ax_orig.set_xlabel('Sample Number')
ax_noise.plot(sig_noise)
ax_noise.set_title('Signal with noise')
ax_noise.set_xlabel('Sample Number')
ax_corr.plot(lags, corr)
ax_corr.set_title('Cross-correlated signal')
ax_corr.set_xlabel('Lag')
ax_orig.margins(0, 0.1)
ax_noise.margins(0, 0.1)
ax_corr.margins(0, 0.1)
fig.tight_layout()
plt.show()
