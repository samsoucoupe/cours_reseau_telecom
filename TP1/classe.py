import numpy as np


class Wave:
    """
    Super class that holds the common properties of all wave classes
    """

    def __init__(self, a=1.0, f=440.0, fe=8000.0, ph=0.0, d=1.0, title="Une wave", label="Wave :", format="-bo"):
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


class SinWave(Wave):
    """
    Class for sinusoidal wave
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label = "Sin Wave : a={}, f={}, fe={}, ph={}, d={}".format(self.a, self.f, self.fe, self.ph, self.d)

    def wave_type(self, a, omega, t, ph):
        return a * np.sin(omega * t + ph)


class SquareWave(Wave):
    """
    Class for square wave
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label = "Square Wave : a={}, f={}, fe={}, ph={}, d={}".format(self.a, self.f, self.fe, self.ph, self.d)

    def wave_type(self, a, omega, t, ph):
        return a * (-1) ** np.floor(2 * self.f * t) + ph


class TriangleWave(Wave):
    """
    Class for triangle wave
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label = "Triangle Wave : a={}, f={}, fe={}, ph={}, d={}".format(self.a, self.f, self.fe, self.ph, self.d)

    def wave_type(self, a, omega, t, ph):
        return 4 * a * (np.abs(t * self.f - np.floor(t * self.f + 0.5)) - 1.0) + ph


class SawTeethWave(Wave):
    """
    Class for saw teeth wave
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label = "Saw Teeth Wave : a={}, f={}, fe={}, ph={}, d={}".format(self.a, self.f, self.fe, self.ph, self.d)

    def wave_type(self, a, omega, t, ph):
        return 2 * a * (t * self.f - np.floor(t * self.f) - 0.5) + ph
