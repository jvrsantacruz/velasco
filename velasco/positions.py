import click
import itertools
import xlsxwriter
import collections

from parsing import Book, write


@click.group()
def cli():
    """Generate book listing"""


def all_book_ids(book):
    return set(itertools.chain.from_iterable(page.entries_by_id.keys()
                                             for page in book.pages))


def books_with_listings(book):
    books = collections.defaultdict(list)
    for bid in all_book_ids(book):
        for page in book.pages:
            entries = page.entries_by_id.get(bid)
            books[bid].append(', '.join(str(entry['pos'] + 1) for entry in entries)
                              if entries else '')
    return sorted(
        ({'book_id': key, 'listings': value}
         for key, value in books.items()),
        key=lambda b: b['book_id'])


listings = [
    {'year': '1455'},
    {'year': '1553'},
    {'year': '1615'},
    {'year': '1647'},
    {'year': '1726'}
]


@cli.command()
def generate():
    book = Book('inventarios.xlsx')
    entries = books_with_listings(book)
    header = ['ID'] + [l['year'] for l in listings]
    entries = (
        dict(zip(header, [e['book_id']] + e['listings'])) for e in entries
    )
    write(entries, 'positions.xlsx', header=header)


def repeated_entries(book):
    for np, page in enumerate(book.pages):
        for book_id, entries in page.entries_by_id.items():
            if len(entries) > 1:
                yield (
                    book_id,
                    np,
                    ', '.join(map(str, (e['pos'] for e in entries))),
                    entries[0]['title']
                )


@cli.command()
def repeated():
    book = Book('inventarios.xls')
    header = ['ID', 'INVENTARIO', 'AÑO', 'POS', 'TEMA']
    entries = ([e[0], e[1] + 1, listings[e[1]]['year'], e[2], e[3]]
               for e in repeated_entries(book))
    export_to_excel('repeated.xlsx', header, entries)


def export_to_excel(filename, header, entries):
    book = xlsxwriter.Workbook(filename)
    sheet = book.add_worksheet()

    sheet.write_row(0, 0, header)
    for n, entry in enumerate(entries, 1):
        for c, datum in enumerate(entry):
            sheet.write(n, c, datum)

    book.close()


if __name__ == "__main__":
    cli()
