import math

from Graph_f import Graph
from classe import SinWave, SquareWave, SawTeethWave, TriangleWave, GaussianWave, ImpulseWave

if __name__ == "__main__":
    # Sinusoidal wave
    sin_wave = SinWave(
        a=2, f=50, fe=1000, ph=0, d=0.08, title="Une sinusoide", format="--g*"
    )
    sin_wave.make_wave()

    graph = Graph(
        waves=[sin_wave],
        plot_type="line",
        subplot=False,
        title="SinWave",
        xlabel="t",
        ylabel="Amplitude",
    )
    # graph.plot()

    # todo2

    d = 0.04
    sin_wave1 = SinWave(
        a=1.28, f=50, fe=500, ph=0, d=d, title="Deux sinusoide", format="bo"
    )
    sin_wave1.make_wave()

    sin_wave2 = SinWave(
        a=0.5, f=50, fe=1000, ph=math.pi, d=d, title="Deux sinusoide", format="r."
    )
    sin_wave2.make_wave()

    sin_waves = [sin_wave1, sin_wave2]

    graph = Graph(
        waves=sin_waves,
        plot_type="line",
        subplot=False,
        title="SinWaves",
        xlabel="t",
        ylabel="Amplitude",
    )
    # graph.plot()

    # todo3 signal carré

    d = 0.08
    sin_square1 = SquareWave(
        a=1, f=50, fe=1000, ph=0, d=d, title="Un signal carré", format="-bo"
    )
    sin_square1.make_wave()

    graph = Graph(
        waves=[sin_square1],
        plot_type="line",
        subplot=False,
        title="SquareWave",
        xlabel="t",
        ylabel="Amplitude",
    )
    # graph.plot()

    # todo3.2 signal saw teeth

    d = 0.08
    sin_saw_teeth = SawTeethWave(
        a=3, f=50, fe=800, ph=0, d=d, title="Un signal saw teeth", format="-bo"
    )
    sin_saw_teeth.make_wave()

    graph = Graph(
        waves=[sin_saw_teeth],
        plot_type="line",
        subplot=False,
        title="SawTeethWave",
        xlabel="t",
        ylabel="Amplitude",
    )
    # graph.plot()

    # todo3.3 signal triangle

    d = 0.08
    sin_triangle = TriangleWave(
        a=3, f=50, fe=800, ph=0, d=d, title="Un signal triangle", format="-bo"
    )
    sin_triangle.make_wave()

    graph = Graph(
        waves=[sin_triangle],
        plot_type="line",
        subplot=False,
        title="TriangleWave",
        xlabel="t",
        ylabel="Amplitude",
    )
    graph.plot()

    # sin wave with noise

    a = 2
    f = 50.0
    fe = 1000.0
    ph = 0
    d = 0.08

    sin_wave = SinWave(
        a=2, f=50, fe=1000, ph=0, d=0.08, title="Une sinusoide", format="-bo"
    )
    sin_wave.make_wave()

    mean = 0
    std = 0.2
    gaussian_wave = GaussianWave(mean=mean, std=std, fe=1000, d=0.08, title="Gaussian noise", format="-g.")
    gaussian_wave.make_wave()

    mean = 0
    std = 2 * a
    nbi = 2
    di = 2

    impluse = ImpulseWave(mean=mean, std=std, fe=1000, d=0.08, title="Impulse noise", nbi=nbi, di=di, format="-g.")
    impluse.make_wave()

    sin_wave_sum = sin_wave + gaussian_wave + impluse
    sin_wave_sum.change_format("-r.")
    l_wave = [sin_wave, gaussian_wave, impluse, sin_wave_sum]
    graph = Graph(
        l_wave,
        plot_type="line",
        subplot=True,
        title="SinWave with noise",
        xlabel="t",
        ylabel="Amplitude",
    )
    graph.plot()
