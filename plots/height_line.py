import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

from common import get_args, plotting, legend, set_axis, read_table


def main():
    args = get_args(__file__)

    f, ax = plt.subplots()
    # TODO fix axis
    pd.DataFrame(read_table(args.table))\
        .pivot(index='pos', columns='lid')\
        .fillna(float('NaN'))\
        .height\
        .plot\
        .bar(subplots=True)
    plotting(plt, args)


if __name__ == "__main__":
    main()
