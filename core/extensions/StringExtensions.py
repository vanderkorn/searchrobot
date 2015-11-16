__author__ = 'Van'
import pycurl
class StringExtensions(object):
    """
    Class Logger
    """

    def __init__(self):
        '''
        Constructor
        '''

    @staticmethod
    def mk_int(s):
        s = s.strip()
        return int(s) if s else 0

    @staticmethod
    def ToProxyType(s):
        s = s.strip().upper()
        if s == 'SOCKS5':
            return pycurl.PROXYTYPE_SOCKS5
        elif s == 'SOCKS4':
            return pycurl.PROXYTYPE_SOCKS4
        else:
            return pycurl.PROXYTYPE_HTTP

    @staticmethod
    def ToProxyAuth(s):
        s = s.strip().upper()
        if s == 'BASIC':
            return pycurl.HTTPAUTH_BASIC
        elif s == 'NTLM':
            return pycurl.HTTPAUTH_NTLM
        elif s == 'GSSNEGOTIATE':
            return pycurl.HTTPAUTH_GSSNEGOTIATE
        else:
            return pycurl.HTTPAUTH_NONE