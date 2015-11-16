import datetime

__author__ = 'Van'
#-------------------------------------------------------------------------------
# Created on 14.12.2011
#
# @author: Van Der Korn
# @file: googlemachine.py
#-------------------------------------------------------------------------------
# -*- coding=utf-8 -*-
from math import ceil
import hashlib
import time
import random

import inject


from  core.crawlers.WebSitesCrawler import *
from core.parsers.Parser import Parser
from core.parsers.carsalescomau import CarsalesComAuSyntaxAnalyzer

import logging


class CarsalesComAuParser(Parser):
    __metaclass__ = ABCMeta

    @abstractmethod
    def Parse(self, count):
        pass

class CarsalesComAuParserImplement(CarsalesComAuParser):
    '''
    classdocs
    '''
    @inject.params(crawler=WebSitesCrawler, synaxanalyzer=CarsalesComAuSyntaxAnalyzer)
    def __init__(self, crawler, synaxanalyzer):
        '''
        Constructor
        '''
        self.crawler = crawler
        self.synaxanalyzer = synaxanalyzer

        self.itemOnPage = 12
        self.ListItemsUrl = 'http://www.carsales.com.au/cars/results?sortby=LastUpdated&offset={offset}&q=Service%3D%5BCarsales%5D'
        self.SiteHost = 'http://www.carsales.com.au'

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

        # self.timeout_down=2500 # timeout in ms
        # self.timeout_up=3500 # timeout in ms
        #
        # self.sleep_i=10
        # self.timeout_down_interval=15000 # timeout through some requests
        # self.timeout_up_interval=30000 # timeout through some requests
        #
        # self.sleep_i_2=100
        # self.timeout_down_interval_2=90000 # timeout through some requests
        # self.timeout_up_interval_2=120000 # timeout through some requests
        #
        # self.sleep_i_3=1000
        # self.timeout_down_interval_3=150000 # timeout through some requests
        # self.timeout_up_interval_3=300000 # timeout through some requests
        #
        # self.timeout_down_error=30000 # timeout for error
        # self.timeout_up_error=45000 # timeout for error

        #self.ListItemsUrl = 'http://localhost/carsales/list4.html'
        #self.ListItemsUrl = 'http://localhost/test/test14.html'

    def Parse(self, count) :
        countPages = int(ceil(count/float(self.itemOnPage)))
        itemIndex = 0
        for i in range(834, countPages):
            try:
                logging.info(i)
                if itemIndex >= count : break
                url = self.ListItemsUrl.format(offset = i*self.itemOnPage )
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
                    detailurl = self.SiteHost + item.Url
                    itemIndex = itemIndex + 1
                    time.sleep(random.uniform(self.timeout_down, self.timeout_up)/1000) #after request it is required to wait

                    try:
                        contentDetail = self.crawler.Get(detailurl)
                        logging.info(detailurl)
                        #contentDetail = self.crawler.Get('http://localhost/carsales/detail6.html')
                        itemDetail = self.synaxanalyzer.AnalyzeItem(contentDetail)
                    except:
                        logging.exception('')
                        time.sleep(random.uniform(self.timeout_down_error, self.timeout_up_error)/1000) #after request it is required to wait
                        continue

                    m = hashlib.md5()
                    m.update(item.Url)
                    item.Id =  m.hexdigest()
                    item.Url= self.SiteHost + item.Url
                    item.OriginalUrl= itemDetail.OriginalUrl
                    item.Description= itemDetail.Description
                    item.CountryOfOrigin = itemDetail.CountryOfOrigin

                    item.ReleaseYear = itemDetail.ReleaseYear
                    item.Colour = itemDetail.Colour
                    item.FuelAverage = itemDetail.FuelAverage
                    item.KerbWeight = itemDetail.KerbWeight
                    item.FuelType = itemDetail.FuelType
                    item.Badge = itemDetail.Badge
                    item.Series = itemDetail.Series
                    item.Gears = itemDetail.Gears
                    item.Doors = itemDetail.Doors
                    item.SeatCapacity = itemDetail.SeatCapacity

                    item.AdditionalFeatures = itemDetail.AdditionalFeatures
                    item.LastModified = itemDetail.LastModified

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


            #if i > count : break
