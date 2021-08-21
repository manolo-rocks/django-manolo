#!/bin/bash

last_week=$(date --date="${2} days ago" +"%Y-%m-%d")
today=$(date +"%Y-%m-%d")

scrapy_path=/code/scrapers/manolo_scraper
scrapy_bin=/usr/local/bin/scrapy

echo $(date) $1 $2 >> /tmp/crawls.log

cd $scrapy_path
$scrapy_bin crawl $1 -a date_start=$last_week -a date_end=$today
