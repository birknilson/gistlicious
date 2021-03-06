import os
from flask import Flask
from flask import render_template, request, redirect
from giststorage import GistStorage
from local import REDIS_PASSWORD

app = Flask(__name__)
app.debug = False

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upvote', methods=['POST'])
def upvote():
    app.storage.upvote(int(request.form['gist_id']))
    return redirect('/')

@app.route('/toplist')
def toplist():
    toplist = app.storage.get_rank_list(num=30)
    return render_template('toplist.html', toplist=toplist)

if __name__ == '__main__':
    REDIS_HOST = 'scat.redistogo.com'
    REDIS_PORT = 9176

    app.storage = GistStorage(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD)
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
