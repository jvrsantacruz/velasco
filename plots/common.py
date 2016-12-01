import os
import re
import argparse

from velasco.parsing import read


def uniquename(name, ext, path):
    name, _ = os.path.splitext(os.path.basename(name))
    number = max(
        [int(m.group(1)) for m in
         (re.match(r'^fig_' + name + r'_(\d+)\.' + ext + '$', n) for n in os.listdir(path))
         if m] or [0]
    )
    return 'fig_' + name + '_' + str(number + 1) + '.' + ext


def get_parser():
    return argparse.ArgumentParser()


def get_args(name='', parser=get_parser()):
    parser.add_argument('table')
    parser.add_argument('--name', default=name)
    parser.add_argument('--ext', default='svg')
    parser.add_argument('--output', default='.')
    parser.add_argument('--dpi', default=None, type=int)
    parser.add_argument('--save', default=False, action='store_true')
    return parser.parse_args()


def set_axis(ax, data, years, ylabel=''):
    ax.set_aspect(0.2)
    ax.set_ylabel('Libros')
    ax.set_xlabel('')
    ax.set_title('')
    ax.set_yticks(range(1, len(data) + 1))
    ax.set_yticklabels(reversed(list(
        str(n) if n == 1 or n % 10 == 0 or n == len(data) else ''
        for n in range(1, len(data) + 1)
    )), rotation=0, size=8)
    ax.set_xticklabels(map(str, sorted(set(years))), rotation=-75, size=8)

    # White lines
    [ax.axvline(i, linewidth=5.2, color="white") for i in range(7)]


def plotting(plt, args):
    if args.save:
        path = os.path.join(
            args.output,
            uniquename(args.name, args.ext, args.output)
        )
        print(path)
        plt.savefig(path, dpi=args.dpi)
    else:
        plt.show()


def legend(f, ax, labels, colors, x=0.25, y=0.1):
    import matplotlib.patches as mpatches

    box = ax.get_position()
    legend_ax = f.add_axes([x, y, 1, .1])
    legend_ax.axis('off')
    ax.set_position([box.x0, box.y0, box.width * 0.2, box.height])

    legend = legend_ax.legend(
        [mpatches.Patch(facecolor=c, edgecolor=c) for c in colors],
        labels, handlelength=0.6, loc='lower left'
    )
    for t in legend.get_texts():
        t.set_ha('left')


def categorical_by(df, column, names, fill='NA'):
    return df.pivot(index='pos', columns='lid', values=column)\
        .fillna(fill)\
        .replace(dict(zip(names, range(len(names)))))


def read_table(path):
    types = {'bid': int, 'bid': int, 'lid': int, 'year': int, 'pos': int}
    return read(path, types=types)
