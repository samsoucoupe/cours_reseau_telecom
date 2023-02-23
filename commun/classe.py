import math
import struct
import wave as wv

import numpy as np


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
        wav = wv.open(self.title + ".wav", "w")
        wav.setparams((1, 2, self.fe, 0, "NONE", "not compressed"))
        wav.writeframes(np.int16(self.sig_s))
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


class SinWave(Wave):
    """
    Class for sinusoidal wave
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label = "Sin Wave : a={}, f={}, fe={}, ph={}, d={}".format(
            self.a, self.f, self.fe, self.ph, self.d
        )

    def wave_type(self, a, omega, t, ph):
        return a * np.sin(omega * t + ph)


class SquareWave(Wave):
    """
    Class for square wave
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label = "Square Wave : a={}, f={}, fe={}, ph={}, d={}".format(
            self.a, self.f, self.fe, self.ph, self.d
        )

    def wave_type(self, a, omega, t, ph):
        return a * (-1) ** np.floor(2 * self.f * t) + ph


class TriangleWave(Wave):
    """
    Class for triangle wave
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label = "Triangle Wave : a={}, f={}, fe={}, ph={}, d={}".format(
            self.a, self.f, self.fe, self.ph, self.d
        )

    def wave_type(self, a, omega, t, ph):
        return a * (
            (4 * abs((t + ph) / (1 / self.f) - np.floor(t / (1 / self.f) + 1 / 2)))
            - 1.0
        )


class SawTeethWave(Wave):
    """
    Class for saw teeth wave
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label = "Saw Teeth Wave : a={}, f={}, fe={}, ph={}, d={}".format(
            self.a, self.f, self.fe, self.ph, self.d
        )

    def wave_type(self, a, omega, t, ph):
        return 2 * a * (t * self.f - np.floor(t * self.f) - 0.5) + ph


class GaussianWave(Wave):
    """
    Class for gaussian wave
    """

    def __init__(self, mean, std, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label = "Gaussian Wave : a={}, f={}, fe={}, ph={}, d={}".format(
            self.a, self.f, self.fe, self.ph, self.d
        )

        self.mean = mean
        self.std = std

    def wave_type(self, a, omega, t, ph):
        return np.random.normal(self.mean, self.std, t.shape)


class ImpulseWave(Wave):
    """
    Class for impulse wave
    """

    def __init__(self, mean, std, nbi, di, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label = "Impulse Wave : a={}, f={}, fe={}, ph={}, d={}".format(
            self.a, self.f, self.fe, self.ph, self.d
        )
        self.mean = mean
        self.std = std
        self.nbi = nbi  # nombre d'impulsions
        self.di = di  # durée d'une impulsion

    def make_wave(self):
        omega = 2 * np.pi * self.f
        N = int(self.d * self.fe)
        te = 1.0 / self.fe

        t = np.linspace(0, self.d, N)
        sig_s = np.zeros(t.shape)

        for i in range(self.nbi):
            width = self.di
            length = np.random.normal(self.mean, self.std)
            pos = np.random.randint(0, N)
            sig_s[pos : pos + width] = length

        self.sig_t = t
        self.sig_s = sig_s


class CosWave(Wave):
    """
    Class for cosine wave
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label = "Cos Wave : a={}, f={}, fe={}, ph={}, d={}".format(
            self.a, self.f, self.fe, self.ph, self.d
        )

    def wave_type(self, a, omega, t, ph):
        return a * np.cos(omega * t + ph)


class Convolution(Wave):
    def __init__(self, sig, h):
        super().__init__(sig.a, sig.f, sig.fe, sig.ph, sig.d)
        self.sig = sig
        self.h = h

    def make_wave(self):

        self.sig_t, self.sig_s = self.sig.sig_t, self.sig.sig_s
        new_sig_s = np.zeros(len(self.sig_s))

        for i in range(len(self.sig_t)):
            for k in range(len(self.h)):
                if i - k < 0:
                    break

                new_sig_s[i] += self.h[k] * self.sig_s[i - k]

        self.sig_s = new_sig_s


class SignalFourrier(Wave):
    def __init__(self, a, f, Fo, fe, d, title, label, format, nmax, an, bn):
        super().__init__(a, f, Fo, fe, d, title, label, format)
        self.fe = fe
        self.an = an
        self.bn = bn
        self.nmax = nmax
        self.N = int(self.d * self.fe)
        self.Fo = Fo
        self.sig_s = np.zeros(self.N)
        self.sig_t = np.zeros(self.N)

    def make_wave(self):

        self.te = 1.0 / self.fe

        for i in range(self.N):
            t = i * self.te  # instant correspondant
            self.sig_t[i] = t
            n = 0  # calcul de la valeur du sample
            while n < self.nmax:  # pour chaque harmonique ... on ajoute sa contribution
                self.sig_s[i] += self.an(n, self.a) * math.cos(
                    2 * math.pi * n * self.Fo * t
                ) + self.bn(n, self.a) * math.sin(2 * math.pi * n * self.Fo * t)
                n += 1

    def get_an(self):
        new_signal = SignalFourrier(
            a=self.a,
            f=self.f,
            Fo=self.Fo,
            fe=self.fe,
            nmax=self.nmax,
            d=self.d,
            title="",
            label="",
            format="",
            an=self.an,
            bn=self.bn,
        )
        new_signal.sig_s = np.zeros(self.nmax)
        new_signal.sig_t = np.zeros(self.nmax)
        new_signal.te = 1.0 / self.fe
        new_signal.title = "an values"
        new_signal.format = "g."
        new_signal.label = "an values"

        for i in range(self.nmax):
            new_signal.sig_s[i] = self.an(i, self.a)
            new_signal.sig_t[i] = i * self.te

        return new_signal

    def get_bn(self):
        new_signal = SignalFourrier(
            a=self.a,
            f=self.f,
            Fo=self.Fo,
            fe=self.fe,
            nmax=self.nmax,
            d=self.d,
            title="",
            label="",
            format="",
            an=self.an,
            bn=self.bn,
        )
        new_signal.sig_s = np.zeros(self.nmax)
        new_signal.sig_t = np.zeros(self.nmax)
        new_signal.te = 1.0 / self.fe
        new_signal.title = "bn values"
        new_signal.format = "g."
        new_signal.label = "bn values"

        for i in range(self.nmax):
            new_signal.sig_s[i] = self.bn(i, self.a)
            new_signal.sig_t[i] = i * self.te

        return new_signal


class SignalFFT(Wave):
    def __init__(self, signal):
        super().__init__(signal.a, signal.f, signal.fe, signal.ph, signal.d)
        self.signal = signal
        self.freq = np.zeros(int(self.d * self.fe))

    def ftt(self):
        self.signal.make_wave()
        self.sig_s = np.fft.fft(self.signal.sig_s)
        self.sig_t = np.fft.fftfreq(len(self.signal.sig_s), self.signal.te)
        self.freq = self.sig_t

    def get_freq(self):
        return self.freq


class Quantificateur(Wave):
    def __init__(self, signal, vmax, b, step=0):
        super().__init__(
            signal.a,
            signal.f,
            signal.fe,
            signal.ph,
            signal.d,
            signal.title,
            signal.label,
            signal.format,
        )
        self.signal = signal
        self.vmax = vmax
        self.b = b
        self.sig_s = np.zeros(len(self.signal.sig_s))
        self.sig_t = np.zeros(len(self.signal.sig_s))
        self.dico = {}
        self.step = step
        if self.step == 0:
            self.step = 2 * self.vmax / (2**self.b)

    def make_dico(self):
        """
        Crée un dictionnaire uniforme de quantification sur "b" bits
        pour des signaux d'amplitude max "vmax"
        """
        self.dico = {}

        for i in range(2**self.b):
            self.dico[i] = i * self.step - self.vmax + self.step / 2

    def quantificate(self):
        self.make_dico()
        for i in range(len(self.signal.sig_s)):
            diff = [
                abs(self.signal.sig_s[i] - self.dico[j]) for j in range(2**self.b)
            ]
            min_diff = min(diff)
            index = diff.index(min_diff)
            self.sig_s[i] = self.dico[index]
            self.sig_t[i] = self.signal.sig_t[i]

        self.change_format("ro")
        self.change_label("Quantificateur")
        self.change_title("Quantificateur")

        difference = Wave(a=self.a, f=self.f, fe=self.fe, ph=self.ph, d=self.d)
        difference.sig_s = abs(self.signal.sig_s - self.sig_s)
        difference.change_format("bx")
        difference.change_label("Difference")
        difference.change_title("Difference")

        return difference

    def MSE(self):
        return np.sum((self.signal.sig_s - self.sig_s) ** 2) / len(self.signal.sig_s)

    def SNR(self):
        return 10 * np.log10(np.sum(self.signal.sig_s**2) / self.MSE())


# TPNOTES


class DTMF(Wave):
    def __init__(
        self,
        file,
    ):
        super().__init__(a=1, f=0, fe=10, ph=0, d=0, title="", label="", format="")
        self.file = file
        self.sig_t, self.sig_s = np.loadtxt(self.file)


class DTMF09(Wave):
    def __init__(self):
        super().__init__(a=1, f=0, fe=10, ph=0, d=0, title="", label="", format="")

        self.fe = 4000
        self.valeur = {
            "0": [941, 1336],
            "1": [697, 1209],
            "2": [697, 1336],
            "3": [697, 1477],
            "4": [770, 1209],
            "5": [770, 1336],
            "6": [770, 1477],
            "7": [852, 1209],
            "8": [852, 1336],
            "9": [852, 1477],
        }

    def generate_signal(self):
        # make a signal using self.valeur to make a signal with the number 0123456789 sur des echantillon de 40 ms puisun blanc de40 ms

        self.sig_s = np.zeros(4000)
        self.sig_t = np.linspace(0, 1, self.fe)

        for i in range(10):
            # f1= frequence horizontale
            # f2= frequence verticale
            freq1 = self.valeur[str(i)][0]
            freq2 = self.valeur[str(i)][1]
            t = np.linspace(0, 0.04, int(0.04 * self.fe), endpoint=False)

            signal1 = np.sin(2 * np.pi * freq1 * t)
            signal2 = np.sin(2 * np.pi * freq2 * t)

            # Concatenate signals and add silence for 0.04 seconds
            signal = np.concatenate((signal1, signal2, np.zeros(int(0.04 * self.fe))))

            # Add signal to output array
            start_idx = int(i * 0.08 * self.fe)
            end_idx = start_idx + len(signal)
            self.sig_s[start_idx:end_idx] = signal

        # Print signal for debugging
        print(self.sig_s)

    def generate_with_space(self):
        self.sig_s = np.zeros(4000)
        self.sig_t = np.linspace(0, 1, self.fe)
        # genere on fait un signal avec 0 1 2 3 4 5 6 7 8 9 et on fait un espace entre chaque de 40 ms
        # on fait un signal de 4000 echantillons
        # avec chaque echantillon de 40 ms
        for i in range(20):
            if i % 2 == 0:
                # f1= frequence horizontale
                # f2= frequence verticale
                freq1 = self.valeur[str(i // 2)][0]
                freq2 = self.valeur[str(i // 2)][1]

                t = np.linspace(0, 0.04, int(0.04 * self.fe), endpoint=False)

                signal1 = np.sin(2 * np.pi * freq1 * t)
                signal2 = np.sin(2 * np.pi * freq2 * t)
                # Concatenate signals and add silence for 0.04 seconds
                signal = np.concatenate(
                    (signal1, signal2, np.zeros(int(0.04 * self.fe)))
                )

                # Add signal to output array
                start_idx = int(i * 0.04 * self.fe)
                end_idx = start_idx + len(signal)
                self.sig_s[start_idx:end_idx] = signal

            else:
                signal = np.zeros(int(0.04 * self.fe))
                start_idx = int(i * 0.04 * self.fe)
                end_idx = start_idx + len(signal)
                self.sig_s[start_idx:end_idx] = signal

    def convert_to_wav(self):
        nbCanal = 1
        nbOctet = 1
        fe = 4000
        duree = 1
        nbEchantillon = fe * duree
        wave = wv.open(f"{self.title}.wav", "w")
        wave.setparams((nbCanal, nbOctet, fe, nbEchantillon, "NONE", "not compressed"))
        for i in range(len(self.sig_s)):
            val = int(self.sig_s[i])
            if val > 1:
                val = 1
            if val < 1:
                val = -1
            val = int(val * 127.5 + 127.5)
            try:
                fr = struct.pack("B", val)
                # print(fr)
                # print("Sample {} = {}/{}".format(i,y[i],val))
            except struct.error as err:
                print(err)

            wave.writeframes(fr)
        wave.close()
