from commun.Graph_f import Graph
from commun.classe import *

if __name__ == "__main__":
    # todo1
    A = 1
    f = 750
    Fo = f
    fe = 8000
    nmax = 32
    d = 3 * (1 / f)
    title = "Une wave"
    label = "Wave :"
    format = "-bo"

    signal = SignalT(
        A=A, f=f, Fo=Fo, fe=fe, nmax=nmax, d=d, title=title, label=label, format=format
    )
    signal.make_signal()

    signal_an = signal.get_an()
    signal_bn = signal.get_bn()

    graph = Graph(
        [signal, signal_an, signal_bn],
        plot_type="line",
        subplot=True,
        title="signal by fourrier coefs",
        xlabel="time",
        ylabel="Amplitude",
    )

    graph.plot()

    # todo3

    signal = SignalR(A=A, f=f, Fo=Fo, fe=fe, nmax=nmax, d=d, title=title, label=label, format=format)
    signal.make_signal()

    signal_an = signal.get_an()
    signal_bn = signal.get_bn()

    graph = Graph(
        [signal, signal_an, signal_bn],
        plot_type="line",
        subplot=True,
        title="signal by fourrier coefs",
        xlabel="time",
        ylabel="Amplitude",
    )

    graph.plot()

    signal = SignalC(A=A, f=f, Fo=Fo, fe=fe, nmax=nmax, d=d, title=title, label=label, format=format)
    signal.make_signal()

    signal_an = signal.get_an()
    signal_bn = signal.get_bn()

    graph = Graph(
        [signal, signal_an, signal_bn],
        plot_type="line",
        subplot=True,
        title="signal by fourrier coefs",
        xlabel="time",
        ylabel="Amplitude",
    )

    graph.plot()
