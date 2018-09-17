"""Positional matrix chart colored by criteria"""
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

from velasco.parsing import read
from common import (get_args, plotting, categorical_by, legend, set_axis,
                    read_table, get_parser, as_letters)


def topic_config(df, key):
    names = ['NA', 'REL', 'CRONIC', 'ANTI']
    labels = ['N/A', 'Religioso', 'Crónicas y Leyes', 'Historia Antigua']
    colornames = ['light grey', 'pale red', 'medium green', 'denim blue']
    colors = sns.xkcd_palette(colornames)
    return categorical_by(df, key, names), labels, colors


def lang_config(df, key):
    names = ['NA', 'LAT', 'ROM', 'FRAN']
    labels = ['N/A', 'Latín', 'Romance', 'Francés']
    colornames = ['light grey', 'pale red', 'medium green', 'denim blue']
    colors = sns.xkcd_palette(colornames)
    return categorical_by(df, key, names), labels, colors


def height_config(df, key):
    df = df.pivot(index='pos', columns='lid', values=key).fillna(0)
    df[key] = pd.cut(df[key], 5)
    values = df[key].value_counts()
    labels = sorted(values.keys())
    colors = sns.color_palette(n_colors=len(labels))
    return df, labels, colors


def year_config(df, key):
    data = df\
        .drop_duplicates(['bid', 'lid'], keep='first')\
        .pivot(index='bid', columns='lid', values='year')\
        .fillna(False)
    colors = sns.light_palette('red', len(data))
    return data, [], colors


def bid_config(df, key):
    data = df.pivot(index='bid', columns='lid', values='bid')
    colors = sns.light_palette('navy', len(data))
    return data, [], colors


def uno_config(df, key):
    def track(row):
        # Mark it as id, which will go in red
        return 1000 if row['bid'] == 25 else row['bid']

    df['track'] = df.apply(track, axis=1)
    data = df.pivot(index='pos', columns='lid', values='track')
    colornames = ['light blue', 'bright red']
    colors = sns.xkcd_palette(colornames)
    return data, [], colors


def fantasmas_config(df, key):
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

    labels = ['N/A', 'Id. Física', 'Id. Historiográfica', 'Desconocido', 'Perdido']
    colornames = ['light grey', 'medium green', 'denim blue', 'pale red']

    df['ident'] = df.apply(categorize, axis=1)
    data = df\
        .drop_duplicates(['bid', 'lid'], keep='first')\
        .pivot(index='bid', columns='lid', values='ident')\
        .fillna(0)
    colors = sns.xkcd_palette(colornames)

    return data, labels, colors


def area_config(df, key):
    sizes = len(range(int(df['area'].max())))
    data = df.pivot(index='pos', columns='lid', values='area').fillna(0)
    colors = sns.light_palette('navy', sizes)
    return data, [], colors


def height_config(df, key):
    sizes = len(range(int(df['height'].max())))
    data = df.pivot(index='pos', columns='lid', values='height').fillna(0)
    colors = sns.light_palette('green', sizes)
    return data, [], colors


def author_config(df, key):
    data = df.pivot(index='bid', columns='lid', values='author').fillna('NA')
    colors = sns.light_palette('red', len(data))
    return data, [], colors


configs = {
    'height': height_config,
    'lang': lang_config,
    'topic': topic_config,
    'year': year_config,
    'bid': bid_config,
    'uno': uno_config,
    'fantasmas': fantasmas_config,
    'area': area_config,
    'height': height_config,
}


def print_list():
    print('\n'.join(configs))


def main():
    parser = get_parser()
    parser.add_argument('--list', action='store_true')
    parser.add_argument('--annotated', action='store_true')
    parser.add_argument('--color-by')
    args = get_args(__file__, parser)

    if args.list:
        print_list()
    else:
        plot(args)


def plot(args):
    df = pd.DataFrame(read_table(args.table))
    configurer = configs[args.color_by]
    data, labels, colors = configurer(df, args.color_by)

    f, ax = plt.subplots()

    fig = sns.heatmap(
        data,
        ax=ax,
        #square=True,
        linewidth=0.5,
        cmap=ListedColormap(colors),
        cbar=False
    )

    set_axis(ax, data, as_letters(set(df.year.values)), ylabel='Posición')
    legend(f, ax, labels, colors)

    if args.annotated and args.color_by in ['bid', 'year']:
        df_by_bid = df.drop_duplicates('bid').set_index('bid')
        texts = [
            fig.text(
                15,
                bid,
                df.loc[bid, 'short'],
                fontsize=8,
            )
            for bid, row in data.iterrows()
        ]

    plotting(plt, args)


if __name__ == "__main__":
    main()
