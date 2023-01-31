from commun.Graph_f import Graph
from commun.classe import SinWave, SquareWave, SawTeethWave, TriangleWave

if __name__ == "__main__":
    # test function make_wave
    # create a sin wave
    sin_wave = SinWave(
        a=2, f=50, fe=1000, ph=0, d=0.08, title="Une sinusoide", format="-bo"
    )
    sin_wave.make_wave()
    # create a square wave
    sin_square = SquareWave(
        a=1, f=50, fe=1000, ph=0, d=0.08, title="Un signal carré", format="-g."
    )
    sin_square.make_wave()
    # create a saw teeth wave
    sin_saw_teeth = SawTeethWave(
        a=3, f=50, fe=800, ph=0, d=0.08, title="Un signal saw teeth", format="-r."
    )
    sin_saw_teeth.make_wave()
    # create a triangle wave
    sin_triangle = TriangleWave(
        a=3, f=50, fe=800, ph=0, d=0.08, title="Un signal triangle", format="-y."
    )
    sin_triangle.make_wave()

    l_sin = [sin_wave, sin_square, sin_saw_teeth, sin_triangle]
    graph = Graph(
        waves=l_sin,
        plot_type="line",
        subplot=True,
        title="SinWave",
        xlabel="t",
        ylabel="Amplitude",
    )
    graph.plot()

    # test function add_noise

    sin_wave = SinWave(
        a=2,
        f=50,
        fe=1000,
        ph=0,
        d=0.08,
        title="Une sinusoide avec du bruit",
        format="-bo",
    )
    sin_wave.make_wave()
    sin_wave_n = SinWave(
        a=2, f=50, fe=1000, ph=0, d=0.08, title="Une sinusoide", format="-bo"
    )
    sin_wave_n.make_wave()
    noise = sin_wave_n.generate_gaussian_noise(0, 0.2)
    sin_wave.add_noise(noise)
    l_sin = [sin_wave_n, sin_wave]

    graph = Graph(
        waves=l_sin,
        plot_type="line",
        subplot=True,
        title="test add noise",
        xlabel="t",
        ylabel="Amplitude",
    )
    graph.plot()

    # test function add_signal

    sin_wave = SinWave(
        a=2, f=50, fe=1000, ph=0, d=0.08, title="Une sinusoide", format="-bo"
    )
    sin_wave.make_wave()
    sin_wave_n = SinWave(
        a=2, f=50, fe=1000, ph=0, d=0.08, title="Une sinusoide", format="-bo"
    )
    sin_wave_n.make_wave()
    sin_square = SquareWave(
        a=1, f=50, fe=1000, ph=0, d=0.08, title="Un signal carré", format="-g."
    )
    sin_square.make_wave()
    sin_wave.add_signal(sin_square)

    l_sin = [sin_wave_n, sin_square, sin_wave]

    graph = Graph(
        waves=l_sin,
        plot_type="line",
        subplot=True,
        title="SinWave",
        xlabel="t",
        ylabel="Amplitude",
    )

    graph.plot()
