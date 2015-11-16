#-------------------------------------------------------------------------------
# Created on 13.04.2015
# 
# @author: Van Der Korn
# @file: WebSitesCrawler.py
#-------------------------------------------------------------------------------
# -*- coding=utf-8 -*-
from abc import ABCMeta, abstractmethod, abstractproperty
import pycurl
import StringIO


class WebSitesCrawler:
    """
    Abstract websites crawler
    """
    __metaclass__ = ABCMeta
    
    @abstractmethod
    def Get(self, url):
        """
        Get request
        :param url: uri address
        :return:
        data
        """
        pass
    
    @abstractmethod
    def Post(self, url, postdata):
        """
        Post request
        :param url: uri address
        :param postdata: post data
        :return:
        data
        """
        pass

class WebSitesCrawlerImplement(WebSitesCrawler):
    """
    Websites crawler without proxies
    """
    def __init__(self):
        """
        Constructor
        """

    def Get(self, url):
        """
        Get request
        :param url: uri address
        :return:
        data
        """
        #initialize objects
        data = StringIO.StringIO()
        curl = pycurl.Curl()
        #set up pycurl
        curl.setopt(pycurl.FOLLOWLOCATION, 1)
        curl.setopt(pycurl.CONNECTTIMEOUT, 30)
        curl.setopt(pycurl.TIMEOUT, 320);
        curl.setopt(pycurl.USERAGENT, "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2226.0 Safari/537.36")
        curl.setopt(pycurl.URL, url)
        curl.setopt(pycurl.WRITEFUNCTION, data.write)

              
        #Try run request
        curl.perform()

        #close connection
        curl.close()
        #return the received page
        return data.getvalue()
    
    def Post(self, url, postdata):
        """
        Post request
        :param url: uri address
        :param postdata: post data
        :return:
        data
        """
        #initialize objects
        data = StringIO.StringIO()
        curl = pycurl.Curl()
        #set up pycurl
        curl.setopt(pycurl.FOLLOWLOCATION, 1)
        curl.setopt(pycurl.CONNECTTIMEOUT, 30)
        curl.setopt(pycurl.TIMEOUT, 320);
        curl.setopt(pycurl.URL, url)
        curl.setopt(pycurl.WRITEFUNCTION, data.write)
        curl.setopt(pycurl.POST, 1)
        curl.setopt(pycurl.POSTFIELDS, postdata)
              
        #Try run request
        curl.perform()

        #close connection
        curl.close()
        #return the received page
        return data.getvalue()