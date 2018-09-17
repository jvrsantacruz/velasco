"""Excel listing of the book catalog"""
import argparse

from velasco.parsing import read, write, parse_mentions, Book


HEADER = ('Pos', 'ID', 'Title', 'Referencia')


def generate_index(args):
    mentions = list(parse_mentions(Book(args.inventarios)))
    second_listing = sorted(
        [m for m in mentions if m['list_id'] == 2], key=lambda m: m['pos']
    )
    metadata = {r['id']: r for r in read(args.metadata, types={'id': int})}
    for mention in second_listing:
        bid = mention['book_id']
        ref_number = metadata[bid].get('ref')
        ref_text = 'BNE mss/{}'.format(ref_number) if ref_number else ''
        yield dict(zip(
            HEADER, 
            (mention['pos'], bid, mention['title'], ref_text)
        ))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('inventarios')
    parser.add_argument('metadata')
    parser.add_argument('--output')
    args = parser.parse_args()

    index = list(generate_index(args))
    write(index, args.output, header=HEADER)

if __name__ == '__main__':
    main()
