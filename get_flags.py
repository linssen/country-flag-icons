import re
import os
import codecs
import json

import requests
from bs4 import BeautifulSoup

WIKI_URL = 'http://en.wikipedia.org'
_here = os.path.dirname(__file__)
errors = []
countries = []


def main():
    with open(os.path.join(_here, 'licenses.csv'), 'w') as f:
        f.write('Alpha-3 code,English short name,License\n')

    r = requests.get('%s/wiki/ISO_3166-1' % WIKI_URL)
    soup = BeautifulSoup(r.text, 'html.parser')
    country_rows = soup.select('#mw-content-text table:nth-of-type(2) tr')[1:]
    print(f'Found {len(country_rows)} countries')
    for row in country_rows:
        get_flag_page(dict(
            url=row.select_one('td:nth-of-type(1) a')['href'],
            alpha3=row.select_one('td:nth-of-type(3)').get_text(),
            name=re.sub(r'\[\w+]', '', row.select_one('td:nth-of-type(1)').get_text()).strip().replace(',', ' -'),
        ))
    write_json(countries)
    print(f'Done with {len(errors)} errors')


def get_flag_page(country):
    r = requests.get(WIKI_URL + country['url'])
    soup = BeautifulSoup(r.text, 'html.parser')
    media_link = soup.find(title=re.compile('^Flag of'))
    if media_link is None:
        errors.append(f'No flag found for {country["name"]}')
        print(errors[-1])
        return False
    media_url = media_link['href']
    r = requests.get(WIKI_URL + media_url)
    soup = BeautifulSoup(r.text, 'html.parser')
    file_link = soup.select('#file > a')
    if len(file_link) == 0:
        errors.append(f'No flag found for "{country["name"]}"')
        print(errors[-1])
        return False
    country['file_url'] = file_link[0]['href']
    country['license'] = get_license(soup)

    download_flag(country)
    append_licenses(country)
    countries.append(country)


def get_license(page):
    """Find the location of the licensing info and regex for our magic words."""
    img_desc = page.select('#shared-image-desc')
    public_domain = re.compile(r'(?i)public domain')
    cc = re.compile(r'(?i)attribution-share alike (?P<version>\d+\.\d+) (?P<type>\w+)')
    non_protected = re.compile(r'(?i)non-protected works')

    if len(img_desc) == 0:
        img_desc = page.select('#mw-content-text .imbox-license')

    if img_desc[0].find(text=public_domain):
        return 'Public domain'
    if len(img_desc) > 1 and img_desc[1].find(text=public_domain):
        return 'Public domain'
    if img_desc[0].find(text=non_protected):
        return 'Non-protected works'

    if text := img_desc[0].find(text=cc):
        match = re.search(cc, text.get_text())
        return f'Creative Commons Attribution-Share Alike {match.group("version")} {match.group("type")}'


def append_licenses(country):
    with codecs.open(os.path.join(_here, 'licenses.csv'), 'a', 'utf-8') as f:
        f.write(','.join(
            [country['alpha3'], country['name'], country.get('license', 'Unknown')]
        ) + '\n')


def download_flag(country):
    file_name = os.path.basename(f'{country["alpha3"].lower()}.svg')
    path = os.path.join(_here, 'images', 'svg', file_name)
    r = requests.get('http:' + country['file_url'])
    print(f'Saving file: "{file_name}" for {country["name"]}')
    with open(path, 'wb') as f:
        for chunk in r.iter_content():
            f.write(chunk)


def write_json(countries):
    with codecs.open(os.path.join(_here, 'countries.json'), 'w', 'utf-8') as f:
        f.write(json.dumps(countries, indent=2))


if __name__ == '__main__':
    main()
