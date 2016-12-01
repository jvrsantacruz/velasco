# -*- coding: utf-8 -*-
import csv
import argparse

from parsing import read, write


def get(dct, bid, name):
    return dct.get(bid, {}).get(name, '')


def make_entry(data, header):
    return {k: data[k] for k in header}


def put(header, data):
    print(",".join(str(data[h]).replace(',', '') for h in header))


def load(path):
    with open(path) as stream:
        reader = csv.reader(stream, delimiter=',', quotechar='"')
        header = next(reader)
        return [dict(zip(header, row)) for row in reader]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('inventario')
    parser.add_argument('metadata')
    parser.add_argument('-o', '--output')
    parser.add_argument('-f', '--format')
    args = parser.parse_args()

    inventario = {r['ID']: r for r in read(args.inventario, types={'ID', int})}
    metadata = {r['id']: r for r in read(args.metadata, types={'id', int})}

    for bid in metadata:
        metadata[bid]['ref_old'] = old = get(inventario, bid, 'SIGNATURA ANTIGUA')
        metadata[bid]['ref'] = sig = get(inventario, bid, 'SIGNATURA ACTUAL')
        metadata[bid]['inc'] = inc = get(inventario, bid, 'INCUNABLE')
        metadata[bid]['bb'] = bb = (not bool(get(inventario, bid, 'BB'))) and ''
        metadata[bid]['exists'] = bool(bb != '' or inc or sig or old) or ''

    header = ('id', 'title', 'lid', 'pos', 'topic', 'lang',
              'ref_old', 'ref', 'inc', 'bb', 'exists')
    entries = (dict(zip(header, metadata[bid])) for bid in metadata)
    write(entries, args.output, header=header, format=args.format)


if __name__ == '__main__':
    main()
