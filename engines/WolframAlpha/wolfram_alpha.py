# -*- coding: iso-8859-1 -*-
import requests
import re


class WolframAlpha():
    def __init__(self, query, key, unit):
        self.SR_ROOT = 'https://api.wolframalpha.com/v2/spoken'
        self.SA_ROOT = 'http://api.wolframalpha.com/v2/result'
        self.query = query
        self.key = key
        self.unit = unit

    def spoken_answer(self):

        r = requests.get(self.SR_ROOT,params= {'appid': self.key,
                                               'i': self.query,
                                               'units': self.unit})
        if r.ok:
            return self.format_result(r.text)
        else:
            return None

                        
    def short_answer(self):
        r = requests.get(self.SA_ROOT,params= {'appid': self.key,
                                               'i': self.query,
                                               'units': self.unit})
        if r.ok:
            return self.format_result(r.text)
        else:
            return None

    def format_result(self, result):
        result = re.sub(r'\([^)]*\)', '', result)

        if result.endswith('definitions') or result.endswith('definition'):
            sentences = result.split('.')
            result = '.'.join(sentences[:-1])
        
        return result
