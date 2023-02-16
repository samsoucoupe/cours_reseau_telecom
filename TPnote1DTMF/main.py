import numpy as np

from commun.Graph_f import Graph


class Wave:
    """
    Super class that holds the common properties of all wave classes
    """

    def __init__(
        self,
        a=1.0,
        f=440.0,
        fe=8000.0,
        ph=0.0,
        d=1.0,
        title="Une wave",
        label="Wave :",
        format="-bo",
    ):
        self.sig_s = np.linspace(0, d, int(d * fe))
        self.a = a
        self.f = f
        self.fe = fe
        self.ph = ph
        self.d = d
        self.title = title
        self.format = format
        self.label = label
        self.sig_t = np.linspace(0, self.d, int(self.d * self.fe))

    def make_wave(self):
        omega = 2 * np.pi * self.f
        N = int(self.d * self.fe)
        te = 1.0 / self.fe

        t = np.linspace(0, self.d, N)
        sig_s = self.wave_type(self.a, omega, t, self.ph)

        self.sig_t = t
        self.sig_s = sig_s

    def wave_type(self, a, omega, t, ph):
        return None

    def plot_on_ax(self, ax):
        ax.plot(self.sig_t, self.sig_s, self.format, label=self.label)

    def scatter_on_ax(self, ax):
        ax.scatter(self.sig_t, self.sig_s, label=self.label)

    def change_format(self, format):
        self.format = format

    def change_label(self, label):
        self.label = label

    def change_title(self, title):
        self.title = title

    def add_signal(self, signal):
        self.sig_s = self.sig_s + signal.sig_s

    def __add__(self, other):
        new_signal = Wave()

        self.make_wave()
        other.make_wave()

        if len(self.sig_t) != len(other.sig_t):
            raise Exception("Les deux signaux doivent avoir la meme duree")

        new_signal.sig_t = self.sig_t
        sig_s = np.add(self.sig_s, other.sig_s)

        new_signal.title = self.title + " + " + other.title
        new_signal.make_wave = lambda: sig_s
        new_signal.sig_s = sig_s

        return new_signal

    def convert_to_wav(self):
        """
        Convert the signal to a wav file
        """
        wav = wv.open("test.wav", "w")
        wav.setparams((1, 2, self.fe, 0, "NONE", "not compressed"))
        wav.writeframes(self.sig_s)
        wav.close()

    def make_spectrum(self):
        """
        Create a spectrum of the signal
        """
        new_signal = Wave()
        spectrum = np.fft.fftshift(np.fft.fft(self.sig_s))
        new_signal.sig_s = spectrum
        new_signal.sig_t = np.linspace(-self.fe / 2, self.fe / 2, len(spectrum))
        new_signal.title = "Spectrum of " + self.title
        return new_signal


class DTMF(Wave):
    def __init__(
        self,
        file,
    ):
        super().__init__(a=1, f=0, fe=10, ph=0, d=0, title="", label="", format="")
        self.file = file
        self.sig_t, self.sig_s = np.loadtxt(self.file)

    def get_dtmf_number_i(self, i):
        newsignal = Wave()
        newsignal.sig_t = self.sig_t[i * 160 + 1 : (i + 1) * 160 + 1]
        newsignal.sig_s = self.sig_s[i * 160 + 1 : (i + 1) * 160 + 1]

        return newsignal

    def get_digit(self):
        # afficher les spectres des echantilonnes coupe toutes les 40ms
        # pour chaque echantillon, calculer le spectre
        l_ech = []
        for i in range(0, 8, 2):
            newsignal = self.get_dtmf_number_i(i)
            newsignal.make_spectrum()
            l_ech.append(newsignal.make_spectrum())
        Graph(l_ech, subplot=True, plot_type="line", title="Signal DTMF").plot()

    def make_spectrum_freqstep(self, freqstep):
        """
        Create a spectrum of the signal
        """
        new_signal = Wave()
        spectrum = np.fft.fftshift(np.fft.fft(self.sig_s))
        new_signal.sig_s = spectrum
        new_signal.sig_t = np.linspace(-self.fe / 2, self.fe / 2, len(spectrum))
        new_signal.title = "Spectrum of " + self.title
        return new_signal


if __name__ == "__main__":
    signal = DTMF("phone.out")
    Graph([signal], plot_type="line", title="Signal DTMF").plot()
    signal.get_digit()
