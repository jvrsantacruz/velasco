import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from adjustText import adjust_text

from common import get_parser, get_args, plotting, read_table


def main():
    parser = get_parser()
    parser.add_argument('--first', default=3, type=int)
    parser.add_argument('--second', default=4, type=int)
    parser.add_argument('--annotated', action='store_true')
    parser.add_argument('--iterations', default=10, type=int)
    parser.add_argument('--color-by')
    args = get_args(__file__, parser)

    columns = [args.first, args.second]
    df = pd.DataFrame(read_table(args.table))
    data = df[(df.lid == args.first) | (df.lid == args.second)]\
        .pivot(index='bid', columns='lid', values='pos')\
        .sort_values(by=args.first)\
        .fillna(0)\
        .reindex_axis(columns, axis=1)  # assure column order

    # Reindex by position
    meta = Metadata(index='pos', dfs=[
        df[df.lid == args.first],
        df[df.lid == args.second]
    ])

    if not args.color_by:
        # Color based on wether theyre in both inventaries or missing
        data['color'] = data.apply(
            lambda row: any(not row[c] for c in columns), 1)
    else:
        data['color'] = data.apply(
            lambda row: meta.get_field(args.color_by, *[row[c] for c in columns]), 1)

    if args.color_by in ['area', 'height']:
        data['color'] = pd.cut(data['color'], 5)

    columns = list(map(str, columns))
    data.columns = columns + ['color']

    p = sns.lmplot(*columns, data=data, hue='color',
                   legend=bool(args.color_by),
                   fit_reg=False, size=7, aspect=1.3)

    p.set(ylim=(0, None), xlim=(0, None))

    if args.annotated:
        texts = [
            p.ax.text(
                first,
                second,
                meta.get_field('short', first, second),
                fontsize=8,
            )
            for first, second, color in data.values
        ]
        #for first, second, na in data.values:
        #    # plt.annotate(
        #    #     meta.get(first, second)['short'],
        #    #     #str((first, second)),
        #    #     xy=(first, second),
        #    #     xytext=(first + 1, second + 1),
        #    #     fontsize=8,
        #    # )

        adjust_text(texts, force_points=1.5, lim=args.iterations,
                    arrowprops=dict(arrowstyle="-", color='r', alpha=0.8))

    plotting(plt, args)


class Metadata:
    def __init__(self, index, dfs):
        self.datasets = [
            {row[index]: row for n, row in df.iterrows() if row[index]}
            for df in dfs
        ]

    def get(self, *indexes):
        for index, data in zip(indexes, self.datasets):
            if index in data:
                return data[index]

    def get_field(self, field, *indexes):
        data = self.get(*indexes)
        return float('NaN') if data is None else data[field]


if __name__ == "__main__":
    main()
