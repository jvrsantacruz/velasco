# -*- coding: utf-8 -*-
import argparse
from collections import defaultdict

from parsing import Book, parse_mentions, parse_metadata, write


HEADER = ('id', 'inventario', 'posicion', 'problema', 'titulo')


def problem(m, msg):
    if 'book_id' in m:
        return dict(zip(
            HEADER, (m['book_id'], m['list_id'] + 1, m['pos'] + 1, msg, m['title'])
        ))
    else:
        return dict(zip(
            HEADER, (m['id'], 'meta', '', msg, m['title'])
        ))


def repeated(sequence, field):
    byfield = defaultdict(list)
    [byfield[e[field]].append(e) for e in sequence]
    for name, entries in byfield.items():
        if name and len(entries) > 1:
            yield name, entries


def find_repes(sequence, field):
    for ref, entries in repeated(sequence, field):
        repes = ', '.join('{id}: ({title})'.format(**e) for e in entries)
        yield problem(
            entries[0],
            'El campo {} {!r} está repetido en varios libros: {}'
            .format(field, ref, repes)
        )


def find_meta_problems(meta):
    meta = list(meta)
    yield from find_repes(meta, 'ref')
    yield from find_repes(meta, 'ref_old')
    yield from find_repes(meta, 'id')
    yield from find_repes(meta, 'idx')


def find_mention_problems(mentions):
    books = {}
    for m in mentions:
        bid = m['book_id']
        other = books.get(bid, {})

        if not bid:
            yield problem(m, 'No tiene ID')

        elif m['list_id'] == other.get('list_id'):
            yield problem(
                m, 'Repetido en el mismo inventario {!r}'.format(other)
            )
        else:
            books[bid] = m

        chars = set(m['title']).intersection('().,!?¿¡')
        if chars:
            problem(m, 'Signos de puntuación en el título: {!r}'
                    .format(' '.join(chars)))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('inventarios')
    parser.add_argument('metadata')
    parser.add_argument('-o', '--output')
    parser.add_argument('-f', '--format')
    args = parser.parse_args()

    problems = []
    problems.extend(
        find_mention_problems(parse_mentions(Book(args.inventarios)))
    )
    problems.extend(
        find_meta_problems(parse_metadata(args.metadata))
    )
    write(problems, args.output, header=HEADER, format=args.format)


if __name__ == "__main__":
    main()
