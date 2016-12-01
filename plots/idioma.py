import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

from common import (get_args, plotting, categorical_by, legend, set_axis,
                    read_table)


def main():
    args = get_args(__file__)

    names = ['NA', 'LAT', 'ROM', 'FRAN']
    labels = ['N/A', 'Latín', 'Romance', 'Francés']
    colornames = ['light grey', 'pale red', 'medium green', 'denim blue']

    df = pd.DataFrame(read_table(args.table))
    data = categorical_by(df, 'lang', names)
    colors = sns.xkcd_palette(colornames)

    f, ax = plt.subplots()

    sns.heatmap(
        data,
        ax=ax,
        square=True,
        linewidth=0.5,
        cmap=ListedColormap(colors),
        cbar=False
    )

    set_axis(ax, data, set(df.year.values), 'Libros')
    legend(f, ax, labels, colors)
    plotting(plt, args)


if __name__ == "__main__":
    main()
