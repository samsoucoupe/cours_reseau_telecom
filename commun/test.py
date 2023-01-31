import math

import numpy as np

from Graph_f import Graph


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

    def plot_on_ax(self, ax):
        ax.plot(self.sig_t, self.sig_s, self.format, label=self.label)

    def scatter_on_ax(self, ax):
        ax.scatter(self.sig_t, self.sig_s, label=self.label)

    def change_format(self, format):
        self.format = format

    def add_signal(self, signal):
        self.sig_s = self.sig_s + signal.sig_s

    def __add__(self, other):
        new_signal = Signal()
        new_signal.sig_s = self.sig_s + other.sig_s
        new_signal.sig_t = self.sig_t
        return new_signal


class SignalT(Signal):
    def __init__(self, A, f, Fo, fe, nmax, d, title, label, format):
        super().__init__(A, f, Fo, fe, nmax, d, title, label, format)

    def an(self, n, A):
        if n % 2 == 0:
            return 0
        else:
            return (8 * A) / (np.pi**2) * (1 / (n**2))

    def bn(self, n, A):
        return 0


A = 1
f = 750
Fo = f
fe = 8000
nmax = 32
d = 3 * (1 / f)
title = "Une wave"
label = "Wave :"
format = "-bo"

signal = Signal(
    A=A, f=f, Fo=Fo, fe=fe, nmax=nmax, d=d, title=title, label=label, format=format
)
signal.make_signal()

graph = Graph(
    [signal],
    plot_type="line",
    subplot=True,
    title="SinWave with noise",
    xlabel="t",
    ylabel="Amplitude",
)
graph.plot()
