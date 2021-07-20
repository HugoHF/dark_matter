# Measuring significance
Running some tests, I found out a relationship between the first peak of the Fourier transform, i.e. the peak we ignore for further, and the detected most significant peak. The relationship is: `first peak / significant peak = 2`.

Varying `density` between 0.001 and 0.1 with 0.001 intervals to test the relation holds with small amplitudes, as this is the type of data we expect from experiments. I also tested it by varying the same variable between 1 and 100, 500 and 600 to make sure the relation holds with biger amplitudes.

The edge case I found was when `m_phi = np.pi`, in which case also the HFF function breaks down and detects 250 as the most significant frequency. There is also an error when `m_phi = 0`, however, this happens because this value for `m_phi` provokes division by zero when creating the data. (Note that no noise is being introduced for this test.)

The function to test this is the following:

```python
# Variables to vary the value of density in the data function
d_start = 1
d_end   = 10
d_inter = 1

# Variables to vary the frequency of the data function
f_start = 2
f_end   = 10
f_inter = 1

time_interval = 0.001 
total_time    = 1
deviation     = 0

for i in np.arange(f_start, f_end, f_inter):
    for j in np.arange(d_start, d_end, d_inter):
        signal = create_data(m_phi = i * np.pi, density = j, use_noise=False, deviation=deviation, time_interval=time_interval, total_time=total_time)
        ampl, freq = get_hff(signal, time_interval) 
        dom, ran = get_fft(signal, time_interval)
        significance = get_significance(ran, freq)
        print(ran[0] / ran[freq])
```

Running this, we get 2 (or something like 2.0000000000000004 and 1.9999999999999996) every time. Therefore, it is safe to assume that the proportion is equal to 2 when there is no noise in the signal.

## Defining the significance function
To define the significance function, I used the fact that ideally (without noise), `first peak / significant peak = 2`. Taking this as a base, we can define the cost function as `((first peak / significant peak) / 2) - 1`. The first term checks the proportion of `first peak / significant peak` from the noisy data with the ideal one. Then, I subtract one to make the value when there is no noise equal to 0 and therefore the function is centered around 0. 

To test the function, I created data with different frequencies (2 through) and noise deviations to see how well the function represents the significance of the frequency. The code to get the results presented below is the same as the above but with the last line replaced with:
```python
significance = get_significance(ran, freq)
print(f'Calculated significance of frequency {freq}: {significance}')
```

Running this with data that has no noise, I got the following:
```
Calculated significance of frequency 2: 0.0
Calculated significance of frequency 3: 0.0
Calculated significance of frequency 4: 2.220446049250313e-16
Calculated significance of frequency 5: 0.0
Calculated significance of frequency 6: 0.0
Calculated significance of frequency 7: 0.0
Calculated significance of frequency 8: -2.220446049250313e-16
Calculated significance of frequency 9: -1.1102230246251565e-16
```

With data with noise with deviation of 0.01, we get:
```
Calculated significance of frequency 2: -0.002100143414827449
Calculated significance of frequency 3: -0.00012623164134739628
Calculated significance of frequency 4: 0.0012595373023303047
Calculated significance of frequency 5: 0.005169803256461991
Calculated significance of frequency 6: 0.005120405926670513
Calculated significance of frequency 7: 0.0023669236655896597
Calculated significance of frequency 8: 0.008376260921484358
Calculated significance of frequency 9: 0.014027116469695011
```

With deviation of 0.1, we get:
```
Calculated significance of frequency 2: 0.04844152652389755
Calculated significance of frequency 3: 0.08437329170874452
Calculated significance of frequency 4: 0.16136376178577816
Calculated significance of frequency 5: 0.2910539013534412
Calculated significance of frequency 6: 0.4817100011527302
Calculated significance of frequency 7: 0.6115901838823774
Calculated significance of frequency 8: 0.718340617898303
Calculated significance of frequency 9: 0.6636806739527958
```

With deviation of 0.5, HFF breaks down (the amplitude of the signal is around 0.6) and the significance detected by the function is a bit over 3:
```
Calculated significance of frequency 2: 1.0580536698256964
Calculated significance of frequency 354: 3.88744656904972
Calculated significance of frequency 208: 3.2257445418105206
Calculated significance of frequency 71: 3.8407370351194734
Calculated significance of frequency 91: 3.268217070541281
Calculated significance of frequency 358: 3.4543494599333595
Calculated significance of frequency 387: 3.7107069717564274
Calculated significance of frequency 408: 3.6340293395610406
```

For deviation of 0.3, the results are very interesting:
```
Calculated significance of frequency 2: 0.4741641984533347
Calculated significance of frequency 3: 0.8539925460175926
Calculated significance of frequency 4: 0.8250132397367975
Calculated significance of frequency 161: 3.999946102244574
Calculated significance of frequency 6: 3.120008835319023
Calculated significance of frequency 7: 2.280011903258249
Calculated significance of frequency 379: 3.563642622026796
Calculated significance of frequency 136: 3.325993519002677
```
Remember that the detected frequencies should be 2 through 9. In the results above, when HFF was able to detect the correct frequency, the significance is below 3 except for frequency 6. The value for frequency 6 can vary with each run of the algorithm since the noise generated is random. But what reamins the same all of the time is that a wrongly detected frequency has a significance greater than or equal to three. 

Therefore, I think that for starters we can assume that a significance below 3 means that the frequency was correctly detected. And the closer to 0 the more confident we are about this. 