import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from common import get_parser, get_args, plotting, read_table


def main():
    parser = get_parser()
    parser.add_argument('--first', default=3, type=int)
    parser.add_argument('--second', default=4, type=int)
    args = get_args(__file__, parser)

    df = pd.DataFrame(read_table(args.table))
    data = df[(df.lid == args.first) | (df.lid == args.second)]\
        .drop_duplicates(['bid', 'lid'])\
        .pivot(index='bid', columns='lid', values='pos')\
        .sort_values(by=args.first)\
        .fillna(0)

    columns = [str(a) for a in [args.first, args.second]]
    data = pd.DataFrame(data.as_matrix())
    data.columns = columns

    data['na'] = data.apply(
        lambda row: any(not row[c] for c in columns), 1)

    p = sns.lmplot(*columns, data=data, hue='na',
                   fit_reg=False, size=7, aspect=1.3)
    p.set(ylim=(0, None), xlim=(0, None))
    plotting(plt, args)


if __name__ == "__main__":
    main()
