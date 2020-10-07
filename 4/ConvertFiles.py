# SJTU EE208

import os, threading

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
                if not filename.endswith('.htm'):
                    continue
                print("Converting {}".format(filename))
                try:
                    path = os.path.join(root, filename)
                    contents = self.get_contents(path)
                    tokenized = self.tokenize(contents)
                    title = contents.find('title').string
                    self.write(filename, tokenized, title)
                except Exception as e:
                    print("Failed to convert doc: {}".format(e))
        
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
        filename = filename[:-4] + '.txt'  # Change the suffix of the file
        with open(os.path.join(self.store_dir, filename), 'w') as file:
            file.write(' '.join(contents))
        with open(self.title_filename, 'a') as file:
            file.write(filename + '\t' + title + '\n')
    

    def get_contents(self, path):
        '''
        Read contents from file, and convert to `BeautifulSoup`.

        Input: `path`: path of the file
        Output: contents of the file
        '''
        with open(path, 'r') as file:
            contents = file.read()
        soup = BeautifulSoup(contents)  # Load the HTML content into BeautifulSoup
        if soup.find('meta').get('charset', '') == 'GB2312':
            contents.decode('gbk').encode('utf-8')
            soup = BeautifulSoup(contents)  # Convert coding and reload HTML contents
        return soup


    def tokenize(self, contents):
        '''
        Tokenize contents using Jieba.

        Input: `contents`: contents of the file
        Output: list of words in the file
        '''
        tokenized = []
        for s in jieba.cut(contents.text):
            if s not in string.whitespace + string.punctuation:
                tokenized.append(s)  # Remove whitespaces and punctuations
        return tokenized
