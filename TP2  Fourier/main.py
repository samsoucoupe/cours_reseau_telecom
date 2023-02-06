from commun.Graph_f import Graph
from commun.classe import Signal, SignalT

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

    # todo2
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

    graph = Graph(
        [signal],
        plot_type="line",
        subplot=True,
        title="SinWave with noise",
        xlabel="t",
        ylabel="Amplitude",
    )
    graph.plot()
