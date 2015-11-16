#-------------------------------------------------------------------------------
# Created on 13.04.2015
#
# @author: Van Der Korn
# @file: ElasticSearchProvider.py
#-------------------------------------------------------------------------------
# -*- coding=utf-8 -*-

from abc import ABCMeta, abstractmethod
import inspect
import socket

from elasticsearch import Elasticsearch, Urllib3HttpConnection
import urllib3


class ElasticSearchProvider:
    """
    Abstract class ElasticSearch service
    """
    __metaclass__ = ABCMeta
     
    @abstractmethod
    def Index(self, vehicle):
        """
        Index vehicle
        :param vehicle:
        :return:
        """
        pass


class ElasticSearchProviderImplement(ElasticSearchProvider):
    """
    ElasticSearch service
    """

    def __init__(self, host = "localhost", port = 9200, user = None, password = None):
        """
        Constructor
        """
        self.host = host
        self.port = port
        self.user = user
        self.password = password

        # set tcp settings
        DEFAULT_SOCKET_OPTION = urllib3.connection.HTTPConnection.default_socket_options

        if hasattr(socket, "SO_KEEPALIVE"):
            DEFAULT_SOCKET_OPTION.append((socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1))
        if hasattr(socket, "TCP_KEEPIDLE"):
            DEFAULT_SOCKET_OPTION.append((socket.IPPROTO_TCP, socket.TCP_KEEPIDLE, 30))
        if hasattr(socket, "TCP_KEEPINTVL"):
            DEFAULT_SOCKET_OPTION.append((socket.IPPROTO_TCP, socket.TCP_KEEPINTVL, 30))

        urllib3.connection.HTTPConnection.default_socket_options = DEFAULT_SOCKET_OPTION

        print urllib3.connection.HTTPConnection.default_socket_options

        # initialize ElasticSearch instance
        self.es = Elasticsearch(["{0}:{1} ".format(self.host, self.port)], connection_class=Urllib3HttpConnection, http_auth=(self.user, self.password), timeout=60)

    def Index(self, vehicle):
        """
        Index vehicle
        :param vehicle:
        :return:
        """
        dict = self.props(vehicle)
        res = self.es.index(index="vehicles", doc_type='vehicles', id=vehicle.Id, body=dict)
        # print(res['created'])
        
    def props(self, obj):
        """
        Convert object to dictionary
        :param obj: vehicle
        :return:
        """
        pr = {}
        for name in dir(obj):
            value = getattr(obj, name)
            if not name.startswith('__') and not inspect.ismethod(value):
                pr[name] = value
        return pr
    
    def SetNullImages(self):
        """
        Helper method for set up null images
        :return:
        """
        res = self.es.search(index="vehicles", doc_type='vehicles', body={"from": 0, "size": 1500, "query": {"query_string": {"query": "*no-image-available*","fields": ["ThumbnailUrl"]}}})
        print("Got %d Hits:" % res['hits']['total'])
        for hit in res['hits']['hits']:
            id = hit["_id"]
            res = self.es.update(index="vehicles", doc_type='vehicles', id = id, body={"doc" : { "ThumbnailUrl" :""}})