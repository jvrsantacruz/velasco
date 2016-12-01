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
    right = read(args.bne, types={'bid': int})
    merged = merge(list(left), list(right), key='id', right_key='bid')
    write(list(merged), args.output)
    # autor secundario
    # autor principal
    # desc fisica
    # volumenes
    # hojas
    # columnas
    # lineas
    # material
    # tamaño
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


if __name__ == "__main__":
    main()
