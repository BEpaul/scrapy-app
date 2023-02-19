BOT_NAME = 'wines'

SPIDER_MODULES = ['wines.spiders']
NEWSPIDER_MODULE = 'wines.spiders'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False


# Set settings whose default value is deprecated to a future-proof value
REQUEST_FINGERPRINTER_IMPLEMENTATION = '2.7'
TWISTED_REACTOR = 'twisted.internet.asyncioreactor.AsyncioSelectorReactor'

# 로그 파일 따로 생성
LOG_FILE = 'wines.log'

# csv utf setting
FEED_EXPORT_ENCODING = "utf-8-sig"

# connect pipeline to spider
ITEM_PIPELINES = {
  "wines.pipelines.WinesPipeline": 300,
}