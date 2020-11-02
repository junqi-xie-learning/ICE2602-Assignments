# SJTU EE208

from flask import Flask, redirect, render_template, request, url_for
import lucene, jieba

from org.apache.lucene.analysis.core import SimpleAnalyzer
from SearchFiles import SearchFiles

app = Flask(__name__)


def search(request):
    keyword = request.form['keyword']
    return redirect(url_for('result', keyword=keyword))


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == "POST":
        return search(request)
    return render_template("index.html")


@app.route('/result', methods=['POST', 'GET'])
def result():
    if request.method == "POST":
        return search(request)
    
    vm_env.attachCurrentThread()
    engine = SearchFiles('index', SimpleAnalyzer(), lambda x: ' '.join(jieba.cut(x)))
    keyword = request.args.get('keyword')
    results = engine.search_command(keyword)
    return render_template("result.html", keyword=keyword, results=results)


vm_env = None  # To be initialized in __main__
if __name__ == '__main__':
    vm_env = lucene.initVM()
    print('lucene', lucene.VERSION)
    app.run(debug=True, port=8080)
