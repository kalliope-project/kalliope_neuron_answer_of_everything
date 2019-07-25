import requests
from html.parser import HTMLParser


class Target:
    def __init__(self, elements):
        self.elements = elements

    def check_path(self, path):
        length = len(self.elements)
        for i in range(length):
            index = -length + i
            if path[index][0] == self.elements[index][0] and (path[index][1] == self.elements[index][1] or self.elements[index][1] == ''):
                continue
            else:
                return False
        return True


class Parser(HTMLParser):
    def __init__(self, target):
        HTMLParser.__init__(self)
        self.target = target
        self.target_depth = 0
        self.path = []
        self.occurrences = []

    def handle_starttag(self, tag, attributes):
        attr_string = ""
        for attribute in attributes:
            attr_string += attribute[0] + '="' + attribute[1] + '" '
        attr_string = attr_string[:-1]

        self.path.append([tag, attr_string])
        if self.target_depth > 0 or self.target.check_path(self.path):
            if self.target_depth == 0:
                self.occurrences.append('')
            self.target_depth += 1

    def handle_endtag(self, tag):
        self.path.pop()
        if self.target_depth > 0:
            self.target_depth -= 1

    def handle_data(self, data):
        if self.target_depth > 0:
            self.occurrences[-1] += data

    def feed(self, data):
        HTMLParser.feed(self, data)
        return self.occurrences


def scrape(url):
    global HEADER_PAYLOAD, TARGET_LIST
    data = requests.get(url, headers=HEADER_PAYLOAD).text
    try:
        start_js = data.index('/g-section-with-header')
    except ValueError:
        start_js = None
    data = data[0:start_js]
    results = []

    for target in TARGET_LIST:
        results += Parser(target).feed(data)

    return results

TARGET_LIST = [
    Target([['div', 'class="Z0LcW"']]),  # Enables Featured Snippet Scraping
    Target([['span', 'class="_Tgc"']]),  # Enables Featured Snippet Description Scraping
    Target([['span', 'class="cwcot gsrt" id="cwos"']]),  # Enables Calculator Answer Scraping
    Target([['div', 'class="vk_bk dDoNo"']]),  # Enable Time Scraping
    Target([['span', 'class="ILfuVd"']]),
    Target([['div', 'class="LGOjhe"']]),
    Target([['div', 'class="rg_ilbg"']]),
    Target([['span', 'class="ILfuVd c3biWd"']]),
    Target([['div', 'class="Z0LcW"']]),
    Target([['span', 'class="tsp-di tsp-dt tsp-cp"']]),
]

HEADER_PAYLOAD = {  # Enables requests.get() to See the Same Web Page a Browser Does.
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'
}

