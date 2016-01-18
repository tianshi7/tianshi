#!/usr/bin/env python
# encoding: utf-8

from flask import Flask,request,render_template
from flask.ext.script import Manager
from flask.ext.bootstrap import Bootstrap

app = Flask(__name__)
bootstrap = Bootstrap(app)
manager = Manager((app))
@app.route('/')
def index():
    #return '<h1>Hello World!</h1>'
    return render_template('index.html')

@app.route('/user/<name>')
def user(name):
	#return '<h1>hello %s' % name
    return render_template('user.html',name=name)
@app.route('/agent')
def agent():
	user_agent = request.headers.get('User-Agent')
	return '<p>you browser is %s</p>' % user_agent

if __name__ == '__main__':
    manager.run()
