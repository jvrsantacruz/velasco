#!/bin/bash -eu

function archive {
    local filename="$1"

    mkdir -p old
    mv $filename old/$filename-$(date +"%Y-%m-%d_%H-%M-%S")
}

archive "$1"
