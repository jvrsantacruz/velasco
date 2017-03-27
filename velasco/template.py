# -*- coding: utf-8 -*-
"""Genera documento vacío que sirve como plantilla para los metadatos"""
import sys
import argparse

from parsing import Book, parse_mentions, write


def get_entries(books):
    return [dict(
        id=books[bid]['book_id'],
        title=books[bid]['title'],
        topic='',
        lang='',
        ref_old='',
        ref='',
        bb='',
    ) for bid in sorted(books.keys())]


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

        books[int(m['book_id'])] = m

    header = ('id', 'title', 'topic', 'lang', 'ref_old', 'ref', 'bb')
    write(get_entries(), args.output, header=header, format=args.format)


if __name__ == '__main__':
    main()
