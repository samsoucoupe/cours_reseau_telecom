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

    # Exercice 6
    sin1 = CosWave(
        a=1, f=10, fe=1000, ph=0, d=0.25, title="cos wave 1", label="Wave :", format="-bo"
    )
    sin2 = CosWave(
        a=1, f=20, fe=1000, ph=0, d=0.25, title="cos wave 3", label="Wave :", format="-bo"
    )
    sin3 = CosWave(
        a=1,
        f=400,
        fe=1000,
        ph=0,
        d=0.25,
        title="cos wave 3",
        label="Wave :",
        format="-bo",
    )

    sum = sin1 + sin2 + sin3
    sum.change_title("sum")

    graph = Graph(
        [sin1, sin2, sin3, sum],
        plot_type="line",
        subplot=True,
        title="Exercice 6",
        xlabel="t",
    )
    graph.plot()

    h = [
        -6.849167e-003,
        1.949014e-003,
        1.309874e-002,
        1.100677e-002,
        -6.661435e-003,
        -1.321869e-002,
        6.819504e-003,
        2.292400e-002,
        7.732160e-004,
        -3.153488e-002,
        -1.384843e-002,
        4.054618e-002,
        3.841148e-002,
        -4.790497e-002,
        -8.973017e-002,
        5.285565e-002,
        3.126515e-001,
        4.454146e-001,
        3.126515e-001,
        5.285565e-002,
        -8.973017e-002,
        -4.790497e-002,
        3.841148e-002,
        4.054618e-002,
        -1.384843e-002,
        -3.153488e-002,
        7.732160e-004,
        2.292400e-002,
        6.819504e-003,
        -1.321869e-002,
        -6.661435e-003,
        1.100677e-002,
        1.309874e-002,
        1.949014e-003,
        -6.849167e-003,
    ]

    convolution = Convolution(h=h, sig=sum)
    convolution.make_wave()

    graph = Graph([convolution], plot_type="line", subplot=False, title="Exercice 6", xlabel="t")
    graph.plot()
