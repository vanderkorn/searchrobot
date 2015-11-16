#-------------------------------------------------------------------------------
# Created on 14.12.2011
# 
# @author: Van Der Korn
# @file: googlemachine.py
#-------------------------------------------------------------------------------
# -*- coding=utf-8 -*-
from core.crawlers.WebSitesProxyCrawler import WebSitesProxyCrawler
from core.logger.Logger import Logger
from core.parsers.carsalescomau.CarsalesComAuSyntaxAnalyzer import *
from core.parsers.carsalescomau.CarsalesComAuParser import *

from  core.parsers.drivecomau.DriveComAuParser import *
from  core.parsers.drivecomau.DriveComAuSyntaxAnalyzer import *

from  core.crawlers.WebSitesCrawler import *
from  core.dataproviders.ElasticSearchProvider import *

from core.parsers.gumtreecomau.GumtreeComAuSyntaxAnalyzer import *
from core.parsers.gumtreecomau.GumtreeComAu import *

from core.parsers.ebaycomau.EbayComAuSyntaxAnalyzer import *
from core.parsers.ebaycomau.EbayComAu import *


class Dependencer(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
    @staticmethod
    def RegisterDependencies():
        inject.configure(Dependencer.my_config)
        return
    
    @staticmethod
    def my_config(binder):

        binder.bind_to_provider(DriveComAuParser, DriveComAuParserImplement)
        binder.bind_to_provider(DriveComAuSyntaxAnalyzer, DriveComAuSyntaxAnalyzerImplement)

        binder.bind_to_provider(CarsalesComAuParser, CarsalesComAuParserImplement)
        binder.bind_to_provider(CarsalesComAuSyntaxAnalyzer, CarsalesComAuSyntaxAnalyzerImplement)

        binder.bind_to_provider(GumtreeComAuParser, GumtreeComAuParserImplement)
        binder.bind_to_provider(GumtreeComAuSyntaxAnalyzer, GumtreeComAuSyntaxAnalyzerImplement)

        binder.bind_to_provider(EbayComAuParser, EbayComAuParserImplement)
        binder.bind_to_provider(EbayComAuSyntaxAnalyzer, EbayComAuSyntaxAnalyzerImplement)

        binder.bind(WebSitesCrawler, WebSitesProxyCrawler())
        #binder.bind(WebSitesCrawler, WebSitesCrawlerImplement())
        binder.bind(ElasticSearchProvider, ElasticSearchProviderImplement("vehicles-search.cloudapp.net", 9200, "admin", "vfhn28"))
        Logger.Initialize()
