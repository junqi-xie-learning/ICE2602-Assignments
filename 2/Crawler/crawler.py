# SJTU EE208

import os
import re
import string
import urllib.error
import urllib.parse
import urllib.request

from bs4 import BeautifulSoup


def valid_filename(s):
    '''
    Convert the string to a valid filename

    Input: `s`: string to be converted
    Output: processed filename
    '''
    valid_chars = "-_.() {}{}".format(string.ascii_letters, string.digits)
    chars = []
    for c in s:
        if c in valid_chars:
            chars.append(c)
        else:
            chars.append('_')  # Replace invalid chars with '_'
    s = ''.join(chars)

    if s[-5:] != '.html' and s[-4:] != '.htm':
        s += '.htm'  # Add a suffix to indicate its filetype
    return s


def get_page(page):
    '''
    Get page content of the given URL

    Input: `page`: URL to be obtained
    Output: content of the URL given
    '''
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)\
                  Chrome/85.0.4183.102 Safari/537.36 Edg/85.0.564.51'
    req = urllib.request.Request(page)
    req.add_header('User-Agent', user_agent)  # Add user agent

    content = b''
    try:
        content = urllib.request.urlopen(req, timeout=1).read()  # Read the content of the page
    except:
        pass
    return content


def get_all_links(content, page):
    '''
    Get all the links in the page

    Input: `content`: HTML content to be parsed
           `page`: URL of the `content` (Used in `urljoin`)
    Output: all links in `content`
    '''
    links = []
    pattern1 = re.compile('^http.*')  # 'http://.../', 'https://.../'
    pattern2 = re.compile('^/{2}.*')  # '//.../'
    pattern3 = re.compile('^/{1}.*')  # '/.../'

    soup = BeautifulSoup(content)  # Load the HTML content into BeautifulSoup
    for i in soup.findAll('a'):  # Find the nodes tagged with 'a'
        link = i.get('href', '')  # Get their 'href' attributes
        if pattern1.match(link):
            links.append(link)
        elif pattern2.match(link):
            links.append(urllib.parse.urljoin('http:', link))
        elif pattern3.match(link):
            links.append(urllib.parse.urljoin(page, link))
    return links


def add_page_to_folder(page, content):  # 将网页存到文件夹里，将网址和对应的文件名写入index.txt中
    index_filename = 'index.txt'  # index.txt中每行是'网址 对应的文件名'
    folder = 'html'  # 存放网页的文件夹
    filename = valid_filename(page)  # 将网址变成合法的文件名
    index = open(index_filename, 'a')
    index.write(page + '\t' + filename + '\n')
    index.close()
    if not os.path.exists(folder):  # 如果文件夹不存在则新建
        os.mkdir(folder)
    f = open(os.path.join(folder, filename), 'wb')
    f.write(content)  # 将网页存入文件
    f.close()
