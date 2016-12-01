import itertools

import click
import pandas as pd
import numpy as np

from bokeh.charts import HeatMap, output_file, show
from bokeh.layouts import column, gridplot
from bokeh.palettes import RdYlGn6, RdYlGn9
from bokeh.plotting import figure, ColumnDataSource

from parsing import Book, parse_mentions


listings = [
    {'year': '1455'},
    {'year': '1553'},
    {'year': '1615'},
    {'year': '1647'},
    {'year': '1726'}
]


def all_book_ids(book):
    return sorted(set(itertools.chain.from_iterable(page.entries_by_id.keys()
                                                    for page in book.pages)))


def books_by_listing(book):
    for bid in all_book_ids(book):
        for n, page in enumerate(book.pages):
            present = bool(page.entries_by_id.get(bid))
            if present:
                yield dict(book=bid, year=listings[n]['year'], present=present)


click.echo('Loading')


def add_listing_appearances(mentions):
    from collections import defaultdict
    books = defaultdict(list)
    mentions = tuple(mentions)

    for mention in mentions:
        listings = books[mention['book_id']]
        listings.append(mention['list_id'])
        mention['listings'] = listings

    return mentions


def filter_single_mentions(mentions):
    for mention in mentions:
        listings = mention['listings']
        if len(listings) != 1 or 0 in listings:
            yield mention


def colorize_mentions(mentions):
    for mention in mentions:
        mention['color'] = '#F2C8D2'
        yield mention


def colorize_single_mentions(mentions):
    for mention in mentions:
        listings = mention['listings']
        if len(listings) == 1 and listings[0] != 0:
            #mention['color'] = '#FBEEF1'
            mention['color'] = '#D2F2C8'
        yield mention


def colorize_gaps(mentions):
    done = set()

    for mention in mentions:
        if mention['book_id'] not in done:
            lists = mention['listings']
            missing = set(range(min(lists), max(lists) + 1)) - set(lists)
            for n in missing:
                submention = dict(mention)
                submention['list_id'] = n
                submention['year'] = listings[n]['year']
                submention['color'] = '#C8D2F2'
                done.add(submention['book_id'])
                yield submention

        yield mention


mentions = parse_mentions(Book('inventarios.xls'))
mentions = add_listing_appearances(mentions)
mentions = colorize_mentions(mentions)
mentions = colorize_single_mentions(mentions)
mentions = colorize_gaps(mentions)
mentions = sorted(mentions, key=lambda m: (m['book_id'], m['list_id']))
books = list(map(str, sorted(set(m['book_id'] for m in mentions))))
years = sorted(set(m['year'] for m in mentions))
data = {
    'book': [m['key'] for m in mentions],
    'year': [m['year'] for m in mentions],
    'color': [m['color'] for m in mentions],
}

#p = HeatMap(data, x='book', y='year', values='present', stat=None,
#              width=1000, plot_height=300, spacing_ratio=0.9)

source = ColumnDataSource(data=data)
p = figure(title="Books", y_range=years, x_range=books)

#p.plot_width = 900
p.plot_height = 200

p.rect("book", "year", 1, 1, source=source, color=data['color'], line_color="#999999")

p.grid.grid_line_color = None
p.axis.axis_line_color = None
p.axis.major_tick_line_color = None
p.axis.major_label_text_font_size = "3pt"
p.axis.major_label_standoff = 0
p.xaxis.major_label_orientation = np.pi/3

click.echo('Plotting')
#output_file("heatmap.html", title="heatmap.py example")

show(p)
