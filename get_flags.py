#!/usr/bin/env python
# encoding: utf-8
import re
import os
import urllib
import codecs

import requests
from bs4 import BeautifulSoup

WIKI_URL = u'http://en.wikipedia.org'
_here = os.path.dirname(__file__)


def main():
    with open(os.path.join(_here, 'licenses.csv'), 'wb') as f:
        f.write('Alpha-3 code,English short name,License\n')

    r = requests.get('%s/wiki/ISO_3166-1' % WIKI_URL)
    soup = BeautifulSoup(r.text, 'html5lib')
    country_rows = soup.select('#mw-content-text table:nth-of-type(1) tr')
    for row in country_rows[1:]:
        get_flag_page(dict(
            url=row.select('td:nth-of-type(1) a')[0]['href'],
            alpha3=row.select('td:nth-of-type(3)')[0].get_text(),
            name=row.select('td:nth-of-type(1) a')[0].get_text().replace(',', ' -'),
        ))

def get_flag_page(country):
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
    country['license'] = get_license(soup)

    download_flag(country)
    append_licenses(country)

def get_license(page):
    """Find the location of the licensing info and regex for our magic words."""
    img_desc = page.select('#shared-image-desc')
    if len(img_desc) == 0:
        img_desc = page.select('#mw-content-text .imbox-license')

    if img_desc[0].find(text=re.compile(r'(?i)public domain')):
        return 'Public domain'
    if img_desc[0].find(text=re.compile(r'(?i)non-protected works')):
        return 'Non-protected works'
    if img_desc[0].find(text=re.compile(r'(?i)attribution-share alike 2\.5 generic')):
        return 'Creative Commons Attribution-ShareAlike 2.5 Generic'
    if img_desc[0].find(text=re.compile(r'(?i)attribution-share alike 3\.0 unported')):
        return 'Creative Commons Attribution-Share Alike 3.0 Unported'

def append_licenses(country):
    with codecs.open(os.path.join(_here, 'licenses.csv'), 'a', 'utf-8') as f:
        f.write(','.join(
            [country['alpha3'], country['name'], country['license']]
        ) + '\n')

def download_flag(country):
    file_name = os.path.basename('%s.svg' % country['alpha3'])
    file_name = urllib.unquote(file_name).decode('utf8').lower()
    path = os.path.join(_here, 'images', 'svg', file_name)
    r = requests.get('http:' + country['file_url'])
    print 'Saving file: \'%s\' for %s' % (file_name, country['name'])
    with open(path, 'wb') as f:
        for chunk in r.iter_content():
            f.write(chunk)

if __name__ == '__main__':
    main()