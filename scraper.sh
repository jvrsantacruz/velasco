#!/bin/bash -eu
# Usage: ./scraper.sh metadata.xlsx
# Output bne-$DATE.jl in same directory

declare -r META="$(echo "$PWD/${1#./}")"

echo "Starting to collect data from BNE"
(
  cd bne/bne
  scrapy crawl -a metadata_path="$META" catalogo
  mv records.jl ../../bne-$(date +"%Y-%m-%d_%H-%M-%S").jl
)
echo "Finished collecting data from BNE"
