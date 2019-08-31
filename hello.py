from flask import *
# from flask_bootstrap import Bootstrap
# from requests_toolbelt.adapters import appengine
# appengine.monkeypatch()

import geo_search, twitter
import numpy as np
import ml_ask, cause
import time
app = Flask(__name__)
# bootstrap = Bootstrap(app)

@app.route('/', methods=["GET", "POST"])
def hello_world():
    if request.method == "GET":
        return render_template('hello.html', location=None, tweets=[[]], cnt=None, cause=None)
    else:
        # t = geo_search.tweet_search(str(request.form["location"]))+twitter.tweet_search(str(request.form["location"]))
        t = ml_ask.ask(str(request.form["location"]))
        if t==None:
            return render_template('hello.html', location=str(request.form["location"]), tweets=[[]], cnt='0', cause='error')
        work = [x[0] for x in t]
        # print(work)
        for x in work:
            if str(request.form["location"]) in x:
                c = cause.cause(t, str(request.form["location"]))
                break
            else:
                c = 'error'
        return render_template('hello.html', location=str(request.form["location"]), tweets=t, cnt=str(len(t)), cause=c)

@app.route('/hello/')
def hello(name=None):
    return render_template('sample.html', name=name)

if __name__ == '__main__':
    app.run()
