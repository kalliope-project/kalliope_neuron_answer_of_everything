# -*- coding: utf-8 -*-

# Orginal source https://github.com/Areeb-M/GoogleAnswers
from scraper import scrape


class GoogleAnswer():
    def __init__(self, query):
        self.query = query

    def get_answer(self):
        result = None
        url = self.build_url(self.query)
        result = scrape(url)
        if result:
            return result
        return result


    def build_url(self, url):
        url = url.replace(' ', '+')
        url = url.replace('?', '')
        url = "http://www.google.com/search?q=" + url
        return url