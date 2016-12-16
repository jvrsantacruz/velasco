import re
import argparse

from velasco.parsing import read, write, merge


def update_id(records):
    for entry in records:
        entry['bid'] = int(entry['bid'])
    return records


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('meta')
    parser.add_argument('bne')
    parser.add_argument('--output')
    args = parser.parse_args()

    left = read(args.meta, types={'id': int})
    right = read(args.bne, types={'id': int})
    books = merge(list(left), list(right), key='id')
    books = add_height_and_width(books)
    books = add_volume(books)

    header = ('id', 'title', 'lid', 'pos', 'topic', 'lang', 'ref_old', 'ref',
              'inc', 'bb', 'exists', 'height', 'width', 'area', 'vol')
    write(list(books), args.output, header=header)

    # tamaño
    # volumen

    # autor secundario
    # autor principal
    # desc fisica
    # volumenes
    # hojas
    # columnas
    # lineas
    # material
    # enlace
    # incipit
    # autor-person
    # area descripcion fis
    # lengua
    # procedencia
    # nota general
    # nota ilust
    # nota area publ (procedencia)
    # publicaciones
    # referencia precisa
    # termino genero
    # titulo
    # titulo lomo

def add_height_and_width(books):
    """parse "19 x 20 cm" within descriptions"""
    size_regex = re.compile('(\d+)\s*x\s*(\d+)\s*cm')
    for book in books:
        book['height'] = book['width'] = book['area'] = ''
        result = size_regex.findall(book.get('descripcion-fisica') or '')
        if result:
            book['height'] = int(result[0][0])
            book['width'] = int(result[0][1])
            book['area'] = book['height'] * book['width']

        yield book


def add_volume(books):
    """Find wether the reference is a volume of a series"""
    regex = re.compile('.* V.(\d+)$')
    for book in books:
        book['vol'] = 1
        for holding in book['holdings'] or ():
            match = regex.match(holding['codigo-de-barras'])
            if match:
                book['vol'] = int(match.group(1))

        yield book


if __name__ == "__main__":
    main()
