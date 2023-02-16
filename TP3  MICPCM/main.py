from commun.Graph_f import Graph
from commun.classe import *

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

    signal = Quantificateur(Signal, a, b)
    difference = signal.quantificate()

    Graph([Signal, signal, difference], plot_type="line", title="Signal 2").plot()
    print("MSE = ", signal.MSE())
    print("SNR = ", signal.SNR())
    step = 0.75
    signal = Quantificateur(Signal, a, b)
    signal.step = step
    print(signal.step)
    difference = signal.quantificate()
    Graph([Signal, signal, difference], plot_type="line", title="Signal 2").plot()
    print(signal.sig_s)
    print("MSE = ", signal.MSE())
    print("SNR = ", signal.SNR())
