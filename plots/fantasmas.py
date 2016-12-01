import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

from common import get_args, plotting, set_axis, legend, read_table


def categorize(row):
    # Identificación física
    if row['exists'] and row['bid'] <= 166:
        return 1

    # Identificación historiográfica
    if row['bid'] <= 166:
        return 2

    # Fantasma!
    if row['bid'] > 166:
        return 3

    return 0


def main():
    args = get_args(__file__)

    labels = ['N/A', 'Id. Física', 'Id. Historiográfica', 'Desconocido', 'Perdido']
    colornames = ['light grey', 'medium green', 'denim blue', 'pale red']

    df = pd.DataFrame(read_table(args.table))
    df['ident'] = df.apply(categorize, axis=1)
    data = df\
        .drop_duplicates(['bid', 'lid'], keep='first')\
        .pivot(index='bid', columns='lid', values='ident')\
        .fillna(0)

    #colors = sns.color_palette('hls', len(data))
    #colors = sns.color_palette('husl', len(data))
    #colors = sns.light_palette('red', len(data))
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
