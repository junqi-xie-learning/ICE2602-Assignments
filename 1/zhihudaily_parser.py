# SJTU EE208
# Based on `example3.py`

import re
import sys
import urllib.parse
import urllib.request

import argparse # Package for paring arguments

from bs4 import BeautifulSoup


def parseZhihuDaily(content, url):
    zhihulist = list()
    ########################
    # write your code here
    ########################

    soup = BeautifulSoup(content) # Load the HTML content into BeautifulSoup
    # Each box is characterized by <a href='...' class='link-button'> ... </a>
    for i in soup.findAll('a', {'class': 'link-button'}):
        linkpage = i.get('href', '')
        url = urllib.parse.urljoin(url, linkpage) # Convert relative address into the absolute address

        contents = i.contents # Move to the contents of label 'a'
        img = contents[0].get('src', '') # Get the image source
        title = contents[1].string # Get the text of the title

        zhihu = [img, title, url]
        zhihulist.append(zhihu)
    
    return zhihulist


def write_outputs(zhihus, filename):
    file = open(filename, "w", encoding='utf-8')
    for zhihu in zhihus:
        for element in zhihu:
            file.write(element)
            file.write('\t')
        file.write('\n')
    file.close()


def main(config):
    url = "http://daily.zhihu.com/"
    req = urllib.request.Request(url)
    if config.user_agent: # Examine whether the user provided a customized user agent
        req.add_header('User-Agent', config.user_agent) # Add user agent

    content = urllib.request.urlopen(req).read()
    zhihus = parseZhihuDaily(content, url)
    write_outputs(zhihus, "res3.txt")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    # usage:
    # 3.py --user_agent {customized User-Agent}

    # Add the customized User-Agent as a parameter
    parser.add_argument("--user_agent", type = str, help = "customized User-Agent")
    config = parser.parse_args()

    main(config)
