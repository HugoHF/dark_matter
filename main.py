from create_data import create_data
from get_freqs import get_freqs
from autocorrelation import autocorrelation
import numpy as np
import matplotlib.pyplot as plt


#############################
# # # C O N S T A N T S # # #
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
use_noise=True              #Generating signal
i=1                         #Autocorrelation
threshold=0.5               #Dft and psd



#############################################
## calling subprograms one after the other ##
#############################################

##---------------------------##
##---- GENERATING SIGNAL ----##
##---------------------------##
signal = create_data(total_time=total_time, time_interval=time_interval, m_phi=m_phi, theta=theta, c_gamma=c_gamma, alpha=alpha, v=v, density=density,
                    c=c, h_bar=h_bar, mean=mean, deviation=deviation, use_noise=use_noise)

plt.plot(signal[0], signal[1])
plt.title("raw signal")
plt.ylabel("energy")
plt.xlabel("time")
plt.show()


##----------------------------##
##---- AUTOCORRELATING IT ----##
##----------------------------##
autocorrelated_signal = autocorrelation(signal, i=i)

plt.plot(autocorrelated_signal[0], autocorrelated_signal[1])
plt.title("signal after autocorrelation")
plt.ylabel("correlation")
plt.xlabel("shift amount [t]")
plt.show()


##---------------------------##
##---- FOURIER TRANSFORM ----##
##---------------------------##
psd, freqs = get_freqs(autocorrelated_signal, threshold)

fig, ax = plt.subplots(2,1)
ax[0].plot(np.arange(len(psd)), psd, label="power spectrum density")
ax[0].set_xlabel("this should be some frequencies, right? but scaled by what factor?")
ax[0].set_ylabel("amount")

ax[1].scatter(freqs, np.ones(len(freqs)), label="peaks")
ax[1].set_xlabel("frequency")

ax[0].legend()
ax[1].legend()
ax[0].set_title("dft results")

plt.show()
