#!/bin/bash -eu

mkdir graficas
for name in todos tema idioma orden orden_uno fantasmas; do
    python plots/${name}.py table.csv --save --output graficas --ext png --dpi 200
done
