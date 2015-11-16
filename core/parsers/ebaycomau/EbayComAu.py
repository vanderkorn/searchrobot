import datetime

__author__ = 'Van'
from math import ceil
import hashlib
import time
import random

import inject


from  core.crawlers.WebSitesCrawler import *
from core.parsers.Parser import Parser
from core.parsers.ebaycomau import EbayComAuSyntaxAnalyzer

import logging


class EbayComAuParser(Parser):
    __metaclass__ = ABCMeta

    @abstractmethod
    def Parse(self, count):
        pass

class EbayComAuParserImplement(EbayComAuParser):
    '''
    classdocs
    '''
    @inject.params(crawler=WebSitesCrawler, synaxanalyzer=EbayComAuSyntaxAnalyzer)
    def __init__(self, crawler, synaxanalyzer):
        '''
        Constructor
        '''
        self.crawler = crawler
        self.synaxanalyzer = synaxanalyzer

        self.itemOnPage = 200
        self.ListItemsUrl = 'http://www.ebay.com.au/sch/Cars-/29690/i.html?_sop=10&_ipg=200&_pgn={pageNumber}&rt=nc&LH_PrefLoc=1'
        self.SiteHost = 'http://www.ebay.com.au'

        # self.timeout_down=5 # timeout in ms
        # self.timeout_up=50 # timeout in ms
        #
        # self.sleep_i=10
        # self.timeout_down_interval=15 # timeout through some requests
        # self.timeout_up_interval=30 # timeout through some requests
        #
        # self.sleep_i_2=100
        # self.timeout_down_interval_2=90 # timeout through some requests
        # self.timeout_up_interval_2=120 # timeout through some requests
        #
        # self.sleep_i_3=1000
        # self.timeout_down_interval_3=15 # timeout through some requests
        # self.timeout_up_interval_3=30 # timeout through some requests
        #
        # self.timeout_down_error=30 # timeout for error
        # self.timeout_up_error=45 # timeout for error

        self.timeout_down=250 # timeout in ms
        self.timeout_up=350 # timeout in ms

        self.sleep_i=10
        self.timeout_down_interval=500 # timeout through some requests
        self.timeout_up_interval=1500 # timeout through some requests

        self.sleep_i_2=100
        self.timeout_down_interval_2=4500 # timeout through some requests
        self.timeout_up_interval_2=6000 # timeout through some requests

        self.sleep_i_3=1000
        self.timeout_down_interval_3=7500 # timeout through some requests
        self.timeout_up_interval_3=15000 # timeout through some requests

        self.timeout_down_error=1500 # timeout for error
        self.timeout_up_error=3000 # timeout for error

        #self.ListItemsUrl = 'http://localhost/ebay/list5.html'
        #self.ListItemsUrl = 'http://localhost/test/test14.html'

    def Parse(self, count) :
        countPages = int(ceil(count/float(self.itemOnPage)))
        itemIndex = 0
        for i in range(0, countPages):
            try:
                logging.info(i)
                if itemIndex >= count : break
                url = self.ListItemsUrl.format(pageNumber = i)
                logging.info(url)
                time.sleep(random.uniform(self.timeout_down, self.timeout_up)/1000) #after request it is required to wait
                try:
                    content = self.crawler.Get(url)
                    listItems = self.synaxanalyzer.AnalyzeList(content)
                except:
                    logging.exception('')
                    time.sleep(random.uniform(self.timeout_down_error, self.timeout_up_error)/1000) #after request it is required to wait
                    continue
                for item in listItems :
                    if itemIndex >= count : break
                    detailurl = item.Url
                    itemIndex = itemIndex + 1
                    time.sleep(random.uniform(self.timeout_down, self.timeout_up)/1000) #after request it is required to wait

                    try:
                        contentDetail = self.crawler.Get(detailurl)
                        logging.info(detailurl)
                        #contentDetail = self.crawler.Get('http://localhost/ebay/detail6.html')
                        itemDetail = self.synaxanalyzer.AnalyzeItem(contentDetail)
                    except:
                        logging.exception('')
                        time.sleep(random.uniform(self.timeout_down_error, self.timeout_up_error)/1000) #after request it is required to wait
                        continue

                    m = hashlib.md5()
                    m.update(item.Url)
                    item.Id =  m.hexdigest()
                    item.Url= item.Url
                    item.OriginalUrl= itemDetail.OriginalUrl

                    item.ReleaseYear = itemDetail.ReleaseYear
                    item.Colour = itemDetail.Colour
                    item.Vin = itemDetail.Vin
                    item.Doors = itemDetail.Doors
                    item.AdditionalFeatures = itemDetail.AdditionalFeatures
                    item.Make = itemDetail.Make
                    item.Model = itemDetail.Model
                    item.BodyType = itemDetail.BodyType
                    item.Transmission = itemDetail.Transmission
                    item.Engine = itemDetail.Engine
                    item.Odometer = itemDetail.Odometer
                    item.IsPrivateSeller = itemDetail.IsPrivateSeller
                    item.IsNew = itemDetail.IsNew

                    if None == item.LastModified:
                        item.LastModified = datetime.date.fromordinal(datetime.date.today().toordinal() - i)

                    yield item
            finally:
                if (i%self.sleep_i==0):
                    time.sleep(random.uniform(self.timeout_down_interval,self.timeout_up_interval)/1000)#after request it is required to wait
                if (i%self.sleep_i_2==0):
                    time.sleep(random.uniform(self.timeout_down_interval_2,self.timeout_up_interval_2)/1000)#after request it is required to wait
                if (i%self.sleep_i_3==0):
                    time.sleep(random.uniform(self.timeout_down_interval_3,self.timeout_up_interval_3)/1000)#after request it is required to wait