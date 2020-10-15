# SJTU EE208

import sys, os, lucene, threading
from datetime import datetime
from urllib.parse import urlparse

from java.nio.file import Paths
from org.apache.lucene.analysis.miscellaneous import LimitTokenCountAnalyzer
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.analysis.core import WhitespaceAnalyzer
from org.apache.lucene.document import Document, Field, FieldType, StringField, TextField
from org.apache.lucene.index import FieldInfo, IndexWriter, IndexReader ,IndexWriterConfig, Term, DirectoryReader
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.search import IndexSearcher, TermQuery
from org.apache.lucene.util import Version

from Ticker import Ticker


class IndexUpdate(object):
    def __init__(self, root, original_dir, store_dir, analyzer):
        '''
        Input: `root`: directory storing the documents
               `original_dir`: directory storing the original Lucene index
               `store_dir`: directory to store the new Lucene index
               `analyzer`: analyzer required to split the query
        '''
        # Initialize `IndexWriter` and `IndexSearcher`
        self.writer = self.get_writer(store_dir, analyzer)
        self.searcher = self.get_searcher(original_dir)
        self.root = root

        # Initialize `Ticker`
        self.ticker = Ticker('Commit index')
        threading.Thread(target=self.ticker.run).start()

        # Update Docs
        for root, dirnames, filenames in os.walk(self.root):
            for filename in filenames:
                if not filename.endswith('.txt'):
                    continue
                print("Updating {}".format(filename))
                try:
                    # Remove the original doc and get the info
                    name = filename[:-4]
                    term = Term('name', name)
                    doc_info = self.search(term)
                    self.writer.deleteDocuments(term)

                    # Add `site` field and add the new doc
                    doc_info['site'] = urlparse(doc_info['url']).netloc  # Get the `site` of the url
                    filepath = os.path.join(root, filename)  # Path of the doc file
                    contents = self.get_contents(filepath)
                    doc = self.get_doc(doc_info, contents)
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
        # analyzer = LimitTokenCountAnalyzer(analyzer, 1048576)
        config = IndexWriterConfig(analyzer)
        config.setOpenMode(IndexWriterConfig.OpenMode.CREATE)

        return IndexWriter(store, config)


    def get_searcher(self, original_dir):
        '''
        Generate an `IndexSearcher` according to the parameters.

        Input: `original_dir`: directory storing the original Lucene index
        Output: `IndexSearcher` with the correct parameters
        '''
        store = SimpleFSDirectory(Paths.get(original_dir))
        reader = DirectoryReader.open(store)
        return IndexSearcher(reader)


    def search(self, term):
        '''
        Search the original Lucene index for the desired doc.

        Input: `term`: Term specifying the doc
        Output: dict containing the infomation of the doc
        '''
        query = TermQuery(term)
        score_doc = self.searcher.search(query, 50).scoreDocs[0]
        doc = self.searcher.doc(score_doc.doc)
        doc_info = {
            "name": doc.get('name'),
            "path": doc.get('path'),
            "title": doc.get('title'),
            "url": doc.get('url')
        }
        return doc_info


    def get_contents(self, path):
        '''
        Read contents from the file.

        Input: `path`: path of the file
        Output: contents of the file
        '''
        with open(path, 'r') as file:
            contents = file.read()
        return contents
    

    def get_doc(self, doc_info, contents):
        '''
        Generate a `Document` according to the given info.

        Input: `doc_info`: info of the doc (`name`, `path`, `title`, `url`, `site`)
               `contents`: contents of the webpage
        Output: `Document` with the fields initialized
        '''
        doc = Document()
        doc.add(StringField("name", doc_info['name'], Field.Store.YES))
        doc.add(StringField("path", doc_info['path'], Field.Store.YES))
        doc.add(TextField("title", doc_info['path'], Field.Store.YES))
        doc.add(TextField("url", doc_info['url'], Field.Store.YES))
        doc.add(TextField("site", doc_info['site'], Field.Store.YES))
        if len(contents) > 0:
            doc.add(TextField("contents", contents, Field.Store.YES))
        else:
            print("Warning: No content in {}".format(doc_info['name']))
        return doc


if __name__ == '__main__':

    doc_dir = sys.argv[1]
    original_dir = sys.argv[2]
    store_dir = sys.argv[3]

    lucene.initVM()
    print('lucene {}'.format(lucene.VERSION))

    start = datetime.now()
    try:
        # fn = 'pg17565.txt'
        # IndexUpdate('testfolder', 'index', 'index', StandardAnalyzer())

        IndexUpdate(doc_dir, original_dir, store_dir, WhitespaceAnalyzer())
        end = datetime.now()
        print(end - start)
    except Exception as e:
        print("Failed: {}".format(e))
        raise e