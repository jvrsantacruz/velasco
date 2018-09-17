import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

from common import get_args, plotting, set_axis, read_table, as_letters


def main():
    args = get_args(__file__)

    df = pd.DataFrame(read_table(args.table))
    data = df.pivot(index='pos', columns='lid', values='bid')
    # colors = sns.color_palette('hls', len(data))
    # colors = sns.color_palette('husl', len(data))
    # colors = sns.light_palette('red', len(data))
    colors = sns.light_palette('navy', len(data))

    f, ax = plt.subplots()

    sns.heatmap(
        data,
        ax=ax,
        square=True,
        linewidth=0.5,
        cmap=ListedColormap(colors),
        cbar=False
    )

    set_axis(ax, data, as_letters(set(df.year.values)), 'Posición')
    plotting(plt, args)


if __name__ == "__main__":
    main()
