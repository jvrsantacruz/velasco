# -*- coding: utf-8 -*-
import argparse

from parsing import Book, parse_mentions, parse_metadata, read, write


def table_of_mentions(mentions, meta, bne, header):
    for n, mention in enumerate(mentions, 1):
        bmeta = meta[mention['book_id']]
        bbne = bne[mention['book_id']]
        yield dict(zip(header, (
            n,
            mention['book_id'],
            mention['list_id'],
            mention['year'],
            mention['pos'],
            bmeta['short'],
            mention['title'].replace(',', ''),
            bmeta['lang'] or 'NA',
            bmeta['topic'] or 'NA',
            bbne['area'] or 'Nan',
            bbne['height'] or 'Nan',
            bool(bmeta['ref'] or bmeta['ref_old']),
            bbne['material'] or 'NA',
            bbne['author'] or 'NA',
        )))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('inventarios')
    parser.add_argument('metadata')
    parser.add_argument('bne')
    parser.add_argument('-o', '--output')
    parser.add_argument('-f', '--format')
    args = parser.parse_args()
    header = ('mid', 'bid', 'lid', 'year', 'pos', 'short', 'title', 'lang',
              'topic', 'area', 'height', 'exists', 'material', 'author')

    meta = parse_metadata(args.metadata)
    meta = {int(m['id']): m for m in meta}
    bne = read(args.bne)
    bne = {int(b['id']): b for b in bne}
    mentions = parse_mentions(Book(args.inventarios))

    table = table_of_mentions(mentions, meta, bne, header)
    write(table, args.output, header=header, format=args.format)


if __name__ == '__main__':
    main()
