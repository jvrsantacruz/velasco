import re
import itertools

import click

from parsing import Book, parse_listing


def title_key(title, keys):
    """Get a title key from full title"""
    title = title.lower()

    # remove comments
    title = re.sub(r'\([^)]+\)', '', title)

    # remove supositions
    title = re.sub(r'¿[^?]+?', '', title)

    # remove unwanted characters
    removals = ('¿', '?', ',', '.', ';', ':', '(', ')')
    for removal in removals:
        title = title.replace(removal, '')

    # cleanup old weird characters
    substitutions = (
        ('çe', 'ce'), ('ça', 'za'), ('ço', 'zo'), ("d'", "de "),
        ("d´", "de "), ('í', 'i'), ('á', 'a'), ('é', 'e'), ('í', 'i'),
        ('ó', 'o'), ('ff', 'f'), ('ú', 'u'), ('ss', 's'),
        ('coronica', 'cronica'),
        ('coronica', 'cronica'), ('ystoria', 'historia'),
        ('zirimonial', 'ceremonial'), ('çi', 'ci'),
        ('yngalaterra', 'inglaterra'), ('rrey', 'rey'), ('reyno', 'reino'),
        ('ynventores', 'inventores'), ('corronica', 'cronica'),
        ('prouidencia', 'prudencia'), ('hordenanzas', 'ordenanzas'),
        ('ynos', 'himnos'), ('prezeptos', 'preceptos'), ('quarto', 'cuarto'),
        ('zion', 'cion'), ('uiexo', 'viejo'), ('ficieron', 'hicieron'),
        ('savios', 'sabios'), ('fizo', 'hizo'), ('sarrazina', 'sarracena'),
        ('chronica', 'cronica'), ('briviario', 'breviario'),
        ('ordinazones', 'ordenanzas'), ('franzes', 'frances'),
        ('ytali', 'itali'), ('rbtoricae', 'retorica'),
        ('Bocavulario', 'Vocabulario'), ('cognominado', 'denominado')
    )
    for this, that in substitutions:
        title = title.replace(this, that)

    # remove numbers, articles and common words
    articles = set(['en', 'el', 'de', 'del', 'la', 'las', 'los', 'les', 'por',
                    'otro', 'otros', 'que', 'un', 'se', 'y'])
    common_words = set(['libro', 'dos', 'sobre', 'latin', 'rromanze',
                        'romance', 'rromanzw', 'romanze', 'rromance',
                        'yntitula', '(sic)', 'breve', 'pergamino', 'yntituta',
                        'yntitulado', ''])
    words = [word for word in title.split()
                     if re.match('\w+', word)
                     and word not in articles
                     and word not in common_words]

    # sort words by 'importance' (length and first aparition)
    words = sorted(words, reverse=True,
                   key=lambda w: (len(w), len(w) - words.index(w)))

    # cut long words that cope the identifier
    if sum(1 for word in words if len(word) > 4) > 1:
        words = (word[:5] for word in words)

    # Generate unique ids
    num = 1
    title = ''.join(words)[:9] + str(num)
    while title in keys:
        num += 1
        title = title[:-1] + str(num)

    return title


def export_to_excel(filename, entries):
    import xlsxwriter

    book = xlsxwriter.Workbook(filename)
    sheet = book.add_worksheet()
    format = book.add_format({'align': 'right'})

    sheet.set_column('B:B', 12)
    sheet.set_column('C:C', 200)

    sheet.write_row(0, 0, ['ID', 'CLAVE', 'TEMA'])
    for n, entry in enumerate(entries, 1):
        sheet.write(n, 0, entry['book_id'], format)
        sheet.write(n, 1, entry['key'])
        sheet.write(n, 2, entry['title'])

    book.close()


def export_to_latex(filename, entries):
    template = u"""
\\documentclass[a4paper,landscape]{article}
\\usepackage[margin=0.1in]{geometry}
\\pagestyle{empty}

\\usepackage{pdflscape}
\\usepackage[utf8]{inputenc}
\\usepackage[T1]{fontenc}
\\usepackage[spanish]{babel}
\\usepackage{supertabular}

\\begin{document}

\\twocolumn
\\tablehead{ID & Clave & Tema \\\\}


\\begin{supertabular}{|l|c|p{10cm}}
    %s
\\end{supertabular}

\\end{document}
    """
    rows = ' \\\\ \n '.join(' & '.join((str(e['book_id']), '\\large ' + e['key'], e['title']))
                     for e in entries)
    rows = rows.replace('´', "'") + '\\\\'
    with open(filename, 'w') as stream:
        stream.write(template % rows)


@click.group()
def cli():
    """Generate book listing"""


@cli.command()
def generate():
    """Generate listing.xlsx from inventarios.xls"""
    book = Book('inventarios.xls')
    pages = list(book.pages)
    pages = [pages[1], pages[0]] + pages[2:]
    entries = list(itertools.chain.from_iterable(p.entries for p in pages))
    keys = {}
    books = {}
    for entry in entries:
        if entry['book_id'] in books:
            continue

        entry['key'] = title_key(entry['title'], keys)
        print(entry['key'], '\t', entry['title'])

        # mark entry
        keys[entry['key']] = True
        books[entry['book_id']] = True

    entries = (e for e in entries if 'key' in e)
    entries = sorted(entries, key=lambda e: e['book_id'])
    export_to_excel('listing.xlsx', entries)


@cli.command()
@click.argument('filename', type=click.Path(dir_okay=False, exists=True))
@click.argument('output', type=click.Path(dir_okay=False))
def renumber(filename, output):
    """Rename identifiers in listings"""
    def renumber_key(entry):
        entry['book_id'] = "{:03d}".format(entry['book_id'])
        entry['key'] = ''.join(c for c in entry['key'] if not c.isdigit())
        entry['key'] = "{}{}".format(entry['book_id'], entry['key'])
        return entry

    export_to_excel(output, map(renumber_key, parse_listing(filename)))


@cli.command()
@click.argument('filename', type=click.Path(dir_okay=False, exists=True))
def tex(filename):
    """Export existing listing xls file to LaTeX"""
    entries = [entry for entry in parse_listing(filename)]
    export_to_latex('listing.tex', entries)


if __name__ == "__main__":
    cli()
