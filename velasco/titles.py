# -*- coding: utf-8 -*-
import sys
import argparse

from parsing import Book, parse_mentions, write

YEARS = ["1455", "1553", "1615", "1647", "1726"]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('inventarios')
    parser.add_argument('-o', '--output')
    parser.add_argument('-f', '--format')
    args = parser.parse_args()

    books = {}
    for m in parse_mentions(Book(args.inventarios)):
        if not m['book_id']:
            print('Mention with empty id: {!r}'.format(m), file=sys.stderr)
            continue

        if m['book_id'] not in books:
            books[m['book_id']] = {}
        books[int(m['book_id'])][str(m['year'])] = m['title']

    header = ["ID Libro"] + YEARS

    write(titles_per_year(books, header), args.output,
          header=header, format=args.format)


def titles_per_year(books, header):
    for bid in sorted(books.keys()):
        line = [bid] + [books[bid].get(y, '').replace(',', '') for y in YEARS]
        yield dict(zip(header, line))


if __name__ == '__main__':
    main()
