# -*- coding: utf-8 -*-
import sys
import argparse

from parsing import Book, parse_mentions

def put(*args):
    print(",".join(str(arg).replace(',', '') for arg in args))


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

    put('id', 'title', 'lid', 'pos', 'topic', 'lang')
    for bid in sorted(books.keys()):
        m = books[bid]
        put(m['book_id'], m['title'], m['list_id'], m['pos'], '', '')


if __name__ == '__main__':
    main()
