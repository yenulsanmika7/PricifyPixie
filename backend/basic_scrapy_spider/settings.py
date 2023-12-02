BOT_NAME = 'basic_scrapy_spider'

SPIDER_MODULES = ['basic_scrapy_spider.spiders']
NEWSPIDER_MODULE = 'basic_scrapy_spider.spiders'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

SCRAPEOPS_API_KEY = 'b6de998c-1b9a-44a0-8aa9-e254a05ba257'
SCRAPEOPS_PROXY_ENABLED = True

DOWNLOADER_MIDDLEWARES = {
    ## ScrapeOps Monitor
    'scrapeops_scrapy.middleware.retry.RetryMiddleware': 550,
    'scrapy.downloadermiddlewares.retry.RetryMiddleware': None,
    
    ## Proxy Middleware
    'scrapeops_scrapy_proxy_sdk.scrapeops_scrapy_proxy_sdk.ScrapeOpsScrapyProxySdk': 725,
}

# Max Concurrency On ScrapeOps Proxy Free Plan is 1 thread
CONCURRENT_REQUESTS = 1
DOWNLOAD_DELAY = 0.5
HTTPCACHE_ENABLED = True


LOG_LEVEL = 'INFO'