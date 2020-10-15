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
from org.apache.lucene.search import BooleanQuery
from org.apache.lucene.search import BooleanClause


'''
This script is loosely based on the Lucene (java implementation) demo class \
org.apache.lucene.demo.SearchFiles.  It will take `index` directory as an \
arguments, and will prompt for a search query, then it will search the Lucene \
index for the search query entered against the `contents` field.  It will \
then display the `path`, `title`, `url` and `name` fields for each of the \
hits it finds in the index.
'''


def parseCommand(command):
    '''
    input: C title:T author:A language:L
    output: {'contents':C, 'title':T, 'author':A, 'language':L}

    Sample:
    input:'contenance title:henri language:french author:william shakespeare'
    output:{'author': ' william shakespeare',
                   'language': ' french',
                   'contents': ' contenance',
                   'title': ' henri'}
    '''
    allowed_opt = ['title', 'author', 'language']
    command_dict = {}
    opt = 'contents'
    for i in command.split(' '):
        if ':' in i:
            opt, value = i.split(':')[:2]
            opt = opt.lower()
            if opt in allowed_opt and value != '':
                command_dict[opt] = command_dict.get(opt, '') + ' ' + value
        else:
            command_dict[opt] = command_dict.get(opt, '') + ' ' + i
    return command_dict


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

        # Store Analyzer
        self.analyzer = analyzer

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
            exit()
        return self.preprocess(command)


    def search(self, command):
        '''
        Search for the query in the Lucene index.

        Input: `command`: keyword to be searched
        Output: score_docs satisfying the requirement
        '''
        print()
        print("Searching for: ", command)
        command_dict = parseCommand(command)
        querys = BooleanQuery.Builder()
        for k,v in command_dict.items():
            query = QueryParser(k, self.analyzer).parse(v)
            querys.add(query, BooleanClause.Occur.MUST)
        return self.searcher.search(querys.build(), 50).scoreDocs


    def output(self, score_docs):
        '''
        Output the search results.

        Input: `score_docs`: search results
        Output: None
        '''
        print("{} total matching documents.".format(len(score_docs)))
        for score_doc in score_docs:
            doc = self.searcher.doc(score_doc.doc)
            print('path: {}, title: {}, url: {}, name: {}'.format(
                doc.get('path'), doc.get('title'), doc.get('url'), doc.get('name')))
        print()


if __name__ == '__main__':

    index_dir = sys.argv[1]

    lucene.initVM()
    print('lucene', lucene.VERSION)

    # SearchFiles('index', StandardAnalyzer())

    # Pass the Jieba function as a parameter for generalized preprocessing
    SearchFiles(index_dir, WhitespaceAnalyzer(), lambda x: ' '.join(jieba.cut(x)))