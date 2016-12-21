import re
import argparse

from velasco.parsing import read, write, merge


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('meta')
    parser.add_argument('bne')
    parser.add_argument('-o', '--output')
    args = parser.parse_args()

    left = read(args.meta, types={'id': int})
    right = read(args.bne, types={'id': int})
    books = merge(list(left), list(right), key='id')
    books = add_height_and_width(books)
    books = add_volume(books)
    books = add_volumes(books)
    books = add_material(books)
    books = add_columns(books)
    books = add_lines(books)
    books = add_author(books)

    header = ('id', 'lid', 'pos', 'title', 'author', 'topic', 'lang',
              'ref_old', 'ref', 'inc', 'bb', 'exists', 'height', 'width',
              'area', 'vol', 'vols', 'material', 'columns', 'lines')
    write(list(books), args.output, header=header)

    # tamaño
    # volumen
    # material
    # volumenes
    # lineas
    # columnas
    # autor

    # referencia precisa
    # autor principal
    # desc fisica
    # hojas
    # enlace
    # incipit
    # area descripcion fis
    # lengua
    # procedencia
    # nota general
    # nota ilust
    # nota area publ (procedencia)
    # publicaciones
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


def add_volumes(books):
    """Find wether the reference is series"""
    regex = re.compile(r'.* V.(\d+)$', re.IGNORECASE)
    for book in books:
        holdings = book.get('holdings') or ()
        matches = (regex.match(h['codigo-de-barras']) for h in holdings)
        vols = [int(match.group(1)) for match in matches if match]
        book['vols'] = max(vols or [1])
        yield book


def add_volume(books):
    """Find out which volume of the series the book is"""
    regex = re.compile(r'.* V.(\d+)$')
    for book in books:
        book['vol'] = 1
        if book['ref']:
            regex = re.compile(r'{} V.(\d+)$'.format(book['ref']),
                               re.IGNORECASE)
            holdings = book.get('holdings') or ()
            matches = [regex.match(h['codigo-de-barras']) for h in holdings]
            numbers = [int(match.group(1)) for match in matches if match]
            if numbers:
                book['vol'] = numbers[0]

        yield book


def add_material(books):
    for book in books:
        book['material'] = ','.join(
            m.replace('.', '')
            for m in ('perg.', 'vitela', 'papel')
            if m in (book['descripcion-fisica'] or '')
        )
        yield book


def add_columns(books):
    regex = re.compile('(\d+) col\.')
    for book in books:
        book['columns'] = ''
        matches = regex.findall(book['descripcion-fisica'] or '')
        if matches:
            book['columns'] = int(matches[0])
        yield book


def add_lines(books):
    regex = re.compile('(\d+) lín\.')
    for book in books:
        desc = book['descripcion-fisica']
        if desc:
            matches = regex.findall(desc)
            if matches:
                book['lines'] = int(matches[0])
            elif 'lín. var.' in desc:
                book['lines'] = 'var'
            else:
                book['lines'] = ''

        yield book


def add_author(books):
    for book in books:
        book['author'] = book.get('autor-personal') or ''
        yield book


if __name__ == "__main__":
    main()
