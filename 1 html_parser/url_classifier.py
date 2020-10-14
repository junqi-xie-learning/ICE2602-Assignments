# SJTU EE208
# Based on `example1.py`

import re
import sys
import urllib.request

from bs4 import BeautifulSoup


def parseURL(content):
    pattern1 = re.compile('^http://.*')  # 'http://.../'
    pattern2 = re.compile('^https://.*')  # 'https://.../'
    pattern3 = re.compile('^/{2}.*')  # '//.../'
    pattern4 = re.compile('^/{1}.*')  # '/.../'
    # The JavaScript links are ignored

    urlsetdict = { pattern1: set(), pattern2: set(),
                   pattern3: set(), pattern4: set() }

    soup = BeautifulSoup(content)  # Load the HTML content into BeautifulSoup
    for i in soup.findAll('a'):  # Find the nodes tagged with 'a'
        link = i.get('href', '') # Get their 'href' attributes
        for pattern in urlsetdict:
            if pattern.match(link): # Try all the possible patterns
                urlsetdict[pattern].add(link)
                break

    return urlsetdict


def write_outputs(urlsetdict, filename):
    file = open(filename, 'w', encoding='utf-8')
    for pattern in urlsetdict:
        for i in urlsetdict[pattern]:
            file.write(i)
            file.write('\n')
        file.write('\n') # Use empty lines to seperate different patterns
    file.close()


def main():
    url = "http://www.baidu.com/"
    content = urllib.request.urlopen(url).read()
    urlSetDict = parseURL(content)
    write_outputs(urlSetDict, "classified.txt")


if __name__ == '__main__':
    main()
