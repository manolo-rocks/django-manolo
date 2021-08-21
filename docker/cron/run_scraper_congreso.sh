#!/bin/bash

last_week=$(date --date="${1} days ago" +"%Y-%m-%d")
today=$(date +"%Y-%m-%d")

scrapy_path=/code/scrapers/manolo_scraper
scrapy_bin=/usr/local/bin/scrapy

cd $scrapy_path

$scrapy_bin crawl $2 -a date_start=$last_week -a date_end=$today
