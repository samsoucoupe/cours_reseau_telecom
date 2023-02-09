from commun.Graph_f import Graph
from commun.classe import *


# ---------------------------------------------


def make_dico(vmax, b):
    """
    Crée un dictionnaire uniforme de quantification sur "b" bits
    pour des signaux d'amplitude max "vmax"
    """
    D = {}
    step = 2 * vmax / (2 ** b)
    for i in range(2 ** b):
        D[i] = i * step - vmax + step / 2
    return D


# ---------------------------------------------


def QS(signal, vmax, b):
    # change le sig s du signal original
    """
    Quantificateur sur b bits d'un signal sig_s d'amplitude max vmax.
    """
    # Creation du dictionnaire de quantification = une liste de ""codewords"
    D = make_dico(vmax, b)
    newsignal = SinWave(a=signal.a, f=signal.f, fe=signal.fe, d=signal.d)
    # Pour l'instant le signal quantifie est le meme que le signal original.
    for i in range(len(signal.sig_s) - 1):
        # diff avec tout les points du dico et on prend le plus proche
        diff = [abs(signal.sig_s[i] - D[j]) for j in range(2 ** b)]
        # on prend le plus petit
        min_diff = min(diff)
        # on prend l'index du plus petit
        index = diff.index(min_diff)
        # on prend la valeur du dico qui correspond à l'index
        newsignal.sig_s[i] = D[index]

    newsignal.change_format("ro")
    difference = SinWave(a=signal.a, f=signal.f, fe=signal.fe, d=signal.d)
    difference.sig_s = abs(signal.sig_s - newsignal.sig_s)
    difference.change_format("bx")

    return newsignal, difference


# ---------------------------------------------

if __name__ == "__main__":
    np.set_printoptions(linewidth=250)
    np.set_printoptions(precision=3, suppress=True)
    a = 5.0
    b = 3

    # Signal à quantifier
    fe = 20000.0
    f = 50.0
    d = 0.02

    Signal = SinWave(a=a, f=f, fe=fe, d=d)
    Signal.make_wave()
    print("Signal.sig_s = ", Signal.sig_s)

    Q, Diff = QS(Signal, a, b)

    # Affichage du signal
    graph = Graph([Signal, Q, Diff], plot_type="line", title="Signal original")
    graph.plot()

    MSE = np.sum(Diff.sig_s ** 2) / len(Diff.sig_s)


    def MSE(self):
        sig_t, sig_s = self.calculate()
        return np.var(sig_s - self.signal.sig_s)


    def SNR(self):
        sig_t, sig_s = self.calculate()
        return 10 * np.log10(np.var(self.signal.sig_s) / self.MSE())
