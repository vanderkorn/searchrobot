#-------------------------------------------------------------------------------
# Created on 14.12.2011
# 
# @author: Van Der Korn
# @file: logger.py
#-------------------------------------------------------------------------------
# -*- coding=utf-8 -*-

import logging
import logging.handlers
import logging.config
import sys
class Logger(object):
    '''
    Class Logger
    '''
    
    def __init__(self):
        '''
        Constructor
        '''

    @staticmethod
    def Initialize(configFile = 'logging.config'):
        logging.config.fileConfig(configFile, disable_existing_loggers=False)
        # log = logging.getLogger('')
        # format = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        #
        # ch = logging.StreamHandler(sys.stdout)
        # ch.setFormatter(format)
        # ch.setLevel(logging.DEBUG)
        # log.addHandler(ch)
        #
        # fh = logging.handlers.RotatingFileHandler(filename='logs/log.log', maxBytes=(1048576*5), backupCount=7)
        # fh.setLevel(logging.INFO)
        # fh.setFormatter(format)
        # log.addHandler(fh)
