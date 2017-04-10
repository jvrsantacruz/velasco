import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from adjustText import adjust_text

from common import get_parser, get_args, plotting, read_table

def name_by_pos(df):
    return {pos: short for pos, short in df.ix[:, 'pos':'short'].values}


def main():
    parser = get_parser()
    parser.add_argument('--first', default=3, type=int)
    parser.add_argument('--second', default=4, type=int)
    parser.add_argument('--annotate', action='store_true')
    parser.add_argument('--iterations', default=500, type=int)
    args = get_args(__file__, parser)

    df = pd.DataFrame(read_table(args.table))
    data = df[(df.lid == args.first) | (df.lid == args.second)]\
        .drop_duplicates(['bid', 'lid'])\
        .pivot(index='bid', columns='lid', values='pos')\
        .sort_values(by=args.first)\
        .fillna(0)

    first_names = name_by_pos(df[df.lid == args.first])
    second_names = name_by_pos(df[df.lid == args.second])

    columns = [str(a) for a in [args.first, args.second]]
    data = pd.DataFrame(data.as_matrix())
    data.columns = columns

    data['na'] = data.apply(
        lambda row: any(not row[c] for c in columns), 1)

    p = sns.lmplot(*columns, data=data, hue='na', legend=False,
                   fit_reg=False, size=7, aspect=1.3)

    p.set(ylim=(0, None), xlim=(0, None))

    if args.annotate:
        texts = []
        for first, second, na in data.values:
            texts.append(p.ax.text(
                first, second,
                first_names.get(first) or second_names.get(second),
                fontsize=8,
            ))
            # plt.annotate(
            #     first_names.get(first) or second_names.get(second),
            #     #str((first, second)),
            #     xy=(first, second),
            #     xytext=(first + 1, second + 1),
            #     fontsize=8,
            # )

        adjust_text(texts, force_points=1.5, lim=args.iterations,
                    arrowprops=dict(arrowstyle="-", color='r', alpha=0.8))

    plotting(plt, args)


if __name__ == "__main__":
    main()
