# -*- coding: utf-8 -*-
import ddg3



class DuckDuckGo():
    def __init__(self, query):
        self.query = query


    def get_answer(self):
        r = ddg3.query(self.query)
        if (r.answer is not None and "HASH" not in r.answer.text and r.answer.text):
            return r.answer.text
    
        elif len(r.abstract.text) > 0:
            return r.abstract.text.split('. ')[0] + "."

        elif len(r.related) > 0 and len(r.related[0].text) > 0:
            return r.related[0].text

        else:
            return None

