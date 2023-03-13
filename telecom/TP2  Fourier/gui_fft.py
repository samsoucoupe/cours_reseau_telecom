#!/usr/bin/env python
"""
http://yukuan.blogspot.com/2006/12/fft-in-python.html
This example demonstrates the FFT of a simple sine wave and displays its
bilateral spectrum.  

Since the frequency of the sine wave is folded by
whole number freqStep, the bilateral spectrum will display two non-zero point.
 
"""
import math
import numpy as np
import matplotlib.pyplot as plt


def plot_fft(N, freqStep, Fe, t, s_t, s_f):
    """
    s_f is the fft of s_t(t) on N samples

    """
    #==== Symetrisation et normalisation du spectre du signal
    #cf https://dsp.stackexchange.com/questions/4825/why-is-the-fft-mirrored
    s_f = np.fft.fftshift(s_f)      # middles the zero-point's axis
    s_f = s_f/N    # Normalization => ainsi le module ne dependra
                   # de la longueur du signal ou de sa fe
    freq = freqStep * np.arange(-N/2, N/2)  # ticks in frequency domain

    #=== Affichage console des valeurs des raies
    for i,r in enumerate(list(s_f)):
        print("Raie {} \t= \t{:.5g}".format(freq[i],r))

    #==== Plot des spectres 
    plt.figure(figsize=(8,8))
    plt.subplots_adjust(hspace=.6)
    # Plot time data ---------------------------------------
    plt.subplot(3,1,1)
    plt.plot(t, s_t, '.-', label="N={}, fe={}".format(N,Fe))
    plt.grid(True)
    plt.legend()
    plt.xlabel('Time (seconds)')
    plt.ylabel('Amplitude')
    plt.title('Signal')
    plt.axis('tight')
    # Plot spectral magnitude ------------------------------
    plt.subplot(3,1,2)
    plt.plot(freq, np.abs(s_f), '.-b', label="freqStep={}".format(freqStep))
    plt.grid(True)
    plt.legend()
    plt.xlabel('Frequency')
    plt.ylabel('S(F) Magnitude (Linear)')   
    # Plot phase -------------------------------------------
    plt.subplot(3,1,3)
    plt.plot(freq, np.angle(s_f), '.-b')
    plt.grid(True)
    plt.xlabel('Frequency')
    plt.ylabel('S(F) Phase (Radian)')

#==============================================

if __name__ == '__main__':
    N = 32  # the number of points in signal s(n*te) et S(n*Fe)
            # Power of 2 !
    Fe = 8000.       # the sampling rate
    Te = 1./Fe       # the sampling period
    freqStep = Fe/N  # resolution of the frequency IN FREQUENCY DOMAIN
    f = 3*freqStep # frequency of the sine wave
                     # On choisit un multiple de freqstep
    T = 1.0/f        # periode de la sinusoide
    a = 255
    
    #====  Generation d'un signal via numpy !
    t = np.arange(N)*Te         # N ticks in time domain, t = n*Te
                                # t vector covers 3 periods of cos.
    s_t = a*np.cos(2*math.pi*f*t) # cos
    s_t = a*(4*(abs(t*f-np.floor(t*f+0.5)))-1.0) # triangle
        
    #==== Calcul du spectre du signal 
    s_f = np.fft.fft(s_t)       # Spectrum
    print("fft result is a {} of len {} of type {}\n".format(type(s_f),len(s_f),type(s_f[0])))

    # Plot
    plot_fft(N, freqStep,  Fe, t, s_t, s_f)

    plt.savefig("fft_example{}.png".format(N))
    plt.show()
