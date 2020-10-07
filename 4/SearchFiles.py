# SJTU EE208

import sys, os, lucene
import jieba

from java.io import File
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.analysis.core import WhitespaceAnalyzer
from org.apache.lucene.index import DirectoryReader
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.search import IndexSearcher


'''
This script is loosely based on the Lucene (java implementation) demo class \
org.apache.lucene.demo.SearchFiles.  It will take `index` directory as an \
arguments, and will prompt for a search query, then it will search the Lucene \
index for the search query entered against the `contents` field.  It will \
then display the `path`, `title`, `url` and `name` fields for each of the \
hits it finds in the index.
'''


class SearchFiles(object):
    def __init__(self, store_dir, analyzer, preprocess = lambda x: x):
        '''
        Input: `store_dir`: directory storing the Lucene index
               `analyzer`: analyzer required to split the query
               `preprocess`: user-defined preprocess function
        '''
        # Initialize `IndexSearcher`
        self.dir = SimpleFSDirectory(File(store_dir).toPath())
        self.searcher = IndexSearcher(DirectoryReader.open(self.dir))
        self.preprocess = preprocess

        # Initialize `QueryParser`
        self.parser = QueryParser("contents", analyzer)

        # Search docs
        print("Hit enter with no input to quit.")
        while True:
            command = self.get_input()
            score_docs = self.search(command)
            self.output(score_docs)
    

    def get_input(self):
        '''
        Get query input from terminal.

        Input: None
        Output: processed command
        '''
        command = input("Query: ")
        if command == '':
            return
        return self.preprocess(command)


    def search(self, command):
        '''
        Search for the query in the Lucene index.

        Input: `command`: keyword to be searched
        Output: score_docs satisfying the requirement
        '''
        print()
        print("Searching for: ", command)
        query = self.parser.parse(command)
        return self.searcher.search(query, 50).scoreDocs

    
    def output(self, score_docs):
        '''
        Output the search results.

        Input: `score_docs`: search results
        Output: None
        '''
        print("{} total matching documents.".format(len(score_docs)))
        for score_doc in score_docs:
            doc = self.searcher.doc(score_doc.doc)
            print('path: {}, title: {}, url: {}, name: {}.'.format(
                doc.get('path'), doc.get('title'), doc.get('url'), doc.get('name')))
        print()


if __name__ == '__main__':

    lucene.initVM()
    print('lucene', lucene.VERSION)

    # SearchFiles('index', StandardAnalyzer())

    # Pass the Jieba function as a parameter for generalized preprocessing
    SearchFiles('index', WhitespaceAnalyzer(), lambda x: ' '.join(jieba.cut(x)))