# SJTU EE208
# Based on `example1.py`

import re
import sys
import urllib.request

from bs4 import BeautifulSoup


def parseURL(content):
    urlset = set()
    ########################
    # write your code here
    ########################

    soup = BeautifulSoup(content) # Load the HTML content into BeautifulSoup
    # Hyperlink: <a href="...">
    for i in soup.findAll('a'): # Find the nodes tagged with 'a'
        urlset.add(i.get('href', '')) # Get their 'href' attributes
    
    return urlset


def write_outputs(urls, filename):
    file = open(filename, 'w', encoding='utf-8')
    for i in urls:
        file.write(i)
        file.write('\n')
    file.close()


def main():
    url = "http://www.baidu.com/"
    content = urllib.request.urlopen(url).read()
    urlSet = parseURL(content)
    write_outputs(urlSet, "res1.txt")


if __name__ == '__main__':
    main()
