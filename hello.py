#!/usr/bin/env python
# encoding: utf-8

from flask import Flask app = Flask(__name__)

@app.route('/') def index():
    return '<h1>Hello World!</h1>h1>'

if __name__ == '__main__':
    app.run(debug=True)
