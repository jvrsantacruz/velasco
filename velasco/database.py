import os
import sqlite3
import argparse

from parsing import Book, parse_mentions, parse_metadata, read, write


BOOKS_HEADER = ('id', 'key', 'title', 'ref', 'ref_old', 'lang', 'topic',
                'area', 'width', 'height', 'existent', 'material', 'author')
LISTINGS_HEADER = ('id', 'key', 'code', 'title', 'year')
MENTIONS_HEADER = ('id', 'listing_id', 'book_id', 'pos', 'title')


def table_of_books(mentions, meta, bne):
    for n, key in enumerate(sorted(meta)):
        m = meta[key]
        b = bne.get(key) or {}
        yield dict(zip(BOOKS_HEADER, (
            n,
            key,
            m['title'] or b['titulo-uniforme'] or b['titulo'],
            m['ref'] or '',
            m['ref_old'] or '',
            m['lang'] or '',
            m['topic'] or '',
            b.get('area') or '',
            b.get('height') or '',
            b.get('width') or '',
            bool(m['ref'] or m['ref_old']),
            b.get('material') or '',
            b.get('author') or '',
        )))


def table_of_listings(mentions, meta, bne):
    listing_keys = sorted(set(m['list_id'] for m in mentions))
    years = [1455, 1553, 1615, 1647, 1726]
    letters = ['A', 'B', 'C', 'D', 'E', 'F']
    for n, lid in enumerate(listing_keys):
        yield dict(zip(LISTINGS_HEADER, (
            int(n),  # id
            int(lid),  # key
            letters[n],  # code
            'Inventario {} {} ({})'.format(lid, letters[n], years[n]),
            years[n]
        )))


def table_of_mentions(mentions, meta, bne):
    for n, mention in enumerate(mentions, 0):
        yield dict(zip(MENTIONS_HEADER, (
            n,  # id
            int(mention['list_id']) - 1,  # list id
            int(mention['book_id']) - 1,
            int(mention['pos']),
            mention['title'].replace(',', ''),
        )))


def dump_to_csv(args, books_table, listings_table, mentions_table):
    write(
        books_table,
        os.path.join(args.output, 'books.csv'),
        header=BOOKS_HEADER,
    )
    write(
        listings_table,
        os.path.join(args.output, 'listings.csv'),
        header=LISTINGS_HEADER,
    )
    write(
        mentions_table,
        os.path.join(args.output, 'mentions.csv'),
        header=MENTIONS_HEADER,
    )


def dump_to_db(args, books_table, listings_table, mentions_table):
    conn = sqlite3.connect(args.db)
    cursor = conn.cursor()

    if args.schema:
        cursor.executescript(open(args.schema).read())
        conn.commit()

    insert_into_table(cursor, 'books', BOOKS_HEADER, books_table)
    insert_into_table(cursor, 'listings', LISTINGS_HEADER, listings_table)
    insert_into_table(cursor, 'mentions', MENTIONS_HEADER, mentions_table)
    conn.commit()


def insert_into_table(cursor, table_name, header, values):
    books_values = ','.join(['?'] * len(header))
    statement = 'INSERT INTO {} VALUES ({})'.format(table_name, books_values)
    cursor.executemany(statement, [[m[h] for h in header] for m in values])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('inventarios')
    parser.add_argument('metadata')
    parser.add_argument('bne')
    parser.add_argument('-o', '--output', default='.')
    parser.add_argument('-d', '--db')
    parser.add_argument('-s', '--schema')
    args = parser.parse_args()
    meta = parse_metadata(args.metadata)
    meta = {int(m['id']): m for m in meta}
    bne = read(args.bne)
    bne = {int(b['id']): b for b in bne}
    mentions = list(parse_mentions(Book(args.inventarios)))

    books_table = table_of_books(mentions, meta, bne)
    listings_table = table_of_listings(mentions, meta, bne)
    mentions_table = table_of_mentions(mentions, meta, bne)
    if args.db:
        dump_to_db(args, books_table, listings_table, mentions_table)
    else:
        dump_to_csv(args, books_table, listings_table, mentions_table)


if __name__ == '__main__':
    main()
