import logging
import socket
import urllib2
from cStringIO import StringIO
from PIL import Image as PIL_Image

logger = logging.getLogger(__name__)


class IconSpider(object):
    """
    This spider is to scrape icon image, and generate fingerprint for image.
    """

    def scrape(self, icon_event_url_set):
        """
        Fingerprint all url and return it.
        :param icon_event_url_set: icon event url set. sample: set(['url_1', 'url_2'])
        :return: icon_url_fingerprint map, sample {'url_1': 'fingerprint_1', 'url_2': 'fingerprint_2'}
        """
        raise NotImplementedError()


class UrlLibIconSpider(IconSpider):
    def __init__(self):
        self.icon_url_fingerprint_map = {}
        self.scrape_total_count = 0
        self.scrape_succeed_count = 0

    def scrape(self, icon_url_set):
        for url in icon_url_set:
            try:
                request = self._build_request(url)
                response = self._scrape(request)
                self._parser(response, url)
            except Exception, e:
                logger.warn('Unknown exception for url %s: exception: %s' % (url, e.message))
                self.icon_url_fingerprint_map[url] = None

        logger.info("Scraped total count: %s. succeed:%s, failed:%s" %
                    (self.scrape_total_count, self.scrape_succeed_count,
                     self.scrape_total_count - self.scrape_succeed_count))
        return self.icon_url_fingerprint_map

    @staticmethod
    def _build_request(url):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_4) '
                          'AppleWebKit/536.30.1 (KHTML, like Gecko) '
                          'Version/6.0.5 Safari/536.30.1',
        }
        return urllib2.Request(url, headers=headers)

    def _scrape(self, request):
        if not request:
            return None

        retry_times = 3
        while retry_times >= 0:
            try:
                response = urllib2.urlopen(request, timeout=30)
                logger.info('Succeed to scrape url %s' % request.get_full_url())
                self.scrape_succeed_count += 1
                return response
            except urllib2.HTTPError, e:
                if e.code in [404, ]:
                    logger.warn('404 to scrape url %s, no need to retry' % request.get_full_url())
                logger.warn('Failed to scrape url %s, there are %s times to retry' %
                            (request.get_full_url(), retry_times))
            except socket.timeout:
                logger.warn('Time out to scrape url %s, there are %s times to retry' %
                            (request.get_full_url(), retry_times))
            except IOError:
                logger.warn('Image for url %s is broken, there are %s times to retry' %
                            (request.get_full_url(), retry_times))
            finally:
                retry_times -= 1
                self.scrape_total_count += 1
        return None

    def _parser(self, response, url):
        if not response:
            self.icon_url_fingerprint_map[url] = None
            return
        try:
            image = response.read()
            image_obj = PIL_Image.open(StringIO(image))
            self.icon_url_fingerprint_map[url] = image_obj
        except Exception as ex:
            logger.warn(ex.message + ", url : " + url)

if __name__ == '__main__':
    icon_spider = UrlLibIconSpider()
    icons_url_set = {'http://ecx.images-amazon.com/images/I/71TL7Zpu59L._h1_.png',
                     'http://ecx.images-amazon.com/images/I/7144vK7OFzL._h1_.png'}
    url_image_dict = icon_spider.scrape(icons_url_set)
    print url_image_dict
