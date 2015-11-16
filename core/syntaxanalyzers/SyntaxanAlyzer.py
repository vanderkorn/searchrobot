__author__ = 'Van'

from abc import ABCMeta, abstractmethod

class SyntaxAnalyzer:
    __metaclass__ = ABCMeta
    @abstractmethod
    def AnalyzeList(self, htmlstring):
        pass

    @abstractmethod
    def AnalyzeItem(self, htmlstring):
        pass
