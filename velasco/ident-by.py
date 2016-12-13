"""
Genera tabla con todos los libros, y marca si están en cada inventario, si los
identificó Lawrance, Paz o nadie a partir de la bibliografía extraida de la
BNE.
"""
import argparse
import operator
import itertools

from velasco.parsing import read, write

HEADER = ('id', 'referencia-precisa')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('table')
    parser.add_argument('bne')
    parser.add_argument('-o', '--output')
    args = parser.parse_args()

    table = read(args.table, types={'bid': int, 'lid': int})
    bne = read(args.bne, types={'id': int})

    books_listing = get_book_listings(table)
    records = generate_records(bne, books_listing)
    header = ('id', 'ref', '1', '2', '3', '4', 'Lawrance', 'Paz', 'BNE', 'bib')

    write(list(records), args.output, header=header)


def get_book_listings(table):
    byid = operator.itemgetter('bid')
    return {
        bid: {e['lid'] for e in entries} for bid, entries in
        itertools.groupby(sorted(table, key=byid), key=byid)
    }


def get_book_bne_meta(bne):
    return


def generate_records(bne, books):
    bne_meta = {e['id']: e for e in bne}

    for bid in sorted(books):
        entry = bne_meta.get(bid)
        if entry is None:
            entry = {'id': bid, 'ref': ''}

        bib = entry.get('referencia-precisa')
        if not bib:
            bib = ''

        data = {
            'id': entry['id'],
            'ref': entry['ref'],
            'bib': bib
        }

        data['Lawrance'] = 'X' if 'Lawrance' in bib or 'Lawrence' in bib else ''
        data['Paz'] = 'X' if 'Paz' in bib else ''
        data['BNE'] = 'X' if not (data['Lawrance'] or data['Paz']) else ''
        for lid in (1, 2, 3, 4, 5):
            data[str(lid)] = 'X' if lid in books[entry['id']] else ''

        yield data


if __name__ == "__main__":
    main()
