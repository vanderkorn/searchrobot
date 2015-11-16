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
import datetime

import inject
from core.parsers.Parser import Parser

from  core.parsers.drivecomau.DriveComAuSyntaxAnalyzer import *
from  core.crawlers.WebSitesCrawler import *
import logging


class DriveComAuParser(Parser):
    __metaclass__ = ABCMeta
     
    @abstractmethod
    def Parse(self, count):
        pass

class DriveComAuParserImplement(DriveComAuParser):
    '''
    classdocs
    '''
    @inject.params(crawler=WebSitesCrawler, synaxanalyzer=DriveComAuSyntaxAnalyzer)
    def __init__(self, crawler, synaxanalyzer):
        '''
        Constructor
        '''
        self.crawler = crawler
        self.synaxanalyzer = synaxanalyzer

        self.itemOnPage = 10
        self.ListItemsUrl = 'http://www.drive.com.au/search/buy-used-cars/?nc=1&uc=1&ia=0&from=0&pg={pageNumber}&sf=dateupdateddesc'
        self.SiteHost = 'http://www.drive.com.au'

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
        
        #self.ListItemsUrl = 'http://localhost/test/test3.html'
        #self.ListItemsUrl = 'http://localhost/test/test14.html'
           
    def Parse(self, count) :
        countPages = int(ceil(count/float(self.itemOnPage)))
        itemIndex = 0
        for i in range(0, countPages):
            try:
                logging.info(i)
                if itemIndex >= count : break
                url = self.ListItemsUrl.format(pageNumber = (i+1) )
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
                        #contentDetail = self.crawler.Get('http://localhost/test/detail12.html')
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
                    item.Vin = itemDetail.Vin
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
                    item.TotalDealerPrice = itemDetail.TotalDealerPrice
                    item.AdditionalFeatures = itemDetail.AdditionalFeatures

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
