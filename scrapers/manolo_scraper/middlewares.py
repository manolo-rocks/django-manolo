from time import sleep

from scrapy.downloadermiddlewares.retry import RetryMiddleware

from scrapers.manolo_scraper import settings


class ProxyMiddleware(object):
    def process_request(self, request, spider):
        try:
            proxy = settings.HTTP_PROXY
            request.meta['proxy'] = proxy
        except Exception as error:
            print(error)


class CustomRetryMiddleware(RetryMiddleware):
    def process_exception(self, request, exception, spider):
        if (
            isinstance(exception, self.EXCEPTIONS_TO_RETRY)
            and not request.meta.get('dont_retry', False)
        ):
            retry = request.meta.get('retry')
            sleeping = 5 * retry * retry
            print(f'sleeping {sleeping}, {retry}, {exception}, {self.max_retry_times}')
            request.meta['retry'] = retry + 1
            sleep(sleeping)
            return self._retry(request, exception, spider)
