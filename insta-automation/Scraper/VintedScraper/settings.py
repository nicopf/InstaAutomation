# -*- coding: utf-8 -*-

# Scrapy settings for PyntedScrapers project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

FEED_URI = "feed.json"

IMAGES_STORE = './images'

FEED_FORMAT = 'jsonlines'


BOT_NAME = 'VintedScraper'

FEED_EXPORT_ENCODING = 'utf-8'

LOG_LEVEL = 'INFO'

NEWSPIDER_MODULE = 'VintedScraper.spiders'

ITEM_PIPELINES = {'scrapy.pipelines.images.ImagesPipeline': 1}

IMAGES_URLS_FIELD = 'image_urls'

ROBOTSTXT_OBEY = True

SPIDER_MODULES = ['VintedScraper.spiders']