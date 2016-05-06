import logging
import socket
import urllib2
from cStringIO import StringIO
from PIL import Image as PIL_Image
import os


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
        self.icon_url_fingerprint_map = {}
        for url in icon_url_set:
            try:
                request = self._build_request(url)
                response = self._scrape(request)
                self._parser(response, url)
            except Exception, e:
                print 'Unknown exception for url %s: exception: %s' % (url, e.message)
                self.icon_url_fingerprint_map[url] = None

        print "Scraped total count: %s. succeed:%s, failed:%s" % (
            self.scrape_total_count, self.scrape_succeed_count, self.scrape_total_count - self.scrape_succeed_count)
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

        retry_times = 2
        while retry_times >= 0:
            try:
                response = urllib2.urlopen(request, timeout=90)
                # print 'Succeed to scrape url %s' % request.get_full_url()
                self.scrape_succeed_count += 1
                return response
            except urllib2.HTTPError, e:
                if e.code in [404, ]:
                    print ('404 to scrape url %s, no need to retry' % request.get_full_url())
                print ('Failed to scrape url %s, there are %s times to retry' %
                       (request.get_full_url(), retry_times))
            except socket.timeout:
                print ('Time out to scrape url %s, there are %s times to retry' %
                       (request.get_full_url(), retry_times))
            except IOError:
                print ('Image for url %s is broken, there are %s times to retry' %
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
            print ex.message, ", parser, url : ", url


if __name__ == '__main__':
    icon_spider = UrlLibIconSpider()
    icons_url_set = {'http://a4.mzstatic.com/us/r1000/025/Purple/84/23/98/mzl.bnbszqhh.75x75-65.jpg',
                     'http://a1.mzstatic.com/us/r30/Purple/v4/95/94/2b/95942bce-8ab7-552a-5c77-f9ae3f5554ce/icon_75.png'}
    print 1
    url_image_dict = icon_spider.scrape(icons_url_set)
    print url_image_dict
    image_objs = url_image_dict.values()
    print image_objs
    if all(image_objs):
        dir_path = "icons\{id}"
        img_path = "icons\{id}\{lr}.png"
        os.mkdir(dir_path.format(id=9999))
        image_objs[0].save(img_path.format(id=9999, lr='left'))
        image_objs[1].save(img_path.format(id=9999, lr='ight'))

    print url_image_dict
