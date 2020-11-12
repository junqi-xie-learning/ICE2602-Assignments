# SJTU EE208

from flask import Flask, redirect, render_template, request, url_for
import lucene, jieba

from org.apache.lucene.analysis.core import SimpleAnalyzer
from SearchFiles import SearchFiles
from SearchImgs import SearchImgs

app = Flask(__name__)


def render_index(request, template, result):
    '''
    Render 'index' page for website and image search.

    Input: `request`: `request` variable received
           `template`: template HTML file
           `result`: relative path of 'result' page
    '''
    if request.method == "POST":
        keyword = request.form['keyword']
        return redirect(url_for(result, keyword=keyword))
    return render_template(template)


def render_result(request, template, result, Search, index):
    '''
    Render 'result' page for website and image search.

    Input: `request`: `request` variable received
           `template`: template HTML file
           `result`: relative path of 'result' page
           `Search`: search class used to search the index
           `index`: directory storing the Lucene index
    '''
    if request.method == "POST":
        keyword = request.form['keyword']
        return redirect(url_for(result, keyword=keyword))
    
    vm_env.attachCurrentThread()
    engine = Search(index, SimpleAnalyzer(), lambda x: ' '.join(jieba.cut(x)))
    keyword = request.args.get('keyword')

    command = {
        "type": result,
        "keyword": keyword
    }
    if command not in search_history:
        search_history.append(command)
    
    results = engine.search_command(keyword)
    return render_template(template, keyword=keyword, results=results)


@app.route('/', methods=['POST', 'GET'])
def index():
    return render_index(request, 'index.html', 'result')


@app.route('/result', methods=['POST', 'GET'])
def result():
    return render_result(request, 'result.html', 'result', SearchFiles, 'index')


@app.route('/img', methods=['POST', 'GET'])
def index_img():
    return render_index(request, 'index_img.html', 'result_img')


@app.route('/result_img', methods=['POST', 'GET'])
def result_img():
    return render_result(request, 'result_img.html', 'result_img', SearchImgs, 'index_img')


@app.route('/history', methods=['GET'])
def history():
    return render_template('history.html', history=search_history)


vm_env = None  # To be initialized in __main__
search_history = []
if __name__ == '__main__':
    vm_env = lucene.initVM()
    print('lucene', lucene.VERSION)
    app.run(debug=True, port=8080)
