# SJTU EE208

import os, threading
import re

from bs4 import BeautifulSoup
import jieba, urllib

from Ticker import Ticker


class ExtractImgs(object):
    def __init__(self, root):
        # Initialize paths
        self.root = root
        self.image_filename = 'images.txt'

        # Load data from `index.txt`
        self.urls = self.load_urls()

        # Initialize `Ticker`
        self.ticker = Ticker('Extracting Images')
        threading.Thread(target=self.ticker.run).start()

        # Convert HTMLs
        for root, dirnames, filenames in os.walk(self.root):
            for filename in filenames:
                if not filename.endswith('.htm') and not filename.endswith('.html'):
                    continue
                print("Extracting images from {}".format(filename))
                try:
                    path = os.path.join(root, filename)
                    contents = self.get_contents(path)
                    try:
                        title = contents.find('title').string.strip().replace('\n', '').replace('\t', ' ')
                    except:
                        title = ''  # The `title` tag of some webpage is empty

                    for img_url, description in self.extract_img(contents, self.urls[filename]):
                        description = ' '.join(jieba.cut(description)).strip().replace('\n', '').replace('\t', ' ')
                        self.write(img_url, description, self.urls[filename], title)
                except Exception as e:
                    print("Failed to convert doc: {}. Error: {}".format(filename, e))
        
        self.ticker.tick = False


    def write(self, img_url, contents, url, url_title):
        '''
        Write extracted images to `images.txt`

        Input: `img_url`: url of the image
               `contents`: tokenized description of the image
               `url`: url of the webpage containing the image
               `url_title`: title of the webpage containing the image
        Output: None
        '''
        with open(self.image_filename, 'a') as file:
            file.write('\t'.join([img_url, contents, url, url_title]) + '\n')


    def load_urls(self):
        '''
        Read urls from file `index.txt`.

        Input: None
        Output: dict containing the filenames and their corresponding urls
        '''
        urls = { }
        with open('index.txt', 'r') as file:
            for l in file.readlines():
                url, filename = l.split('\t')
                filename = filename.strip()
                urls[filename] = url
        return urls


    def get_encoding(self, contents):
        '''
        Get the encoding of the HTML contents.

        Input: `contents`: contents of the HTML page
        Output: encoding of the contents, converted to lower case
        '''
        soup = BeautifulSoup(contents)  # Load the HTML content into BeautifulSoup
        pattern = re.compile('text/html; charset=(\w+)')
        for i in soup.find_all('meta'):
            try:
                # <meta charset=utf-8/gb2312>
                encoding = i.get('charset', '')
                return encoding.lower()
            except:
                pass
            # <meta content="text/html; charset=utf-8/gb2312">
            matching = pattern.match(i.get('content', ''))
            if matching:
                return matching.group(1).lower()


    def get_contents(self, path):
        '''
        Read contents from file, and convert to `BeautifulSoup`. Change the encoding when necessary.

        Input: `path`: path of the file
        Output: contents of the file
        '''
        with open(path, 'rb') as file:
            contents = file.read()
        if self.get_encoding(contents) == 'gb2312':
            contents.decode('gbk').encode('utf-8')  # Convert 'gb2312' files to 'unicode'
        soup = BeautifulSoup(contents)  # Load the HTML content into BeautifulSoup
        return soup


    def extract_img(self, contents, url):
        '''
        Extract image labels from contents.

        Input: `contents`: contents of the file
        Output: list of images in the file
        '''
        img_list = []

        # Each box is characterized by <div class='info'> ... </div>
        for i in contents.findAll('div', {'class': 'info'}):
            img_url = i.find('img')
            if img_url:  # Check if the box contains an image
                img_url = img_url.get('src', '')  # Get the image source
                img_url = urllib.parse.urljoin(url, img_url)  # Convert relative address into the absolute address

                description = i.find('p')  # Get the description of the image
                description = description.text

                img = [img_url, description]
                img_list.append(img)
        return img_list
