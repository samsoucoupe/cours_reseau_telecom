import math
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
import gui_fft
#==============================================

if __name__ == '__main__':
    filename = "La3piano.wav"
    filename = "La3guitare.wav"
    filename = "La3diapason.wav"
    filename = "La3guitare.wav"

    Fe,s_t = wavfile.read(filename, mmap=False)

    # on ne fait la FFT que des N premiers samples
    N = 1024 
    freqStep = Fe/N
    t = np.arange(N)/Fe
    s_t = s_t[0:N]
    s_f = np.fft.fft(s_t)   # Spectrum
    
    gui_fft.plot_fft(N, freqStep, Fe, t, s_t, s_f)
    plt.show()
