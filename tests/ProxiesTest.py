from core.crawlers.WebSitesProxyCrawler import WebSitesProxyCrawler
from core.logger.Logger import Logger

__author__ = 'Van'

import unittest


class WebSitesProxyCrawlerTest(unittest.TestCase):
    def setUp(self):
        Logger.Initialize('../logging.config')

    def test_Get_6min(self):
        crawler = WebSitesProxyCrawler('../proxies.csv', '../user_agents.txt')
        url = '6min.ru'
        for i in range(0, 10):
            content = crawler.Get(url)
            result = 'class="componentheading"' in content
            self.assertEqual(True, result)

    # def test_Get_carsales(self):
    #     crawler = WebSitesProxyCrawler('../proxies.csv', '../user_agents.txt')
    #     url = 'carsales.com.au'
    #     for i in range(0, 10):
    #         content = crawler.Get(url)
    #         result = 'class="r-module"' in content
    #         self.assertEqual(True, result)

    # def test_Get_drive(self):
    #     crawler = WebSitesProxyCrawler('../proxies.csv', '../user_agents.txt')
    #     url = 'drive.com.au'
    #     for i in range(0, 10):
    #         content = crawler.Get(url)
    #         result = 'id="main"' in content
    #         self.assertEqual(True, result)

    # def test_Get_gumtree(self):
    #     crawler = WebSitesProxyCrawler('../proxies.csv', '../user_agents.txt')
    #     url = 'gumtree.com.au'
    #     for i in range(0, 10):
    #         content = crawler.Get(url)
    #         result = 'class="module-heading"' in content
    #         self.assertEqual(True, result)

    # def test_Get_ebay(self):
    #     crawler = WebSitesProxyCrawler('../proxies.csv', '../user_agents.txt')
    #     url = 'www.ebay.com.au'
    #     for i in range(0, 10):
    #         content = crawler.Get(url)
    #         result = 'class="gf-li"' in content
    #         self.assertEqual(True, result)

if __name__ == '__main__':
    unittest.main()
