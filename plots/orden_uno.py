import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

from common import get_args, plotting, set_axis, read_table


def main():
    args = get_args(__file__)

    df = pd.DataFrame(read_table(args.table))

    def track(row):
        # Mark it as id, which will go in red
        return 1000 if row['bid'] == 25 else row['bid']

    df['track'] = df.apply(track, axis=1)
    data = df.pivot(index='pos', columns='lid', values='track')
    colornames = ['light blue', 'bright red']
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

    set_axis(ax, data, set(df.year.values), 'Posición')
    plotting(plt, args)


if __name__ == "__main__":
    main()
