from commun.Graph_f import Graph
from commun.classe import *

if __name__ == "__main__":
    # todo1
    a = 1.5
    f = 750
    Fo = f
    fe = 8000
    nmax = 32
    d = 3 * (1 / f)
    title = "Une wave"
    label = "Wave :"
    format = "-bo"


    # SignalT
    def an(n, A):
        if n % 2 == 0:
            return 0
        else:
            return (8 * A) / (np.pi ** 2) * (1 / (n ** 2))


    def bn(n, A):
        return 0


    Signal = SignalFourrier(
        a=a,
        f=f,
        Fo=Fo,
        fe=fe,
        nmax=nmax,
        d=d,
        title=title,
        label=label,
        format=format,
        an=an,
        bn=bn,
    )
    Signal.make_wave()

    graph = Graph(
        [Signal, Signal.get_an(), Signal.get_bn()],
        plot_type="line",
        subplot=True,
        title="SignalT",
        xlabel="t",
    )
    graph.plot()


    # signalR
    def an(n, A):
        return 0


    def bn(n, A):
        if n == 0:
            return 0
        return (-2 * A) / np.pi * (1 / n)


    Signal = SignalFourrier(
        a=a,
        f=f,
        Fo=Fo,
        fe=fe,
        nmax=nmax,
        d=d,
        title=title,
        label=label,
        format=format,
        an=an,
        bn=bn,
    )
    Signal.make_wave()

    graph = Graph(
        [Signal, Signal.get_an(), Signal.get_bn()],
        plot_type="line",
        subplot=True,
        title="SignalR",
        xlabel="t",
    )
    graph.plot()


    # signalC

    def an(n, A):
        return 0


    def bn(n, A):
        if n % 2 == 0:
            return 0
        else:
            return 4 * A / (np.pi * n)


    Signal = SignalFourrier(
        a=a,
        f=f,
        Fo=Fo,
        fe=fe,
        nmax=nmax,
        d=d,
        title=title,
        label=label,
        format=format,
        an=an,
        bn=bn,
    )
    Signal.make_wave()

    graph = Graph(
        [Signal, Signal.get_an(), Signal.get_bn()],
        plot_type="line",
        subplot=True,
        title="SignalC",
        xlabel="t",
    )
    graph.plot()
