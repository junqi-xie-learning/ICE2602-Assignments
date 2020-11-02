# SJTU EE208

from java.io import File
from org.apache.lucene.index import DirectoryReader
from org.apache.lucene.analysis.core import SimpleAnalyzer
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.search import IndexSearcher
from org.apache.lucene.search import BooleanQuery
from org.apache.lucene.search import BooleanClause

from org.apache.lucene.search.highlight import Highlighter, QueryScorer, SimpleFragmenter, SimpleHTMLFormatter


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

        # Initialize `Formatter`
        self.formatter = SimpleHTMLFormatter('<em>', '</em>')
    

    def search_command(self, command):
        '''
        Interface for other programs to search in a particular index.

        Input: `command`: raw query in the str format
        Output: list of documents found in the index
        '''
        command = self.parse_command(command)
        command['contents'] = self.preprocess(command['contents'])
        score_docs = self.search(command)
        return self.output(score_docs, command['contents'])


    def parse_command(self, command):
        '''
        Parse the input command and convert it into a command dict.

        Input: `command`: query in the format `C site:S`
        Output: dict in the format `{ 'contents': C, 'site': S }`
        '''
        allowed_opt = ['site']
        opt = 'contents'
        command_dict = { opt: '' }

        for i in command.split(' '):
            if ':' in i:
                opt, value = i.split(':')
                opt = opt.lower()
                if opt in allowed_opt:
                    command_dict[opt] = value
            else:
                command_dict[opt] += ' ' + i
        return command_dict


    def search(self, command_dict):
        '''
        Search for the query in the Lucene index.

        Input: `command_dict`: dict containing preprocessed query
        Output: score_docs satisfying the requirement
        '''
        querys = BooleanQuery.Builder()
        for k, v in command_dict.items():
            query = QueryParser(k, self.analyzer).parse(v)
            querys.add(query, BooleanClause.Occur.MUST)
        return self.searcher.search(querys.build(), 50).scoreDocs


    def output(self, score_docs, command):
        '''
        Highlight and return the search results.

        Input: `score_docs`: search results from the index
        Output: list of documents found in the index
                the information contains `title`, `url` and `abstract`
        '''
        query = QueryParser('contents', self.analyzer).parse(command)
        highlighter = Highlighter(self.formatter, QueryScorer(query))
        highlighter.setTextFragmenter(SimpleFragmenter(25))  # Limit the max number of characters

        results = []
        for score_doc in score_docs:
            doc = self.searcher.doc(score_doc.doc)
            contents = doc.get('contents')
            stream = self.analyzer.tokenStream("contents", contents)
            abstract = highlighter.getBestFragment(stream, contents)  # Get the abstract and highlight
            result = {
                'title': doc.get('title'),
                'url': doc.get('url'),
                'abstract': abstract
            }
            results.append(result)
        return results
