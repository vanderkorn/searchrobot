#-------------------------------------------------------------------------------
# Created on 13.04.2015
#
# @author: Van Der Korn
# @file: WebSitesProxyCrawler.py
#-------------------------------------------------------------------------------
# -*- coding=utf-8 -*-
from Queue import Queue
import logging
import pycurl
import StringIO
import csv
import random

from core.crawlers.WebSitesCrawler import WebSitesCrawler
from core.extensions.StringExtensions import StringExtensions
from core.models.Proxy import Proxy

class WebSitesProxyCrawler(WebSitesCrawler):
    """
    Websites crawler with proxies
    """

    def __init__(self, proxyFile = 'proxies.csv', userAgentFile = 'user_agents.txt'):
        """
        Constructor of web proxy crawler
        :return:
        """

        #load proxies
        self.__proxies = self.__load_proxies(proxyFile)
        # load the user agents, in random order
        self.__user_agents = self.__load_user_agents(uafile=userAgentFile)

    def Get(self, url):
        """
        Get request
        :param url: uri address
        :return:
        data
        """

        def get_function(curl):
                curl.setopt(pycurl.URL, url)
        return self.__do_request(get_function)

    def Post(self, url, postdata):
        """
        Post request
        :param url: uri address
        :param postdata: post data
        :return:
        data
        """

        def post_function(curl):
            curl.setopt(pycurl.URL, url)
            curl.setopt(pycurl.POST, 1)
            curl.setopt(pycurl.POSTFIELDS, postdata)
        return self.__do_request(post_function)

    def __do_request(self, request_function):
        """
            Execute request
        :param request_function:
            Helpers function for add some data in curl object
        :return:
            data
        """

        try:

            #initialize objects
            data = StringIO.StringIO()
            curl = pycurl.Curl()

            #Set up parameters
            curl.setopt(pycurl.FOLLOWLOCATION, 1)
            curl.setopt(pycurl.CONNECTTIMEOUT, 30)
            curl.setopt(pycurl.TIMEOUT, 320)
            curl.setopt(pycurl.WRITEFUNCTION, data.write)

            ua = random.choice(self.__user_agents)  # select a random user agent
            logging.info("Select User Agent: %s", ua)
            curl.setopt(pycurl.USERAGENT, ua)

            # curl.setopt(pycurl.HTTPHEADER, ['Accept: text/html', 'Accept-Language: ru-RU,ru;q=0.8,en-US;q=0.6,en;q=0.4'])

            #Set up additional parameters
            request_function(curl)

            #Set up proxy
            proxy = self.__set_proxy(curl)

            if proxy != None:
                logging.info("Select Proxy: %s", proxy)
            else:
                logging.info("Proxy not selected!")

            #Try run request
            curl.perform()

            httpCode = curl.getinfo(pycurl.HTTP_CODE)
            result_str = data.getvalue()
            if httpCode != 200:
                effective_url = curl.getinfo(pycurl.EFFECTIVE_URL)
                logging.error("Error status code: %s; Effective url: %s", httpCode, effective_url)
                logging.error("Error content message: %s", result_str)

            #return the received page
            return result_str
        finally:
            if curl != None:
                #close connection
                curl.close()
            if proxy != None:
                # release proxy
                self.__proxies.put(proxy)

    def __set_proxy(self, curl):
        """
        Add proxy in curl object if need
        :param curl: object
            curl
        :return:
            selected proxy
        """

        if self.__proxies.empty() == False:
            proxy = self.__proxies.get()
            self.__proxies.task_done()
            self.__proxies.put(proxy)
            curl.setopt(pycurl.PROXY, proxy.Host)
            curl.setopt(pycurl.PROXYPORT, proxy.Port)
            curl.setopt(pycurl.PROXYTYPE, proxy.Type)
            curl.setopt(pycurl.PROXYAUTH, proxy.Auth)
            if proxy.User and proxy.Password:
                curl.setopt(pycurl.PROXYUSERPWD, '%s:%s' % (proxy.User, proxy.Password))
            return proxy
        return None

    def __load_proxies(self, fileProxy):
        """
        Read proxies from CSV-file
        :param fileProxy: string
            path to csv file
        :return:
            array of proxies
        """

        proxyList = Queue()
        input_file = csv.DictReader(open(fileProxy), delimiter=';')
        for row in input_file:
            proxy = Proxy()
            proxy.Host = row["PROXY_HOST"].strip()
            port = StringExtensions.mk_int(row["PROXY_PORT"])
            if port > 0:
                proxy.Port = port
            proxy.Type = StringExtensions.ToProxyType(row["PROXY_TYPE"])
            proxy.User = row["PROXY_USER"].strip()
            proxy.Password = row["PROXY_PASSOWRD"].strip()
            proxy.Auth = StringExtensions.ToProxyAuth(row["PROXY_AUTH"])
            proxyList.put(proxy)
        return proxyList

    def __load_user_agents(self, uafile):
        """
        Read user agents from file
        :rtype : array
        :param uafile: string
            path to text file of user agents, one per line
        :return: array
            array of user agents
        """

        uas = []
        with open(uafile, 'rb') as uaf:
            for ua in uaf.readlines():
                if ua:
                    uas.append(ua.strip()[1:-1-1])
        random.shuffle(uas)
        return uas