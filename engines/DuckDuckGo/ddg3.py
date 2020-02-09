#!/usr/bin/env python3

import requests
from urllib.parse import urlencode
from xml.etree import ElementTree

__version__ = '0.6.6'
_useragent = 'ddg3 {}'.format(__version__)


def query(query, useragent=_useragent):
    '''
    Query Duck Duck Go, returning a Results object.

    Here's a query that's unlikely to change:

    >>> result = query('1 + 1')
    >>> result.type
    'nothing'
    >>> result.answer.text
    '1 + 1 = 2'
    >>> result.answer.type
    'calc'
    '''

    params = urlencode({'q': query, 'o': 'x'})
    
    url = 'http://duckduckgo.com/?{}'.format(params)

    request = requests.get(url, headers={'User-Agent': useragent})
    response = request.text
    xml = ElementTree.fromstring(response)
    return Results(xml)


class Results(object):

    def __init__(self, xml):
        self.type = {
            'A': 'answer',
            'D': 'disambiguation',
            'C': 'category',
            'N': 'name',
            'E': 'exclusive',
            '': 'nothing'
        }[xml.findtext('Type', '')]

        self.api_version = xml.attrib.get('version', None)

        self.heading = xml.findtext('Heading', '')

        self.results = [Result(elem) for elem in xml.getiterator('Result')]
        self.related = [
            Result(elem) for elem in
            xml.getiterator('RelatedTopic')
        ]

        self.abstract = Abstract(xml)

        answer_xml = xml.find('Answer')
        if answer_xml is not None:
            self.answer = Answer(answer_xml)
            if not self.answer.text:
                self.answer = None
        else:
            self.answer = None

        image_xml = xml.find('Image')
        if image_xml is not None and image_xml.text:
            self.image = Image(image_xml)
        else:
            self.image = None


class Abstract(object):

    def __init__(self, xml):
        self.html = xml.findtext('Abstract', '')
        self.text = xml.findtext('AbstractText', '')
        self.url = xml.findtext('AbstractURL', '')
        self.source = xml.findtext('AbstractSource')


class Result(object):

    def __init__(self, xml):
        self.html = xml.text
        self.text = xml.findtext('Text')
        self.url = xml.findtext('FirstURL')

        icon_xml = xml.find('Icon')
        if icon_xml is not None:
            self.icon = Image(icon_xml)
        else:
            self.icon = None


class Image(object):

    def __init__(self, xml):
        self.url = xml.text
        self.height = xml.attrib.get('height', None)
        self.width = xml.attrib.get('width', None)


class Answer(object):

    def __init__(self, xml):
        self.text = xml.text
        self.type = xml.attrib.get('type', '')


def main():
    import sys
    from optparse import OptionParser

    parser = OptionParser(
        usage='usage: %prog [options] query',
        version='ddg3 {}'.format(__version__)
    )
    parser.add_option(
        '-o',
        '--open',
        dest='open',
        action='store_true',
        help='open results in a browser'
    )
    parser.add_option(
        '-n',
        dest='n',
        type='int',
        default=3,
        help='number of results to show'
    )
    parser.add_option(
        '-d',
        dest='d',
        type='int',
        default=None,
        help='disambiguation choice'
    )
    (options, args) = parser.parse_args()
    q = ' '.join(args)

    if options.open:
        import urllib
        import webbrowser

        webbrowser.open(
            'http://duckduckgo.com/?{}'.format(
                urllib.urlencode(dict(q=q)),
                new=2
            )
        )

        sys.exit(0)

    results = query(q)

    if options.d and results.type == 'disambiguation':
        try:
            related = results.related[options.d - 1]
        except IndexError:
            print('Invalid disambiguation number.')
            sys.exit(1)
        results = query(related.url.split('/')[-1].replace('_', ' '))

    if results.answer and results.answer.text:
        print('Answer: {}\n'.format(results.answer.text))
    elif results.abstract and results.abstract.text:
        print('{}\n'.format(results.abstract.text))

    if results.type == 'disambiguation':
        print(
            '''
            '{}' can mean multiple things. You can re-run your query
            and add '-d #' where '#' is the topic number you're
            interested in.
            '''.format(q).replace('\n', '').replace('\t', ' ')
        )

        for i, related in enumerate(results.related[0:options.n]):
            name = related.url.split('/')[-1].replace('_', ' ')
            summary = related.text
            if len(summary) < len(related.text):
                summary += '...'
            print('{}. {}: {}\n'.format(i + 1, name, summary))
    else:
        for i, result in enumerate(results.results[0:options.n]):
            summary = result.text[0:70].replace('&nbsp;', ' ')
            if len(summary) < len(result.text):
                summary += '...'
            print('{}. {}'.format(i + 1, summary))
            print('  <{}>\n'.format(result.url))


if __name__ == '__main__':
    main()
