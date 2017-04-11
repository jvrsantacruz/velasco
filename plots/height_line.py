import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.colors import ListedColormap

from common import get_args, plotting, legend, set_axis, read_table


def main():
    args = get_args(__file__)

    # TODO fix axis
    df = pd.DataFrame(read_table(args.table))\
        .pivot(index='pos', columns='lid')\
        .fillna(float('NaN'))

    title = 'Altura de libro por inventario y posición'

    plots = df.height.plot(kind='bar', subplots=True, title=title, grid=True)

    for plot in plots:
        plot.set_title('')
        plot.set_ylabel('')
        plot.legend(loc='upper right', bbox_to_anchor=(1.1, 1))

    visible = set(range(1, len(df), 5))
    for n, label in enumerate(plots[-1].xaxis.get_ticklabels()):
        label.set_visible(n + 1 in visible)

    plotting(plt, args)


if __name__ == "__main__":
    main()
