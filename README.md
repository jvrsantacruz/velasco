# Velasco

1. Base datos (csv) sobre libros e inventarios
2. Consultas generadas
3. Gráficas
4. Extracción metadatos BNE

# Base de datos

La base de datos se compone de dos ficheros editables manualmente:

- inventarios
- metadata

El fichero *inventarios* es un excel de 5 páginas, cada una con las entradas de un inventario,
indicando un *id* y *titulo* con el texto. Cada entrada que refiere al mismo libro tiene el mismo
*id*.

El fichero *metadata* es un excel/csv que incluye información extra para cada libro reconocido a
partir de los inventarios. Ahí es posible indicar características físicas tales como el soporte o
el idioma en el que se encuentra escrito o referencias externas como su signatura en la BNE.

Estos ficheros son *editables manualmente*, su información puede actualizarse, cambiarse o
modificarse a mano empleando excel o cualquier editor de texto con el fin de ampliar campos o
incluir nuevos datos, siempre que se mantenga la coherencia entre identificadores.

# Ficheros generados

A partir de los dos ficheros de *base de datos*, existen muchos otros derivados que son generados
automáticamente por alguno de los scripts incluidos en la base de código. Estos ficheros suelen ser
coyunturales, deben regenerarse cuando la base de datos cambie y pueden borrarse ya que son
susceptibles de ser generados de nuevo.

- *table*: Crea una tabla con cada entrada del inventario mezclada con sus metadatos. Es el
  principal fichero, ya que a partir de el se generan todas las gráficas.
- *template*: Crea la tabla *metadata* vacía lista para empezar a rellenar.
- *bne*: Toma la información extraida del catálogo de la BNE y la une a la de *metadata*.
- *ident-by*: A partir del catálogo de la BNE y de otros, indica quién identificó cada libro.

# Gráficas

Las gráficas pueden generarse todas con un script llamado *plotall.sh*.
El script necesita que exista el fichero *table.csv* en el mismo directorio.

./plotall.sh

# Catálogo BNE

Se extrae información del catálogo de la Biblioteca Nacional para los libros cuya signatura es
conocida y se encuentra en la BNE. El programa visita la página del catálogo y extrae la
mucha de la información disponible.

Puede ejecutarse empleando el script `scraper.sh` pasándole el fichero de metadatos; el resultado
será un fichero `bne-DATE.jl` situado en el directorio de ejecución:

    ./scraper.sh metadata.xlsx

O manualmente desde el directorio del proyecto bne/bne:

    scrapy crawl -a metadata_path="/path/to/metadata" catalogo
    scrapy runspider spiders/catalogo.py -a metadata_path="/path/to/metadata"

El resultado quedará en un fichero llamado *records.jl*.

# Dependencias

sudo apt-get install python3-tk
