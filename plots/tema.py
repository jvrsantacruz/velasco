"""Positional matrix chart colored by theme"""
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

from velasco.parsing import read
from common import (get_args, plotting, categorical_by, legend, set_axis,
                    read_table, as_letters)


def main():
    args = get_args(__file__)

    names = ['NA', 'REL', 'CRONIC', 'ANTI']
    labels = ['N/A', 'Religioso', 'Crónicas y Leyes', 'Historia Antigua']
    colornames = ['light grey', 'pale red', 'medium green', 'denim blue']

    df = pd.DataFrame(read_table(args.table))
    #df = pd.read_csv(args.table)
    data = categorical_by(df, 'topic', names)
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

    set_axis(ax, data, as_letters(df.year.values), ylabel='Posición')
    legend(f, ax, labels, colors)
    plotting(plt, args)


if __name__ == "__main__":
    main()
