# -*- coding: utf-8 -*-
import requests
import bs4

HEADER_PAYLOAD = {  # Enables requests.get() to See the Same Web Page a Browser Does.
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'
}

TARGET_LIST = [
    ['span', 'tsp-di tsp-dt tsp-cp'],
    ['span', 'ayqGOc kno-fb-ctx KBXm4e'],
    ['span', 'ILfuVd'],
    ['div', 'MUxGbd t51gnb lyLwlc lEBKkf'],
    ['div', 'Z0LcW XcVN5d'],
    ['div', 'rysD0c'],
    ]
    
class GoogleAnswer():
    def __init__(self, query):
        self.query = query

    def get_answer(self):
        soup = self.get_soup()
        
        answers = soup.find_all("div", {"class": "BNeawe iBp4i AP7Wnd"})
        answer_list = list()

        for answer in answers:
            if answer.text:
                answer_list.append(answer.text)
                return answer_list
        
        soup = self.get_soup(use_header=True)
        
        for target in TARGET_LIST:
            answers = soup.find_all(target[0], {"class": target[1]})
            for answer in answers:
                for single_answer in answer:
                    if single_answer:
                        try:
                            answer_list.append(single_answer.text.strip())
                        except AttributeError:
                            answer_list.append(single_answer.strip())

                        if len(answer_list) == 2:
                            break
                if answer_list:
                    return answer_list

        return answer_list

    def get_soup(self, use_header=False):
        url = f'https://www.google.com/search?q={self.query}&ie=utf-8&oe=utf-8'
        if use_header:
            response = requests.get(url, headers=HEADER_PAYLOAD)
        else:
            response = requests.get(url)
        return bs4.BeautifulSoup(response.text, 'lxml')

