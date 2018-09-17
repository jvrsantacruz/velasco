#!/bin/bash -eu

declare -r INVENTARIOS="$1"
declare -r METADATA="$2"
declare -r BNE="$3"
declare -r NAME="graficas"
declare -r DATE=$(date +"%Y-%m-%d_%H-%M-%S")
declare -r DIR="${4:-"$NAME-$DATE"}"
declare -r TABLE="$DIR/table.csv"
declare -r BNE_TABLE="$DIR/bne.csv"
declare -r NTASKS=8


function plot_with_args {
    local script=$1
    shift
    local args="$@"

    set -x
    python plots/${script}.py $TABLE $args \
        --save --output $DIR --ext png --dpi 200
    set +x
}


function plot_orden {
    local first=$1
    local second=$2

    python plots/orden_orden.py $TABLE\
        --ext png --dpi 200 --save --output $DIR\
        --first $first --second $second\
        --name "orden_orden_${first}_vs_${second}_simple"

    python plots/orden_orden.py $TABLE\
        --ext png --dpi 200 --save --output $DIR\
        --first $first --second $second --annotated\
        --name "orden_orden_${first}_vs_${second}_annotated"

    for criteria in topic lang height area material author; do
        python plots/orden_orden.py $TABLE\
            --ext png --dpi 200 --save --output $DIR\
            --first $first --second $second --color-by $criteria\
            --name "orden_orden_${first}_vs_${second}_${criteria}"

        python plots/orden_orden.py $TABLE\
            --ext png --dpi 200 --save --output $DIR\
            --first $first --second $second --color-by $criteria --annotated\
            --name "orden_orden_${first}_vs_${second}_${criteria}_annotated"
    done
}


function wait_some {
    while test "$(jobs -p | wc -l)" -gt $NTASKS; do
        wait "$(jobs -p | head -n 1)"  || true
    done
}


function wait_all {
    for pid in $(jobs -p); do wait $pid; done
}


mkdir -p $DIR
python velasco/bne.py "$METADATA" "$BNE" --output $BNE_TABLE
python velasco/table.py "$INVENTARIOS" "$METADATA" "$BNE_TABLE" --output $TABLE

for script in height_line; do
    plot_with_args "$script" &
done

for name in $(python plots/squares.py --list $TABLE); do
    plot_with_args "squares" --color-by "$name" --name "squares_$name"  &
done
wait_some

for first in $(seq 1 5); do
    for second in $(seq 1 5); do
        if test $first -ne $second; then
            plot_orden "$first" "$second" &
        fi
    done
    wait_some
done
wait_all
