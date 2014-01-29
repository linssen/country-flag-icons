#!/usr/bin/env python
# encoding: utf-8
import re
import os
import urllib

import requests
from bs4 import BeautifulSoup

WIKI_URL = u'http://en.wikipedia.org'

def main():
    r = requests.get('%s/wiki/ISO_3166-1' % WIKI_URL)
    soup = BeautifulSoup(r.text, 'html5lib')
    country_rows = soup.select('#mw-content-text table:nth-of-type(1) tr')
    for row in country_rows[1:]:
        get_flag_url(dict(
            url=row.select('td:nth-of-type(1) a')[0]['href'],
            alpha3=row.select('td:nth-of-type(3)')[0].get_text(),
            name=row.select('td:nth-of-type(1')[0].get_text(),
        ))

def get_flag_url(country):
    r = requests.get(WIKI_URL + country['url'])
    soup = BeautifulSoup(r.text, 'html5lib')
    media_link = soup.find(title=re.compile('^Flag of'))
    if media_link is None:
        print 'No flag found for \'%s\'' % country['name']
        return False
    media_url = media_link['href']
    r = requests.get(WIKI_URL + media_url)
    soup = BeautifulSoup(r.text, 'html5lib')
    country['file_url'] = soup.select('#file > a')[0]['href']
    download_flag(country)

def download_flag(country):
    file_name = os.path.basename('%s.svg' % country['alpha3'])
    file_name = urllib.unquote(file_name).decode('utf8').lower()
    path = os.path.join(os.path.dirname(__file__), 'images', file_name)
    r = requests.get('http:' + country['file_url'])
    print 'Saving file: \'%s\' for %s' % (file_name, country['name'])
    with open(path, 'wb') as f:
        for chunk in r.iter_content():
            f.write(chunk)

if __name__ == '__main__':
    main()