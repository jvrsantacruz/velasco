# -*- coding: utf-8 -*-
import sys
import argparse

from parsing import Book, parse_mentions, parse_metadata, write


def table_of_mentions(mentions, meta, header):
    for n, mention in enumerate(mentions, 1):
        bmeta = meta[mention['book_id']]
        yield dict(zip(header, (
            n,
            mention['book_id'],
            mention['list_id'],
            mention['year'],
            mention['pos'],
            mention['title'].replace(',', ''),
            bmeta['lang'] or 'NA',
            bmeta['topic'] or 'NA',
            bool(bmeta['exists'])
        )))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('inventarios')
    parser.add_argument('metadata')
    parser.add_argument('-o', '--output')
    parser.add_argument('-f', '--format')
    args = parser.parse_args()
    header = ('mid', 'bid', 'lid', 'year', 'pos', 'title',
              'lang', 'topic', 'exists')

    meta = parse_metadata(args.metadata)
    meta = {int(m['id']): m for m in meta}
    mentions = parse_mentions(Book(args.inventarios))
    table = table_of_mentions(mentions, meta, header)
    write(table, args.output, header=header, format=args.format)


if __name__ == '__main__':
    main()
