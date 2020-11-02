# SJTU EE208

import sys, os, lucene, threading
from datetime import datetime

from java.nio.file import Paths
from org.apache.lucene.analysis.miscellaneous import LimitTokenCountAnalyzer
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.analysis.core import SimpleAnalyzer
from org.apache.lucene.document import Document, Field, FieldType, StringField, TextField
from org.apache.lucene.index import IndexWriter, IndexWriterConfig, IndexOptions
from org.apache.lucene.store import SimpleFSDirectory

from Ticker import Ticker
from ExtractImgs import ExtractImgs


class IndexImgs(object):
    def __init__(self, store_dir, analyzer):
        '''
        Input: `store_dir`: directory to store the Lucene index
               `analyzer`: analyzer required to split the query
        '''
        # Initialize `IndexWriter`
        self.writer = self.get_writer(store_dir, analyzer)

        # Load data from `images.txt`
        self.images = self.load_images()

        # Initialize `Ticker`
        self.ticker = Ticker('Commit index')
        threading.Thread(target=self.ticker.run).start()

        # Index Images
        for img in self.images:
            try:
                print("Adding {}".format(img['img_url']))
                doc = self.get_doc(img)
                self.writer.addDocument(doc)
            except Exception as e:
                print("Failed to index image: {}".format(e))
        
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


    def load_images(self):
        '''
        Read image infos from file `images.txt`.

        Input: None
        Output: list containing image infos
        '''
        img_list = []
        with open('images.txt', 'r') as file:
            for l in file.readlines():
                img_url, contents, url, url_title = l.split('\t')
                url_title = url_title.strip()  # Remove the ending '\n'
                img = {
                    'img_url': img_url,
                    'description': contents,
                    'url': url,
                    'url_title': url_title
                }
                img_list.append(img)
        return img_list


    def get_doc(self, img):
        '''
        Generate a `Document` according to the parameters.

        Input: `img`: dict containing a single image info
        Output: `Document` with the fields initialized
        '''
        doc = Document()
        doc.add(StringField("img_url", img['img_url'], Field.Store.YES))
        doc.add(TextField("description", img['description'], Field.Store.YES))
        doc.add(StringField("url", img['url'], Field.Store.YES))
        doc.add(StringField("url_title", img['url_title'], Field.Store.YES))
        return doc


if __name__ == '__main__':

    #html_dir = sys.argv[1]
    store_dir = 'index'#sys.argv[2]

    lucene.initVM()
    print('lucene {}'.format(lucene.VERSION))

    start = datetime.now()
    try:
        # ExtractImgs(html_dir)
        IndexImgs(store_dir, SimpleAnalyzer())
        end = datetime.now()
        print(end - start)
    except Exception as e:
        print("Failed: {}".format(e))
        raise e