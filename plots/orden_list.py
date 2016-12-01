import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from common import get_parser, get_args, plotting, read_table


def main():
    parser = get_parser()
    parser.add_argument('--field', default='bid')
    args = get_args(__file__, parser)

    multiple = args.field != 'bid'

    def get_key(key):
        return key[1] if multiple else key

    def get_grouping():
        return ['bid', args.field] if multiple else 'bid'

    df = pd.DataFrame(read_table(args.table))
    palette = sns.color_palette('deep', df[args.field].size)
    colors = {key: palette[n] for n, key in
              enumerate(set(df[args.field].values))}

    fig, ax = plt.subplots(figsize=(15, 7.5))
    for key, grp in df.groupby(get_grouping()):
        grp.plot(ax=ax, kind='line', x='year', y='pos', c=colors[get_key(key)])

    miny, maxy = df.bid.min(), df.bid.max()
    for year in df.year.values:
        plt.plot((year, year), (miny, maxy), c='black', linewidth=0.6)

    plt.xticks(sorted(set(df.year.values)))
    ax.legend().remove()

    plotting(plt, args)


if __name__ == "__main__":
    main()
