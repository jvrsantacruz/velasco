import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from adjustText import adjust_text

from common import get_parser, get_args, plotting, read_table


variable_names = {
    'height': 'altura (cm)',
    'area': 'area (cm²)',
    'topic': 'tema',
    'lang': 'idioma',
    'author': 'autor',
}


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

    palette_name = None
    title = 'Orden/Orden inventarios {} y {}'\
        .format(args.first, args.second)
    if not args.color_by:
        # Color based on wether theyre in both inventaries or missing
        data['color'] = data.apply(
            lambda row: any(not row[c] for c in columns), 1)
    else:
        variable_name = variable_names.get(args.color_by, args.color_by)
        title += ' variable "{}"'.format(variable_name)
        data['color'] = data.apply(
            lambda row: meta.get_field(args.color_by, *[row[c] for c in columns]), 1)

    # Group numerical values in 5 bins/categories
    color_sorter = None
    if args.color_by in ['area', 'height']:
        palette_name = 'YlOrRd'  # yellow to red
        bins = 10 if args.color_by == 'height' else 5
        data['color'] = pd.cut(data['color'], bins, precision=0)
        def color_sorter(e):
            return float(str(e).strip('(').strip(']').split(', ', 1)[0])

    # Assure repeteable colors by setting category-color map
    # before lmplot does it randomly on each run and confuse us
    values = sorted(data['color'].unique(), key=color_sorter)
    colors = sns.color_palette(palette=palette_name, n_colors=len(values))
    palette = dict(zip(values, colors))

    # Use str as column names, otherwise lmplot goes wild
    columns = list(map(str, columns))
    data.columns = columns + ['color']

    p = sns.lmplot(*columns, data=data, hue='color',
                   palette=palette,
                   legend=False, legend_out=True,
                   fit_reg=False, size=7, aspect=1.3)

    # Set top title and space for it
    sns.plt.suptitle(title)
    p.fig.subplots_adjust(top=0.92)

    p.set(ylim=(0, None), xlim=(0, None))

    # Set legend outside graph at center right
    if args.color_by:
        p.fig.subplots_adjust(right=0.85)
        variable_name = variable_names.get(args.color_by, args.color_by)
        plt.legend(bbox_to_anchor=(1.18, 0.7), borderaxespad=0.,
                   title=variable_name)

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
        # for first, second, na in data.values:
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
