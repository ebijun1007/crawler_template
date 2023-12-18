import sys

from scrapy.cmdline import execute
from scrapy.utils.project import get_project_settings

settings = get_project_settings()
settings.set('DOWNLOADER_MIDDLEWARES', {'crawler.middlewares.MyCustomDownloaderMiddleware': 900})

if __name__ == '__main__':
    # get args from command line
    url = sys.argv[1]
    execute(['scrapy', 'shell', f"{url}"], settings=settings)
