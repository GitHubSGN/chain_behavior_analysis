from matplotlib import pyplot as plt


def plot_hist(data_plot, title=None, output_file=None, show_plot=False):
    # draw distributions
    plt.figure(figsize=(10, 10))
    plt.hist(data_plot, 100, histtype='stepfilled')

    if title:
        plt.title(title.replace('\t', ' '))  # performance metric strings came with tabs to be removed.

    if output_file:
        plt.savefig(output_file)

    if show_plot:
        plt.show()

    plt.close()
