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
        self.sig_s = None
        self.sig_t = None
        self.a = a
        self.f = f
        self.fe = fe
        self.ph = ph
        self.d = d
        self.title = title
        self.format = format
        self.label = label

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
            raise Exception(
                "Les deux signaux doivent avoir la meme duree"
            )

        new_signal.sig_t = self.sig_t
        sig_s = np.add(self.sig_s, other.sig_s)

        new_signal.title = self.title + " + " + other.title
        new_signal.make_wave = lambda: sig_s
        new_signal.sig_s = sig_s

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
            sig_s[pos:pos + width] = length

        self.sig_t = t
        self.sig_s = sig_s
