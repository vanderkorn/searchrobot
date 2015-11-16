#-------------------------------------------------------------------------------
# Created on 14.12.2011
# 
# @author: Van Der Korn
# @file: googlemachine.py
#-------------------------------------------------------------------------------
# -*- coding=utf-8 -*-
import inject
from core.parsers.carsalescomau.CarsalesComAuParser import CarsalesComAuParser

from core.parsers.drivecomau.DriveComAuParser import DriveComAuParser
from core.parsers.ebaycomau.EbayComAu import EbayComAuParser
from core.parsers.gumtreecomau.GumtreeComAu import GumtreeComAuParser


class ParsersFactory(object):
    '''
    classdocs
    '''
    @staticmethod
    def factory(host):
        host = host.lower()
        if host == "www.drive.com.au": return inject.instance(DriveComAuParser)
        elif host == "www.carsales.com.au": return inject.instance(CarsalesComAuParser)
        elif host == "www.gumtree.com.au": return inject.instance(GumtreeComAuParser)
        elif host == "www.ebay.com.au": return inject.instance(EbayComAuParser)
        assert 0, "Bad shape creation: " + type
