# SJTU EE208
# Based on `example1.py`

import re
import sys
import urllib.request

from bs4 import BeautifulSoup


def parseIMG(content):
    imgset = set()
    ########################
    # write your code here
    ########################

    soup = BeautifulSoup(content) # Load the HTML content into BeautifulSoup
    # Image: <img src="...">
    for i in soup.findAll('img'): # Find the nodes tagged with 'img'
        imgset.add(i.get('src', '')) # Get their 'src' attributes
    
    return imgset


def write_outputs(urls, filename):
    file = open(filename, 'w', encoding='utf-8')
    for i in urls:
        file.write(i)
        file.write('\n')
    file.close()


def main():
    url = "http://www.baidu.com/"
    content = urllib.request.urlopen(url).read()
    urlSet = parseIMG(content)
    write_outputs(urlSet, "res2.txt")


if __name__ == '__main__':
    main()
