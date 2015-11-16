#-------------------------------------------------------------------------------
# Created on 14.12.2011
# 
# @author: Van Der Korn
# @file: dataprovider.py
#-------------------------------------------------------------------------------
# -*- coding=utf-8 -*-

import inject
from math import ceil
from  core.dataproviders.ElasticSearchProvider import *
from  core.parsers.ParsersFactory import *
import logging
import sys,traceback
from multiprocessing.dummy import Pool as ThreadPool
from functools import partial
class SearchRobot(object):
    '''
    classdocs
    '''
    @inject.params(elasticservice=ElasticSearchProvider)
    def __init__(self, elasticservice):
        '''
        Constructor
        '''
        self.elasticservice = elasticservice
        return


    def Index(self, hosts, count = 10000):
        '''Get name site'''
        hostsCount = len(hosts)
        logging.info('Search Robot started for count of hosts = %s; count of ads = %s!' % (hostsCount, count))
        count = (int) (ceil(float(count) / hostsCount))

        for host in hosts:
            self.IndexSite((count, host))
            

        logging.info('Search Robot completed!')
        return

    def IndexParallel(self, hosts, count = 10000):
        '''Get name site'''
        hostsCount = len(hosts)
        logging.info('Search Robot started for count of hosts = %s; count of ads = %s!' % (hostsCount, count))
        count = (int) (ceil(float(count) / hostsCount))
        pool = ThreadPool(hostsCount)

        pool.map(self.IndexSite, zip([count]*hostsCount,hosts))

        logging.info('Search Robot completed!')
        return

    def IndexSite(self, (count, host)):
        logging.info('Search Robot started for site = %s; count = %d' % (host, count))
        try:
            parser = ParsersFactory.factory(host)
            for vehicle in parser.Parse(count):
                self.elasticservice.Index(vehicle)
                logging.info('Idexed vehicle from url = %s' % (vehicle.Url))
        except:
            logging.exception('')
        logging.info('Search Robot finished for site = %s; count = %d' % (host, count))