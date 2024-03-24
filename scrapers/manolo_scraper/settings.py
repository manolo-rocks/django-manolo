# -*- coding: utf-8 -*-

# Scrapy settings for manolo_scraper project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath('..')))

os.environ['DJANGO_SETTINGS_MODULE'] = 'manolo.settings.production'

# This is required only if Django Version > 1.8
import django  # noqa
django.setup()

CONCURRENT_REQUESTS = 1
CONCURRENT_REQUESTS_PER_DOMAIN = 1
DOWNLOAD_DELAY = 5

BOT_NAME = 'bingbot'

SPIDER_MODULES = ['manolo_scraper.spiders']
NEWSPIDER_MODULE = 'manolo_scraper.spiders'
HTTPERROR_ALLOWED_CODES = [400]

# activate for splash
# SPIDER_MIDDLEWARES = {
#     'scrapy_splash.SplashDeduplicateArgsMiddleware': 100,
# }
# DUPEFILTER_CLASS = 'scrapy_splash.SplashAwareDupeFilter'
# SPLASH_URL = 'http://IP:8050'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = "Mozilla/5.0 (Linux; Android 4.0.4; Galaxy Nexus Build/IMM76B) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.133 Mobile Safari/535.19"  # noqa

CRAWLERA_ENABLED = False

DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': 500,
    'scrapy.downloadermiddlewares.cookies.CookiesMiddleware': 700,
    'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
    # 'manolo_scraper.middlewares.CustomRetryMiddleware': 910,
    # 'scrapy_splash.SplashCookiesMiddleware': 723,
    # 'scrapy_splash.SplashMiddleware': 725,
    # 'manolo_scraper.middlewares.ProxyMiddleware': 750,
    # 'scrapy.downloadermiddlewares.retry.RetryMiddleware': None,
}

LOG_LEVEL = 'DEBUG'
LOG_ENABLED = True

ITEM_PIPELINES = {
    'manolo_scraper.pipelines.DuplicatesPipeline': 300,
    'manolo_scraper.pipelines.CleanItemPipeline': 400,
}

DUPEFILTER_DEBUG = True
COOKIES_DEBUG = True
COOKIES_ENABLED = True
