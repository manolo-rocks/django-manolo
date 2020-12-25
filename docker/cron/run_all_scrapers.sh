#!/bin/bash

last_week=$(date --date='7 days ago' +"%Y-%m-%d")
today=$(date +"%Y-%m-%d")

scrapy_path=/code/scrapers/manolo_scraper
scrapy_bin=/usr/local/bin/scrapy

cd $scrapy_path

declare -a scrapers=(
    'ambiente' 'congreso' 'defensa' 'ingemmet' 'inpe' 'minagr' 'mincetur'
    'mincu' 'minedu' 'minem' 'minsa' 'minvi' 'osce' 'pcm' 'presidencia'
    'produce2' 'trabajo' 'midis'
)

for i in "${scrapers[@]}"; do
  $scrapy_bin crawl $i -a date_start=$last_week -a date_end=$today
done
