# SJTU EE208

import sys, os, lucene, threading
from datetime import datetime

from java.nio.file import Paths
from org.apache.lucene.analysis.miscellaneous import LimitTokenCountAnalyzer
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.analysis.core import WhitespaceAnalyzer
from org.apache.lucene.document import Document, Field, FieldType
from org.apache.lucene.index import IndexWriter, IndexWriterConfig, IndexOptions
from org.apache.lucene.store import SimpleFSDirectory

from Ticker import Ticker
from ConvertFiles import ConvertFiles


'''
This class is loosely based on the Lucene (java implementation) demo class \
org.apache.lucene.demo.IndexFiles.  It will take `html`, `docs` and `index` \
directory as arguments, and will index all of the webpages in that directory \
and downward recursively.  It will index on the file name, path, title, url \
and the contents.
'''


class IndexFiles(object):
    def __init__(self, root, store_dir, analyzer):
        '''
        Input: `root`: directory stroing the documents
               `store_dir`: directory to store the Lucene index
               `analyzer`: analyzer required to split the query
        '''
        # Initialize `IndexWriter`
        self.writer = self.get_writer(store_dir, analyzer)
        self.root = root

        # Initialize `FieldType`
        self.file_type = self.get_field_type(True, False)
        self.title_type = self.get_field_type(True, True)
        self.content_type = self.get_field_type(False, True)

        # Load data from `index.txt` and `titles.txt`
        self.titles = self.load_titles()
        self.urls = self.load_urls()

        # Initialize `Ticker`
        self.ticker = Ticker('Commit index')
        threading.Thread(target=self.ticker.run).start()

        # Index Docs
        for root, dirnames, filenames in os.walk(self.root):
            for filename in filenames:
                if not filename.endswith('.txt'):
                    continue
                print("Adding {}".format(filename))
                try:
                    path = os.path.join(root, filename)
                    contents = self.get_contents(path)
                    title = self.titles[filename]
                    url = self.urls[filename]
                    doc = self.get_doc(filename, path, title, url, contents)
                    self.writer.addDocument(doc)
                except Exception as e:
                    print("Failed to index doc: {}".format(e))
        
        self.writer.commit()
        self.writer.close()
        self.ticker.tick = False


    def get_writer(self, store_dir, analyzer):
        '''
        Generate an `IndexWriter` according to the parameters.

        Input: `store_dir`: directory to store the Lucene index
               `analyzer`: analyzer used to analyze the docs
        Output: `IndexWriter` with the correct parameters
        '''
        # Initialize the `store_dir`
        if not os.path.exists(store_dir):
            os.mkdir(store_dir)
        store = SimpleFSDirectory(Paths.get(store_dir))

        # Generate an analyzer according to parameters
        analyzer = LimitTokenCountAnalyzer(analyzer, 1048576)
        config = IndexWriterConfig(analyzer)
        config.setOpenMode(IndexWriterConfig.OpenMode.CREATE)

        return IndexWriter(store, config)


    def get_field_type(self, stored, indexed):
        '''
        Generate a `FieldType` according to the parameters.

        Input: `stored`: whether the field is stored
               `indexed`: whether the field is indexed
        Output: `FieldType` with the correct parameters
        '''
        t = FieldType()
        t.setStored(stored)
        t.setTokenized(indexed)
        if indexed:  # Indexes documents, frequencies and positions
            t.setIndexOptions(IndexOptions.DOCS_AND_FREQS_AND_POSITIONS)
        else:  # Not indexed
            t.setIndexOptions(IndexOptions.NONE)
        return t
    

    def load_titles(self):
        '''
        Read titles from file `titles.txt`.

        Input: None
        Output: None
        '''
        titles = { }
        with open('titles.txt', 'r') as file:
            for l in file.readlines():
                filename, title = l.split('\t')
                title = title.strip()  # Remove the ending '\n'
                titles[filename] = title
        return titles
    

    def load_urls(self):
        '''
        Read urls from file `index.txt`.

        Input: None
        Output: None
        '''
        urls = { }
        with open('index.txt', 'r') as file:
            for l in file.readlines():
                url, filename = l.split('\t')
                filename = filename.strip()[:-4] + '.txt'  # Legacy Problem: change the suffix of the file
                urls[filename] = url
        return urls


    def get_contents(self, path):
        '''
        Read contents from the file.

        Input: `path`: path of the file
        Output: contents of the file
        '''
        with open(path, 'r') as file:
            contents = file.read()
        return contents


    def get_doc(self, filename, path, title, url, contents):
        '''
        Generate a `Document` according to the parameters.

        Input: `filename`: filename of the webpage
               `path`: path of the webpage
               `title`: title of the webpage
               `url`: original url of the webpage
               `contents`: contents of the webpage
        Output: `Document` with the fields initialized
        '''
        doc = Document()
        doc.add(Field("name", filename, self.file_type))
        doc.add(Field("path", path, self.file_type))
        doc.add(Field("title", title, self.title_type))
        doc.add(Field("url", url, self.file_type))
        if len(contents) > 0:
            doc.add(Field("contents", contents, self.content_type))
        else:
            print("Warning: No content in {}".format(filename))
        return doc


if __name__ == '__main__':

    html_dir = sys.argv[1]
    doc_dir = sys.argv[2]
    store_dir = sys.argv[3]

    lucene.initVM()
    print('lucene {}'.format(lucene.VERSION))

    start = datetime.now()
    try:
        # IndexFiles('test_folder', 'index', StandardAnalyzer())

        ConvertFiles(html_dir, doc_dir)
        IndexFiles(doc_dir, store_dir, WhitespaceAnalyzer())
        end = datetime.now()
        print(end - start)
    except Exception as e:
        print("Failed: {}".format(e))
        raise e