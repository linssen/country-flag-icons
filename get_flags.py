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
    country_urls = [a['href'] for a in soup.select('#mw-content-text table:nth-of-type(1) tr > td:nth-of-type(1) > a')]
    for country_url in country_urls[]:
        # print 'Looking for \'%s\'' % country_url
        get_flag_url(country_url)

def get_flag_url(country_url):
    r = requests.get(WIKI_URL + country_url)
    soup = BeautifulSoup(r.text, 'html5lib')
    media_url = soup.find(title=re.compile('^Flag of'))['href']
    # print 'Found media page: \'%s\'' % media_url

    r = requests.get(WIKI_URL + media_url)
    soup = BeautifulSoup(r.text, 'html5lib')
    file_url = soup.select('#file > a')[0]['href']
    # print 'Found file: \'%s\'' % file_url
    download_flag(file_url)

def download_flag(file_url):
    file_name = os.path.basename(file_url)
    file_name = urllib.unquote(file_name).decode('utf8').lower()
    path = os.path.join(os.path.dirname(__file__), 'images', file_name)
    r = requests.get(WIKI_URL + file_url)
    print 'Saving file: \'%s\'' % file_name
    with open(path, 'wb') as f:
        for chunk in r.iter_content():
            f.write(chunk)

if __name__ == '__main__':
    main()