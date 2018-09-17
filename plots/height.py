import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

from common import get_args, plotting, set_axis, read_table, as_letters


def main():
    args = get_args(__file__)

    df = pd.DataFrame(read_table(args.table))
    sizes = len(range(int(df['height'].max())))
    data = df.pivot(index='pos', columns='lid', values='height').fillna(0)
    #colors = sns.color_palette('cubehelix', sizes)
    #colors = sns.color_palette('hls', len(data))
    #colors = sns.color_palette('husl', len(data))
    #colors = sns.light_palette('red', sizes)
    #colors = sns.light_palette('navy', sizes)
    colors = sns.light_palette('green', sizes)

    f, ax = plt.subplots()

    sns.heatmap(
        data,
        ax=ax,
        square=True,
        linewidth=0.5,
        cmap=ListedColormap(colors),
        cbar=False
    )

    set_axis(ax, data, as_letters(set(df.year.values)), 'Tamaño')
    plotting(plt, args)


if __name__ == "__main__":
    main()
