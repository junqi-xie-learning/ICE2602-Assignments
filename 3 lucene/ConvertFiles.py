# SJTU EE208

import os, threading
import re

from bs4 import BeautifulSoup
import jieba, string

from Ticker import Ticker


'''
This class will take input and output directory as arguments, and will \
convert all of the webpages in that directory into txt files using Jieba \
and downward recursively.  It will create `title.txt` to store the titles.
'''


class ConvertFiles(object):
    def __init__(self, root, store_dir):
        # Initialize paths
        self.root = root
        self.store_dir = store_dir
        self.title_filename = 'titles.txt'

        # Initialize `Ticker`
        self.ticker = Ticker('Converting Files')
        threading.Thread(target=self.ticker.run).start()

        # Convert HTMLs
        for root, dirnames, filenames in os.walk(self.root):
            for filename in filenames:
                if not filename.endswith('.htm') and not filename.endswith('.html'):
                    continue
                print("Converting {}".format(filename))
                try:
                    path = os.path.join(root, filename)

                    contents = self.get_contents(path)
                    tokenized = self.tokenize(contents)
                    if tokenized == []:
                        raise Exception('this page is empty')  # Some webpage is empty
                    
                    try:
                        title = contents.find('title').string.strip().replace('\n', '').replace('\t', ' ')
                    except:
                        title = ''  # The `title` tag of some webpage is empty
                    
                    self.write(filename, tokenized, title)
                except Exception as e:
                    print("Failed to convert doc: {}. Error: {}".format(filename, e))
        
        self.ticker.tick = False


    def write(self, filename, contents, title):
        '''
        Write tokenized contents to file, and title to `title.txt`

        Input: `filename`: original name of the file
               `contents`: tokenized contents of the file
               `title`: title of the file
        Output: None
        '''
        if not os.path.exists(self.store_dir):
            os.mkdir(self.store_dir)
        filename = filename + '.txt'  # Add the suffix of the file
        with open(os.path.join(self.store_dir, filename), 'w') as file:
            file.write(' '.join(contents))
        with open(self.title_filename, 'a') as file:
            file.write(filename + '\t' + title + '\n')


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


    def tokenize(self, contents):
        '''
        Tokenize contents using Jieba.

        Input: `contents`: contents of the file
        Output: list of words in the file
        '''
        # Whitespace, ascii puctuations and hanzi punctuations
        stop_chars = string.whitespace + string.punctuation \
            + '！？｡。＂＃＄％＆＇（）＊＋，－／：；＜＝＞＠［＼］＾＿｀｛｜｝～｟｠｢｣､、〃》「」『』【】〔〕〖〗〘〙〚〛〜〝〞〟〰〾〿–—‘’‛“”„‟…‧﹏'
        tokenized = []
        for s in jieba.cut(contents.text):  # Use Jieba to tokenize the contents
            if s not in stop_chars:
                tokenized.append(s)  # Remove whitespaces and punctuations
        return tokenized
