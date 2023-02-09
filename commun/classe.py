import math
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
            sig_s[pos: pos + width] = length

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


class Convultion(Wave):
    def __init__(self, sig, h):
        super().__init__(sig.a, sig.f, sig.fe, sig.ph, sig.d)
        self.sig = sig
        self.h = h

    def make_wave(self):
        if self.sig_t is not None and self.sig_s is not None:
            return self.sig_t, self.sig_s

        self.sig_t, self.sig_s = self.sig.calculate()
        new_sig_s = np.zeros(len(self.sig_s))

        for i in range(len(self.sig_t)):
            for k in range(len(self.h)):
                if i - k < 0:
                    break
                print(i, k)
                new_sig_s[i] += self.h[k] * self.sig_s[i - k]

        self.sig_s = new_sig_s

        return self.sig_t, self.sig_s


class Signal:
    def __init__(self, A, f, Fo, fe, nmax, d, title, label, format):
        self.sig_s = None
        self.sig_t = None
        self.A = A
        self.f = f
        self.fe = fe
        self.Fo = Fo
        self.nmax = nmax
        self.d = d
        self.N = int(self.d * self.fe)

        self.title = title
        self.format = format
        self.label = label

    def an(self, n, A):
        return 1

    def bn(self, n, A):
        return 1

    def make_signal(self):
        self.sig_s = np.zeros(self.N)
        self.sig_t = np.zeros(self.N)
        self.te = 1.0 / self.fe

        for i in range(self.N):
            t = i * self.te  # instant correspondant
            self.sig_t[i] = t
            n = 0  # calcul de la valeur du sample
            while n < self.nmax:  # pour chaque harmonique ... on ajoute sa contribution
                self.sig_s[i] += self.an(n, self.A) * math.cos(
                    2 * math.pi * n * self.Fo * t
                ) + self.bn(n, self.A) * math.sin(2 * math.pi * n * self.Fo * t)
                n += 1

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

    def get_an(self):
        new_signal = Signal(
            self.A, self.f, self.Fo, self.fe, self.nmax, self.d, "", "", ""
        )
        # it's a signal but with only an values
        new_signal.sig_s = np.zeros(self.nmax)
        new_signal.sig_t = np.zeros(self.nmax)
        new_signal.te = 1.0 / self.fe
        new_signal.title = "an values"
        new_signal.format = "g."
        new_signal.label = "an values"

        for i in range(self.nmax):
            new_signal.sig_s[i] = self.an(i, self.A)
            new_signal.sig_t[i] = i

        return new_signal

    def get_bn(self):
        new_signal = Signal(
            self.A, self.f, self.Fo, self.fe, self.nmax, self.d, "", "", ""
        )
        # it's a signal but with only bn values
        new_signal.sig_s = np.zeros(self.nmax)
        new_signal.sig_t = np.zeros(self.nmax)
        new_signal.te = 1.0 / self.fe
        new_signal.title = "bn values"
        new_signal.format = "g."
        new_signal.label = "bn values"

        for i in range(self.nmax):
            new_signal.sig_s[i] = self.bn(i, self.A)
            new_signal.sig_t[i] = i

        return new_signal


class SignalT(Signal):
    def __init__(self, A, f, Fo, fe, nmax, d, title, label, format):
        super().__init__(A, f, Fo, fe, nmax, d, title, label, format)

    def an(self, n, A):
        if n % 2 == 0:
            return 0
        else:
            return (8 * A) / (np.pi ** 2) * (1 / (n ** 2))

    def bn(self, n, A):
        return 0


class SignalR(Signal):
    def __init__(self, A, f, Fo, fe, nmax, d, title, label, format):
        super().__init__(A, f, Fo, fe, nmax, d, title, label, format)

    def an(self, n, A):
        return 0

    def bn(self, n, A):
        if n == 0:
            return 0
        return (-2 * A) / np.pi * (1 / n)


class SignalC(Signal):
    def __init__(self, A, f, Fo, fe, nmax, d, title, label, format):
        super().__init__(A, f, Fo, fe, nmax, d, title, label, format)

    def an(self, n, A):
        return 0

    def bn(self, n, A):
        if n % 2 == 0:
            return 0
        return 4 * A / (np.pi * n)


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
        print(self.sig_t, self.sig_s)

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
            new_signal.sig_t[i] = i

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
            new_signal.sig_t[i] = i

        return new_signal


class SignalFFT(Wave):
    def __init__(self, signal):
        super().__init__(signal.a, signal.f, signal.fe, signal.ph, signal.d)
        self.signal = signal
        self.freq = np.zeros(int(self.d * self.fe))

    @staticmethod
    def fft(sig: Signal):
        sig_t, sig_s = sig.calculate()
        sig_s = np.fft.fft(sig_s)
        sig_s = np.abs(sig_s)
        sig_s = sig_s / len(sig_s)
        return sig_t, sig_s

    def make_wave(self):
        self.sig_t, self.sig_s = self.fft(self.signal)
        self.t = np.fft.fftshift(self.sig_t)
        self.sig_t = self.sig_t / len(self.sig_t)
        self.te = 1.0 / self.fe
        self.freq = np.fft.fftfreq(len(self.sig_t), self.te)

        return self.sig_t, self.sig_s
