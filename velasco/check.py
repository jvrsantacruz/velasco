# -*- coding: utf-8 -*-
import argparse

from parsing import Book, parse_mentions, write


HEADER = ('Inventario', 'Posición', 'Problema', 'Título')


def problem(m, msg):
    return dict(zip(HEADER, (m['list_id'] + 1, m['pos'] + 1, msg, m['title'])))


def find_problems(mentions):
    books = {}
    for m in mentions:
        bid = m['book_id']
        other = books.get(bid, {})

        if not bid:
            yield problem(m, 'No tiene ID')

        elif m['list_id'] == other.get('list_id'):
            yield problem(m, 'Repetido en el mismo inventario {!r}'.format(other))

        else:
            books[bid] = m

        # chars = set(m['title']).intersection('().,!?¿¡')
        # if chars:
        #     problem(m, 'Signos de puntuación en el título: {!r}'
        #             .format(' '.join(chars)))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('inventarios')
    parser.add_argument('-o', '--output')
    parser.add_argument('-f', '--format')
    args = parser.parse_args()

    problems = find_problems(parse_mentions(Book(args.inventarios)))
    write(problems, args.output, header=HEADER, format=args.format)


if __name__ == "__main__":
    main()
