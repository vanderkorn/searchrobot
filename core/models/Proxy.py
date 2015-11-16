import pycurl

__author__ = 'Van'
class Proxy(object):
    '''
    Proxy
    '''

    def __init__(self, host = "", port = 80, type = pycurl.PROXYTYPE_HTTP, user = "", password = "", auth = pycurl.HTTPAUTH_NONE):
        '''
        Constructor
        '''
        self.Host = host
        self.Port = port
        self.Type = type
        self.User = user
        self.Password = password
        self.Auth = auth

    def __str__(self):
        return "%s:%s Type: %s User:%s Password:%s Auth:%s" % (self.Host, self.Port, self.Type, self.User, self.Password, self.Auth)

    def __unicode__(self):
        return unicode(str(self))