__author__ = 'Van'
from abc import abstractmethod, ABCMeta
class Parser:
    __metaclass__ = ABCMeta

    @abstractmethod
    def Parse(self, count):
        pass
