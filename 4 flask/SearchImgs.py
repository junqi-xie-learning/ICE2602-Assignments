# SJTU EE208

from java.io import File
from org.apache.lucene.index import DirectoryReader
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.search import IndexSearcher


class SearchImgs(object):
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
        self.parser = QueryParser("description", analyzer)


    def search_command(self, command):
        '''
        Interface for other programs to search in a particular index.

        Input: `command`: raw query in the str format
        Output: list of documents found in the index
        '''
        command = self.preprocess(command)
        score_docs = self.search(command)
        return self.output(score_docs)


    def search(self, command):
        '''
        Search for the query in the Lucene index.

        Input: `command`: keyword to be searched
        Output: score_docs satisfying the requirement
        '''
        query = self.parser.parse(command)
        return self.searcher.search(query, 50).scoreDocs


    def output(self, score_docs):
        '''
        Highlight and return the search results.

        Input: `score_docs`: search results from the index
        Output: list of documents info found in the index,
                details includes `title`, `url` and `description` and `action_url`
        '''
        results = []
        for score_doc in score_docs:
            doc = self.searcher.doc(score_doc.doc)
            result = {
                'title': doc.get('url_title'),
                'url': doc.get('img_url'),
                'description': doc.get('description').replace(' ', ''),
                'action_url': doc.get('url')
            }
            results.append(result)
        return results
