#!/bin/bash -eu

declare -r INVENTARIOS="$1"
declare -r METADATA="$2"
declare -r BNE="$3"
declare -r NAME="graficas"
declare -r DATE=$(date +"%Y-%m-%d_%H-%M-%S")
declare -r DIR="$NAME-$DATE"
declare -r TABLE="$DIR/table.csv"
declare -r BNE_TABLE="$DIR/bne.csv"

mkdir -p $DIR
python velasco/bne.py "$METADATA" "$BNE" --output $BNE_TABLE
python velasco/table.py "$INVENTARIOS" "$METADATA" "$BNE_TABLE" --output $TABLE

for name in todos tema idioma orden orden_uno fantasmas area height; do
    python plots/${name}.py $TABLE --save --output $DIR --ext png --dpi 200
done
for first in $(seq 1 5); do
    for second in $(seq 1 5); do
        if test $first -ne $second; then
            python plots/orden_orden.py $TABLE --output $DIR --ext png --dpi 200 \
                --first $first --second $second --save
        fi
    done
done
