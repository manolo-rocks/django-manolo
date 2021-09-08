#!/bin/bash

# install to be run by bitbar as file in folder scripts of name crawl_pcm.4h.py
# folder ~/projects/scripts

PATH=$PATH:/usr/local/bin/

# gdate is a command for macOS
last_week=$(gdate --date="${2} days ago" +"%Y-%m-%d")
today=$(gdate +"%Y-%m-%d")

scrapy_path=/Users/carlosp420/projects/manolo.rocks-ani/scrapers/manolo_scraper
scrapy_bin=/Users/carlosp420/.virtualenvs/manolo/bin/scrapy
output_path=/tmp/

cd $scrapy_path
$scrapy_bin crawl $1 -a date_start=$last_week -a date_end=$today -o $output_path/$1.jl 2> /tmp/scraping_err.log
