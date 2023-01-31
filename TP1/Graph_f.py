import matplotlib.pyplot as plt


class Graph:

    def __init__(self, waves, plot_type="line", subplot=False, title="Graph", xlabel="t", ylabel="A"):
        self.waves = waves
        self.plot_type = plot_type
        self.subplot = subplot
        self.title = title
        self.xlabel = xlabel
        self.ylabel = ylabel

    def plot(self):
        if not self.subplot:
            fig, ax = plt.subplots(sharex=True, sharey=True, figsize=(10, 10), dpi=100)
            ax.set_title(self.title)
            ax.set_xlabel(self.xlabel)
            ax.set_ylabel(self.ylabel)
            for wave in self.waves:
                if self.plot_type == "line":
                    wave.plot_on_ax(ax)
                elif self.plot_type == "scatter":
                    wave.scatter_on_ax(ax)
            ax.grid(True)
            plt.show()
        else:
            fig, ax = plt.subplots(len(self.waves), 1, sharex=True, sharey=True, figsize=(10, 10), dpi=100)
            for i, wave in enumerate(self.waves):
                ax[i].set_title(wave.title)
                ax[i].set_xlabel(self.xlabel)
                ax[i].set_ylabel(self.ylabel)
                if self.plot_type == "line":
                    wave.plot_on_ax(ax[i])
                elif self.plot_type == "scatter":
                    wave.scatter_on_ax(ax[i])
            plt.tight_layout()
            plt.show()
